#!/bin/bash
arch="$(arch)"
cur_dir=$(dirname "$(readlink -f "$0")")

function run_docker() {
  docker stop ai-vault-svc
  docker rm ai-vault-svc
  docker run -d --restart=always -p $mgmt_port:9000 -p $svc_port:5001 --name ai-vault-svc -v /home/AiVault/.ai-vault:/home/AiVault/.ai-vault $image bash -c /home/AiVault/run.sh
  sleep 3
  docker ps | grep $image | grep "Up"
  if [ $? -eq 0 ]; then
    echo "Install successful. Please visit https://ip:$mgmt_port/"
    exit 0
  else
    echo "Install failed, please check install step."
    exit 1
  fi
}

# 安装docker
docker version > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "docker is not installed"
  exit 1
fi

# 加载镜像
if [ -z $1 ]; then
  echo "Invalid image name, please specify aivault image name"
  exit 1
else
  image=$1
fi

# 指定svc端口
if [ -z $2 ]; then
  svc_port=5001
else
  svc_port=$2
fi

# 指定mgmt端口
if [ -z $3 ]; then
  mgmt_port=9000
else
  mgmt_port=$3
fi

# 非首次安装
if [ -d "/home/AiVault/.ai-vault" ]; then
  run_docker
fi

# 初始化用户
useradd -d /home/AiVault -u 9001 -m AiVault
mkdir -p /home/AiVault/.ai-vault
chown AiVault -R .
chown AiVault -R /home/AiVault
# 签发证书
export LD_LIBRARY_PATH=/home/AiVault/lib:$LD_LIBRARY_PATH

# 读取私钥口令，同时作为新服务证书私钥口令
read -sp "Enter password for ca.key > " passwd
printf "\n"

# AI-VAULT导出CSR
docker run -it --rm -v ${cur_dir}/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /home/AiVault/ai-vault req -force -type MGMT -subject 'CN|SiChuan|ChengDu|Huawei|Ascend' || exit 1
docker run -it --rm -v ${cur_dir}/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /home/AiVault/ai-vault req -force -type SVC -subject 'CN|SiChuan|ChengDu|Huawei|Ascend' || exit 1

# 签发AI-VAULT证书
docker run -it --rm -v ${cur_dir}/.ai-vault:/home/AiVault/.ai-vault $image openssl x509 -req -in /home/AiVault/.ai-vault/cert/svc/svc.csr -CA /home/AiVault/.ai-vault/ca.pem -CAkey /home/AiVault/.ai-vault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/svc.pem -days 3650 -extfile /etc/ssl/openssl.cnf -extensions v3_req -passin pass:${passwd} || exit 1
docker run -it --rm -v ${cur_dir}/.ai-vault:/home/AiVault/.ai-vault $image openssl x509 -req -in /home/AiVault/.ai-vault/cert/mgmt/mgmt.csr -CA /home/AiVault/.ai-vault/ca.pem -CAkey /home/AiVault/.ai-vault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/mgmt.pem -days 3650 -extfile /etc/ssl/openssl.cnf -extensions v3_req -passin pass:${passwd} || exit 1

# 导入AI-VAULT证书
docker run -it --rm -v ${cur_dir}/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image  /home/AiVault/ai-vault x509 -type MGMT -caFile /home/AiVault/.ai-vault/ca.pem -certFile /home/AiVault/.ai-vault/mgmt.pem | grep 'fingerprint' || exit 1
docker run -it --rm -v ${cur_dir}/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image  /home/AiVault/ai-vault x509 -type SVC -caFile /home/AiVault/.ai-vault/ca.pem -certFile /home/AiVault/.ai-vault/svc.pem | grep 'fingerprint' || exit 1

# 生成服务证书私钥
docker run -it --rm -v ${cur_dir}/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /bin/bash -c "openssl rand -writerand ~/.rnd" || exit 1
docker run -it --rm -v ${cur_dir}/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /bin/bash -c "openssl genrsa -out /home/AiVault/.ai-vault/cert/server.key 4096" || exit 1
# 生成服务证书CSR
docker run -it --rm -v ${cur_dir}/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /bin/bash -c "openssl req -new -key /home/AiVault/.ai-vault/cert/server.key -subj '/CN=aivault' -out /home/AiVault/.ai-vault/cert/server.csr" || exit 1
# 生成服务证书
docker run -it --rm -v ${cur_dir}/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /bin/bash -c "openssl x509 -req -in /home/AiVault/.ai-vault/cert/server.csr -CA /home/AiVault/.ai-vault/ca.pem -CAkey /home/AiVault/.ai-vault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/cert/server.pem -days 3650 -sha256 -extensions v3_ca -passin pass:${passwd}" || exit 1
cp -af .ai-vault /home/AiVault/

# 清理临时文件
rm -rf /home/AiVault/.ai-vault/ca.*
rm -rf /home/AiVault/.ai-vault/*.pem
rm -rf /home/AiVault/.ai-vault/cert/server.csr

run_docker
