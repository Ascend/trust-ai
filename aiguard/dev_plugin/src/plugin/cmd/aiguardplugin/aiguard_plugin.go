/*
* Copyright(C) Huawei Technologies Co.,Ltd. 2022. ALL rights reserved.
 */

// Package main implements initialization of the startup parameters of the device plugin.
package main

import (
	"aiguard-plugin/src/plugin/pkg/dev"
	"log"
)

var (
	sharedNum     = dev.MaxSharedNum
	logLevel      = dev.Loglevel
	logMaxAge     = dev.MaxAge
	logFile       = dev.LogPath
	logMaxBackups = dev.MaxBackups
)

func main() {
	dev.InitLogger()
	log.Println("aiguard plugin starting ...")
	hdm := dev.NewHwDevManager(sharedNum)
	hdm.Serve()
}
