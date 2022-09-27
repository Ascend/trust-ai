/*
* Copyright(C) Huawei Technologies Co.,Ltd. 2022. ALL rights reserved.
 */

// Package dev : Provides device plugin registration interface
package dev

import (
	"errors"
	"fmt"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"k8s.io/kubelet/pkg/apis/deviceplugin/v1beta1"
	"net"
	"os"
	"path"
	"time"
)

// FuseDevicePlugin Fuse device plugin registration information
type FuseDevicePlugin struct {
	GrpcServer   *grpc.Server
	Devices      []*v1beta1.Device
	closeCh      chan interface{}
	Name         string
	Permission   string
	ResourceName string
	SockName     string
	IsRegistered bool
}

// CreateFuseDevPlugin create device plugin
func CreateFuseDevPlugin(devConf *Conf) (*FuseDevicePlugin, error) {
	var devices []*v1beta1.Device
	SharedNum := devConf.sharedNum
	RunLog.Infof("FuseDevicePlugin ShareNum is : %d .", SharedNum)
	for i := 0; i < SharedNum; i++ {
		devices = append(devices, &v1beta1.Device{
			ID:     fmt.Sprintf("%s-%d", devConf.name, i),
			Health: v1beta1.Healthy,
		})
	}
	return &FuseDevicePlugin{
		Devices:      devices,
		Name:         devConf.name,
		ResourceName: ResourceNamePrefix + devConf.resourceName,
		SockName:     devConf.resourceName + ".sock",
		IsRegistered: false,
		closeCh:      make(chan interface{}),
	}, nil
}

// FuseDevPluginRegister register device plugin
func (d *FuseDevicePlugin) FuseDevPluginRegister() error {
	conn, err := grpc.Dial(v1beta1.KubeletSocket, grpc.WithInsecure(), grpc.WithDialer(func(addr string, timeout time.Duration) (net.Conn, error) {
		return net.DialTimeout("unix", addr, timeout)
	}))
	if err != nil {
		RunLog.Errorf("connect to kubelet failed, err: %s.", err.Error())
		return err
	}
	defer conn.Close()
	client := v1beta1.NewRegistrationClient(conn)

	r := &v1beta1.RegisterRequest{
		Version:      v1beta1.Version,
		Endpoint:     d.SockName,
		ResourceName: d.ResourceName,
	}
	_, err = client.Register(context.Background(), r)
	if err != nil {
		d.IsRegistered = false
		RunLog.Errorf("FuseDevicePlugin Register %s error: %v", d.Name, err)
		return err
	}
	d.IsRegistered = true
	RunLog.Infof("FuseDevicePlugin Register success: %v.", d.Name)
	return nil
}

func (d *FuseDevicePlugin) createNetListen(pluginSocketPath string) (net.Listener, error) {
	RunLog.Infoln("createNetListen")
	if _, err := os.Stat(pluginSocketPath); err == nil {
		RunLog.Warnf("Found exist sock file, sockName is: %s, now remove it.", path.Base(pluginSocketPath))
		err := os.Remove(pluginSocketPath)
		if err != nil {
			RunLog.Errorf("remove sock %s err:%s", d.SockName, err.Error())
			return nil, err
		}
		RunLog.Infof("remove sock file %s successfully", d.SockName)
	}
	netListen, err := net.Listen("unix", pluginSocketPath)
	if err != nil {
		RunLog.Errorf("device plugin start failed, err: %s.", err.Error())
		return nil, err
	}
	err = os.Chmod(pluginSocketPath, socketChmod)
	if err != nil {
		RunLog.Errorf("change file: %s mode error.", path.Base(pluginSocketPath))
	}
	return netListen, err
}

// FuseDevPluginRegAndServe start device plugin register Serve
func (d *FuseDevicePlugin) FuseDevPluginRegAndServe() error {
	RunLog.Infoln("start DevicePlugin RegAndServe.")
	pluginSocketPath := v1beta1.DevicePluginPath + d.SockName
	RunLog.Infof("pluginSocketPath: %s.", d.SockName)
	netListen, err := d.createNetListen(pluginSocketPath)
	if err != nil {
		RunLog.Errorf("FuseDevPluginRegAndServe createNetListen err: %v .", err)
		return err
	}
	d.GrpcServer = grpc.NewServer([]grpc.ServerOption{}...)
	v1beta1.RegisterDevicePluginServer(d.GrpcServer, d)
	go d.GrpcServer.Serve(netListen)
	RunLog.Infof("DevicePluginRegAndServe(%s) success.", d.Name)
	return nil
}

// FuseDevPluginTearDown stop device plugin server
func (d *FuseDevicePlugin) FuseDevPluginTearDown() {
	if d.GrpcServer == nil {
		return
	}
	d.GrpcServer.Stop()
	d.GrpcServer = nil
	close(d.closeCh)
}

// ListAndWatch : if the server get stop signal ,the ListAndWatch should stop,to be fix
func (d *FuseDevicePlugin) ListAndWatch(_ *v1beta1.Empty, s v1beta1.DevicePlugin_ListAndWatchServer) error {
	err := s.Send(&v1beta1.ListAndWatchResponse{Devices: d.Devices})
	if err != nil {
		RunLog.Errorf("listAndWatch: send device info failed: %v .", err)
		return err
	}
	RunLog.Infoln("ListAndWatch ...")
	for {
		select {
		case <-d.closeCh:
			RunLog.Warnln("FuseDevicePlugin ListAndWatch receive close chan, return.")
			return nil
		}
	}
}

// Allocate is called by kubelet to mount device to k8s pod.
func (d *FuseDevicePlugin) Allocate(ctx context.Context, requests *v1beta1.AllocateRequest) (*v1beta1.AllocateResponse, error) {
	RunLog.Infof("AllocateRequest: %#v .", *requests)
	for _, n := range (*requests).ContainerRequests {
		RunLog.Infof("Allocate ContainerRequests: %#v .", *n)
	}
	var response v1beta1.AllocateResponse
	devSpec := v1beta1.DeviceSpec{
		HostPath:      d.Name,
		ContainerPath: d.Name,
		Permissions:   Permission,
	}
	var devicesList []*v1beta1.ContainerAllocateResponse
	devicesList = append(devicesList, &v1beta1.ContainerAllocateResponse{
		Devices: []*v1beta1.DeviceSpec{&devSpec},
		Mounts:  nil,
	})
	response.ContainerResponses = devicesList
	RunLog.Infof("Allocate Responses devSpec: %#v .", devSpec)
	return &response, nil
}

// GetDevicePluginOptions is Standard interface to kubelet.
func (d *FuseDevicePlugin) GetDevicePluginOptions(context.Context,
	*v1beta1.Empty) (*v1beta1.DevicePluginOptions, error) {
	return &v1beta1.DevicePluginOptions{PreStartRequired: false}, nil
}

// PreStartContainer is Standard interface to kubelet with empty implement.
func (d *FuseDevicePlugin) PreStartContainer(context.Context,
	*v1beta1.PreStartContainerRequest) (*v1beta1.PreStartContainerResponse, error) {
	return &v1beta1.PreStartContainerResponse{}, nil
}

// GetPreferredAllocation implement the kubelet device plugin interface
func (d *FuseDevicePlugin) GetPreferredAllocation(context.Context, *v1beta1.PreferredAllocationRequest) (
	*v1beta1.PreferredAllocationResponse, error) {
	return nil, errors.New("not support")
}
