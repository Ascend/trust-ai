/*
* Copyright(C) Huawei Technologies Co.,Ltd. 2022. ALL rights reserved.
 */

// Package dev : manager device plugin log
package dev

import (
	"io"
	"log"
	"os"
)

var (
	Info  *log.Logger
	Error *log.Logger
	Warn  *log.Logger
)

func InitLogger() {
	fire, err := os.OpenFile("aiguard_plugin.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0600)
	if err != nil {
		log.Fatalln("Faild to open error logger file:", err)
	}
	Info = log.New(io.MultiWriter(fire, os.Stderr), "INFO:", log.Ldate|log.Ltime|log.Lshortfile)
	Warn = log.New(io.MultiWriter(fire, os.Stderr), "WARN:", log.Ldate|log.Ltime|log.Lshortfile)
	Error = log.New(io.MultiWriter(fire, os.Stderr), "ERROR:", log.Ldate|log.Ltime|log.Lshortfile)
}
