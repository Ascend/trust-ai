/*
* Copyright(C) Huawei Technologies Co.,Ltd. 2022. ALL rights reserved.
 */

// Package dev : manager device plugin register
package dev

import (
	"errors"
	"fmt"
	"github.com/fsnotify/fsnotify"
	"go.uber.org/atomic"
	"k8s.io/kubelet/pkg/apis/deviceplugin/v1beta1"
	"os"
	"path"
	"path/filepath"
	"syscall"
)

const (
	socketChmod = 0600
	// ResourceNamePrefix Resource name prefix
	ResourceNamePrefix = "huawei.com/"
	// Name resource name
	Name         = "/dev/fuse"
	resourceName = "dev-fuse"
	// Permission device permission
	Permission = "rw"
	// MaxAge is Maximum number of days for backup run log files
	MaxAge = 7
	// MaxBackups Maximum number of backup log files
	MaxBackups = 30
	// MaxSharedNum Maximum device shared num
	MaxSharedNum = 32
	// EdgeUserConfigPath edge user config file path
	EdgeUserConfigPath = "edge_om/config/edge_user.json"
	// SelfExeLink The current execution file soft link
	SelfExeLink = "/proc/self/exe"
)

// Conf struct For record device configuration information
type Conf struct {
	name         string
	permission   string
	sharedNum    int
	resourceName string
}

// HwDevManager struct for HwDevManager
type HwDevManager struct {
	stopFlag *atomic.Bool
	allDevs  []*Conf
}

// NewHwDevManager function is used to new a dev manager.
func NewHwDevManager(sharedNum int) *HwDevManager {
	devConf := &Conf{
		name:         Name,
		permission:   Permission,
		sharedNum:    sharedNum,
		resourceName: resourceName,
	}
	var allDevs []*Conf
	allDevs = append(allDevs, devConf)
	return &HwDevManager{
		stopFlag: atomic.NewBool(false),
		allDevs:  allDevs,
	}
}

func (hdm *HwDevManager) checkDev(name string) error {
	fileInfo, err := os.Stat(name)
	if err != nil {
		RunLog.Errorf("device: %s not exist.", name)
		return err

	}
	if fileInfo.Mode()&os.ModeDevice != os.ModeDevice {
		RunLog.Errorf("file:%s is not a device file.", name)
		return err
	}
	return nil
}

func (hdm *HwDevManager) start(pm *FuseDevicePluginManager, isForce bool) error {
	if err := pm.FuseDevPluginRegister(isForce); err != nil {
		RunLog.Errorf("Register error: %v.", err)
		return err
	}
	if err := pm.FuseDevPluginRegAndServe(); err != nil {
		RunLog.Errorf("RegisterDeviceAndServe error: %v.", err)
		return err
	}
	return nil
}

// Serve start grpc server
func (hdm *HwDevManager) Serve() error {
	RunLog.Infoln("Starting OS signs watcher.")
	osSignChan := newSignWatcher(syscall.SIGHUP, syscall.SIGINT, syscall.SIGTERM, syscall.SIGQUIT, syscall.SIGKILL)
	if err := hdm.checkDev(Name); err != nil {
		return signNotify(osSignChan)
	}
	socketPath := v1beta1.DevicePluginPath
	realDevSockPath, err := filepath.Abs(socketPath)
	if err != nil {
		return errors.New("get absolute path failed")
	}
	pluginSocket := fmt.Sprintf("%s.sock", resourceName)
	pluginSockPath := path.Join(realDevSockPath, pluginSocket)
	RunLog.Infoln("Starting socket path watcher")
	watcher := NewFileWatch()
	if err := watcher.watchFile(realDevSockPath); err != nil {
		RunLog.Errorf("failed to create file watcher, err:%s.", err.Error())
		return signNotify(osSignChan)
	}
	defer watcher.fileWatcher.Close()
	pm, err := CreateFuseDevPluginManager(hdm.allDevs)
	if err != nil {
		RunLog.Errorf("Create DevicePlugin Manager error: %v.", err)
		return signNotify(osSignChan)
	}
	if err := hdm.start(pm, false); err != nil {
		RunLog.Errorf("start register server error: %v.", err)
	}
	if err := SetEdgeUserID(); err != nil {
		RunLog.Errorf("Set uid error :%s ", err.Error())
		pm.FuseDevPluginTearDown()
		return signNotify(osSignChan)
	}
	for !hdm.stopFlag.Load() {
		if hdm.stopFlag.Load() {
			break
		}
		exitSigs := hdm.signalWatch(watcher.fileWatcher, osSignChan, pluginSockPath)
		if exitSigs {
			pm.FuseDevPluginTearDown()
			break
		}
	}
	return nil
}

func (hdm *HwDevManager) signalWatch(watcher *fsnotify.Watcher, sigs chan os.Signal, pluginSockPath string) bool {
	if sigs == nil {
		RunLog.Infoln("no sigs.")
		return true
	}
	select {
	case event, signEnd := <-watcher.Events:
		if signEnd == false {
			RunLog.Infoln("no watcher event, channel closed.")
			return true
		}
		if event.Name == pluginSockPath && event.Op&fsnotify.Remove == fsnotify.Remove {
			RunLog.Warnln("notify: sock file deleted, plese check!")
		}
		if event.Name == v1beta1.KubeletSocket && event.Op&fsnotify.Create == fsnotify.Create {
			RunLog.Infoln("notify:kubelet.sock file created, Reboot required")
			return true
		}
	case s, signEnd := <-sigs:
		if signEnd == false {
			RunLog.Infoln("no watcher sign event, channel closed.")
			return true
		}
		switch s {
		case syscall.SIGHUP, syscall.SIGINT, syscall.SIGTERM, syscall.SIGQUIT, syscall.SIGKILL:
			RunLog.Infoln("Received exit signal, shutting down.")
			return true
		default:
			RunLog.Infof("Received unknown signal: %s, shutting down.", s.String())
			return true
		}
	}
	return false
}
