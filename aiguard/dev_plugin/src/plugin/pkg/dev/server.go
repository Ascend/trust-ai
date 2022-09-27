/*
* Copyright(C) Huawei Technologies Co.,Ltd. 2022. ALL rights reserved.
 */

// Package dev : Provides device plugin registration server interface
package dev

// FuseDevicePluginManager is used to record Device Plugins
type FuseDevicePluginManager struct {
	DevicePlugin *FuseDevicePlugin
}

// CreateFuseDevPluginManager creation device plugin manager
func CreateFuseDevPluginManager(allDevs []*Conf) (*FuseDevicePluginManager, error) {
	pm := FuseDevicePluginManager{}
	for _, devConf := range allDevs {
		devPlugin, err := CreateFuseDevPlugin(devConf)
		if err != nil {
			RunLog.Errorf("CreateDevicePluginManager CreateDevicePlugin err: %v .", err)
			return nil, err
		}
		pm.DevicePlugin = devPlugin
	}
	return &pm, nil
}

// FuseDevPluginRegister device plugin register
func (d *FuseDevicePluginManager) FuseDevPluginRegister(isForce bool) error {
	devicePlugin := d.DevicePlugin
	if devicePlugin.IsRegistered && !isForce {
		RunLog.Infoln("FuseDevicePluginManager already Registered")
		return nil
	}
	RunLog.Infoln("start Register FuseDevicePluginManager.")
	return devicePlugin.FuseDevPluginRegister()
}

// FuseDevPluginRegAndServe : device plugin serve
func (d *FuseDevicePluginManager) FuseDevPluginRegAndServe() error {
	devicePlugin := d.DevicePlugin
	return devicePlugin.FuseDevPluginRegAndServe()
}

// FuseDevPluginTearDown device plugin TearDown serve
func (d *FuseDevicePluginManager) FuseDevPluginTearDown() {
	devicePlugin := d.DevicePlugin
	devicePlugin.FuseDevPluginTearDown()
}
