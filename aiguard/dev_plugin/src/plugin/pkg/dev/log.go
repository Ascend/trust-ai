package dev

import (
	"errors"
	"github.com/fsnotify/fsnotify"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"gopkg.in/natefinch/lumberjack.v2"
	"os"
	"os/signal"
	"path/filepath"
	"strings"
	"syscall"
)

const (
	LogDirMode    = 0700
	LogLevel      = zapcore.InfoLevel
	FileMaxSize   = 20
	LogMode       = 0600
	BackupLogMode = 0400
)

var (
	RunLog         *zap.SugaredLogger
	OpLog          *zap.SugaredLogger
	HomePath       = getHomePath()
	RootPath       = filepath.Join(HomePath, ".aiguard_plugin")
	LogFolder      = filepath.Join(RootPath, "AtlasEdge_log")
	RunLogFile     = filepath.Join(LogFolder, "aiguard_plugin_run.log")
	OperateLogFile = filepath.Join(LogFolder, "aiguard_plugin_operate.log")
	IsCompress     bool
)

func getHomePath() string {
	dirname, _ := os.UserHomeDir()
	return dirname
}

func handleLogFolder(folder string) error {
	stat, err := os.Stat(folder)
	if err != nil {
		if err = os.MkdirAll(folder, LogDirMode); err != nil {
			return err
		}
	} else {
		if stat.IsDir() {
			if err := os.Chmod(folder, LogDirMode); err != nil {
				return err
			}
		} else {
			return errors.New("exist same name file")
		}
	}
	return nil
}

func handleLogFile(filename string) error {
	stat, err := os.Stat(filename)
	if err != nil {
		if os.IsNotExist(err) {
			f, _ := os.Create(filename)
            if err = os.Chmod(filename, LogMode); err != nil {
			return err
		}
			defer func() {
				_ = f.Close()
			}()
		}
	} else {
		if stat.IsDir() {
			return errors.New("exist same name folder")
		}
		if err = os.Chmod(filename, LogMode); err != nil {
			return err
		}
		return nil
	}
	return nil
}

func create(filename string) *zap.SugaredLogger {
	if err := handleLogFolder(LogFolder); err != nil {
		RunLog.Errorf("handle log folder(%s) failed:%s", LogFolder, err.Error())
		return nil
	}
	if err := handleLogFile(filename); err != nil {
		RunLog.Errorf("handle log file(%s) failed: %s", filename, err.Error())
		return nil
	}

	encoder := zapcore.NewConsoleEncoder(zap.NewDevelopmentEncoderConfig())
	lumberjackLogger := &lumberjack.Logger{
		Filename:   filename,
		MaxSize:    FileMaxSize,
		MaxBackups: MaxBackups,
		MaxAge:     MaxAge,
		Compress:   IsCompress,
	}
	writeSyncer := zapcore.NewMultiWriteSyncer(zapcore.AddSync(os.Stdout), zapcore.AddSync(lumberjackLogger))
	core := zapcore.NewCore(encoder, writeSyncer, LogLevel)
	logger := zap.New(core, zap.AddCaller()).Sugar()
	return logger
}

func workerWatcher(l *zap.SugaredLogger, filenames []string, stopCh <-chan os.Signal) {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		l.Errorf("NewWatcher failed: %s", err.Error())
		return
	}
	defer func() {
		_ = watcher.Close()
	}()
	if err = watcher.Add(LogFolder); err != nil {
		l.Error("watcher add log path failed")
	}
	l.Infof("start monitor log folder:%s", LogFolder)
	for {
		select {
		case <-stopCh:
			l.Info("receive stop signal, exit")
			os.Exit(0)
		case event, ok := <-watcher.Events:
			if !ok {
				l.Error("watcher event failed")
				return
			}
			if event.Op&fsnotify.Create == 0 {
				break
			}
			if err := changeMode(filenames, event); err != nil {
				l.Error("change mod failed")
			}
		case err, ok := <-watcher.Errors:
			if !ok {
				l.Error("watcher error failed")
				return
			}
			l.Errorf("watcher error: %s", err.Error())
			return
		}
	}
}

func contains(s []string, str string) bool {
	for _, v := range s {
		if v == str {
			return true
		}
	}
	return false
}

func changeMode(filenames []string, event fsnotify.Event) error {
	backupFileName := event.Name
	// ignore log file create event
	if contains(filenames, backupFileName) {
		return nil
	}

	// change mode for backup log file
	for _, filename := range filenames {
		prefix := strings.TrimSuffix(filename, filepath.Ext(filename))
		if strings.HasPrefix(backupFileName, prefix) {
			return os.Chmod(backupFileName, BackupLogMode)
		}
	}
	return nil
}

func InitLogger() {
	RunLog = create(RunLogFile)
	RunLog.Info("init RunLog success")
	OpLog = create(OperateLogFile)
	OpLog.Info("init OpLog success")
	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
	go workerWatcher(RunLog, []string{RunLogFile, OperateLogFile}, sig)
}
