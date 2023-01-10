#!/bin/bash
function install_docker() {
    tar -xf docker*.tgz
    cp docker/* /usr/bin
    rm -rf docker
    cp docker.service /etc/systemd/system
    systemctl enable docker >/dev/null
    systemctl daemon-reload
    systemctl restart docker
}

function run_deployer() {
    mkdir -p deploy
    rm -rf deploy/*
    tar -xf deployer.tar -C deploy
    image_name=$(docker load <deploy/deployer.tar | awk '{print $3}')
    docker run -it --rm -v "$PWD"/inventory_file:/root/trust-ai/deployer/inventory_file "$image_name" bash
}

function main() {
    if [ "$(command -v docker | wc -l)" -eq 0 ]; then
        if ! install_docker; then
            echo "install docker failed"
            exit 1
        else
            echo "install docker success"
        fi
    else
        if [ "$(systemctl is-active docker)" != 'active' ]; then
            systemctl daemon-reload
            if ! systemctl restart docker; then
                echo "restart docker failed"
                exit 1
            fi
        fi
    fi
    run_deployer
}

main
main_status=$?
exit ${main_status}
