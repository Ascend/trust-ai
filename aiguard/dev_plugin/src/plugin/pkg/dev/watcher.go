/*
* Copyright(C) Huawei Technologies Co.,Ltd. 2022. ALL rights reserved.
 */

// Package dev : Provides device plugin file watch interface
package dev

import (
	"errors"
	"github.com/fsnotify/fsnotify"
	"os"
	"os/signal"

	"syscall"
)

// FileWatch is used to watch sock file
type FileWatch struct {
	fileWatcher *fsnotify.Watcher
}

// NewFileWatch is used to watch socket file
func NewFileWatch() *FileWatch {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		return nil
	}
	return &FileWatch{
		fileWatcher: watcher,
	}
}

func (fw *FileWatch) watchFile(fileName string) error {
	_, err := os.Stat(fileName)
	if err != nil {
		return err
	}
	err = fw.fileWatcher.Add(fileName)
	if err != nil {
		return err
	}
	return nil
}

func newSignWatcher(osSigns ...os.Signal) chan os.Signal {
	signChan := make(chan os.Signal, 1)
	for _, sign := range osSigns {
		signal.Notify(signChan, sign)
	}
	return signChan
}

func signNotify(sigs chan os.Signal) error {
	Info.Println("(Press CTRL+C to quit).")
	if sigs == nil {
		Info.Println("no sigs.")
		return errors.New("sigs is nil")
	}
	select {
	case s, signEnd := <-sigs:
		if signEnd == false {
			Info.Println("no watcher sign event, channel closed.")
			return errors.New("no watcher sign event, channel closed")
		}
		switch s {
		case syscall.SIGHUP, syscall.SIGINT, syscall.SIGTERM, syscall.SIGQUIT, syscall.SIGKILL:
			Info.Println("Received exit signal, shutting down.")
			return nil
		default:
			Info.Printf("Received unknown signal: %s, shutting down.\n", s.String())
			return errors.New("received unknown signal, shutting down")
		}
	}
}
