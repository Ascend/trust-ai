/*
* Copyright(C) Huawei Technologies Co.,Ltd. 2022. ALL rights reserved.
 */

// Package dev : manager device plugin register
package dev

import (
	"encoding/json"
	"errors"
	"io/ioutil"
	"os/user"
	"path"
	"path/filepath"
	"strconv"
	"syscall"
)

// EdgeUserConfig edge user config message
type EdgeUserConfig struct {
	User string `json:"user"`
}

func getSelfExePath() (string, error) {
	resoledPath, err := filepath.EvalSymlinks(SelfExeLink)
	if err != nil {
		return "", errors.New("get the symlinks path failed")
	}
	if SelfExeLink == resoledPath {
		return "", errors.New("not a symlinks file")
	}
	return resoledPath, nil
}

func getUserName(configPath string) (string, error) {
	exePath, err := getSelfExePath()
	if err != nil {
		Error.Printf("Get aiguard-plugin exec file failed. %s \n", err.Error())
		return "", err
	}
	exeAbsPath, err := filepath.Abs(exePath)
	if err != nil {
		Error.Printf("Get  aiguard-plugin exec file absolute path failed. %s \n", err.Error())
		return "", err
	}
	var edgeWorkDir = path.Dir(path.Dir(exeAbsPath))
	configPath = path.Join(edgeWorkDir, configPath)
	realPath, err := filepath.Abs(configPath)
	if err != nil {
		return "", errors.New("get absolute path failed")
	}
	confByte, err := ioutil.ReadFile(realPath)
	if err != nil {
		Error.Printf("Load user Config err: %s.\n", err.Error())
		return "", err
	}
	if len(confByte) == 0 {
		Error.Println("user Config file is empty")
		return "", errors.New("config is empty")
	}
	var userConfig EdgeUserConfig
	err = json.Unmarshal(confByte, &userConfig)
	if err != nil {
		Error.Printf("LoadDeviceConfig Unmarshal config file err: %v.\n", err)
		return "", err
	}
	userName := userConfig.User
	return userName, err
}

// SetEdgeUserID set EdgeUserID to uid
func SetEdgeUserID() error {
	userName, err := getUserName(EdgeUserConfigPath)
	if err != nil || len(userName) == 0 {
		Error.Printf("get user Name error: %v. \n", err)
		return err
	}
	edgeUser, err := user.Lookup(userName)
	if err != nil {
		Error.Printf("invalid user %s \n", userName)
		return err
	}
	const decimalBase = 10
	const bit32Size = 32
	gid, err := strconv.ParseInt(edgeUser.Gid, decimalBase, bit32Size)
	if err != nil {
		return err
	}
	if err := syscall.Setgid(int(gid)); err != nil {
		Error.Printf("Set gid for user %s error: %s \n", userName, err.Error())
		return err
	}
	uid, err := strconv.ParseInt(edgeUser.Uid, decimalBase, bit32Size)
	if err != nil {
		return err
	}
	if err := syscall.Setuid(int(uid)); err != nil {
		Error.Printf("Set uid for user %s error: %s \n", userName, err.Error())
		return err
	}
	return nil
}
