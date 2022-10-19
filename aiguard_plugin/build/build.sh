#!/bin/bash
# Perform  build k8s-device-plugin
# Copyright(C) Huawei Technologies Co.,Ltd. 2022. All rights reserved.

set -e
CUR_DIR=$(dirname "$(readlink -f "$0")")
TOP_DIR=$(realpath "${CUR_DIR}"/..)

output_name="aiguard-plugin"
os_type=$(arch)
build_type=build

export GO111MODULE="on"
export GONOSUMDB="*"

function build_plugin() {
    [ ! -d "${TOP_DIR}/output" ] && mkdir "${TOP_DIR}/output"
    cd "$TOP_DIR"/dev_plugin/src/plugin/cmd/aiguardplugin
    go mod tidy
    export CGO_ENABLED=1
    export CGO_CFLAGS="-fstack-protector-strong -D_FORTIFY_SOURCE=2 -O2 -fPIC -ftrapv"
    export CGO_CPPFLAGS="-fstack-protector-strong -D_FORTIFY_SOURCE=2 -O2 -fPIC -ftrapv"
    go build -buildmode=pie -ldflags " -buildid none     \
            -s   \
            -linkmode=external \
            -extldflags=-Wl,-z,relro,-z,now,-z,noexecstack" \
            -o "${output_name}"  \
            -trimpath
    ls "${output_name}"
    if [ $? -ne 0 ]; then
        echo "fail to find aiguard-plugin"
        exit 1
    fi
}

function mv_file() {
    mv "$TOP_DIR/dev_plugin/src/plugin/cmd/aiguardplugin/${output_name}"   "${TOP_DIR}"/output
    mkdir "$TOP_DIR"/aiguard_plugin
    mkdir "$TOP_DIR"/aiguard_plugin/aiguard-plugin
    mv "${TOP_DIR}"/output/${output_name} "$TOP_DIR"/aiguard_plugin/aiguard-plugin
    mkdir "$TOP_DIR"/aiguard_plugin/edge_om
    mkdir "$TOP_DIR"/aiguard_plugin/edge_om/config
    mv "$TOP_DIR/edge_user.json"   "${TOP_DIR}"/aiguard_plugin/edge_om/config
    mkdir "$TOP_DIR"/aiguard_plugin/limit_file
    mv "$TOP_DIR/cfs_profile"   "${TOP_DIR}"/aiguard_plugin/limit_file
    mv "$TOP_DIR/seccomp_profile.json"   "${TOP_DIR}"/aiguard_plugin/limit_file
    mkdir "$TOP_DIR"/aiguard_plugin/service
    mv "$TOP_DIR/aiguard_plugin.service"   "${TOP_DIR}"/aiguard_plugin/service
    mv "$TOP_DIR/install.sh" "$TOP_DIR"/aiguard_plugin
}

function change_mod() {
    chmod 600 "${TOP_DIR}/aiguard_plugin/limit_file/seccomp_profile.json"
    chmod 600 "${TOP_DIR}/aiguard_plugin/limit_file/cfs_profile"
    chmod 500 "${TOP_DIR}/aiguard_plugin/aiguard-plugin/${output_name}"
}

function zip_dir(){
    cd "${TOP_DIR}"/
    zip -r "${TOP_DIR}"/output/Ascend-mindxdl-aiguard_plugin.zip aiguard_plugin/
}

function main() {
  build_plugin
  mv_file
  change_mod
  zip_dir
}

main

