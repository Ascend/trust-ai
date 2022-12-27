#!/bin/bash
arch="$(arch)"
cur_dir=$(dirname "$(readlink -f "$0")")

BASE_DIR=$(dirname $(dirname "$cur_dir"))
readonly BASE_DIR

DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
USER_N=$(whoami)

function log_error() {
  echo "[ERROR] $*"
  echo "${DATE_N} ${USER_N}@${aivault_ip} [ERROR] $*" >>"${BASE_DIR}"/deploy.log
}

function operation_log_info() {
  echo "${DATE_N} ${USER_N}@${aivault_ip} [INFO] $*" >>"${BASE_DIR}"/deploy_operation.log
}

function run_docker() {
  [ $(docker ps|grep ai-vault-svc|wc -l) -ne 0 ] && docker stop ai-vault-svc && docker rm ai-vault-svc
  docker run -d --restart=always -p $mgmt_port:9000 -p $svc_port:5001 --name ai-vault-svc -v /home/AiVault/.ai-vault:/home/AiVault/.ai-vault $image bash -c /home/AiVault/run.sh $aivault_args
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

function export_certificate() {
  base_dir=$1
  # AI-VAULT导出CSR
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /home/AiVault/ai-vault req -force -type MGMT -subject 'CN|SiChuan|ChengDu|Huawei|Ascend' || return -1
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /home/AiVault/ai-vault req -force -type SVC -subject 'CN|SiChuan|ChengDu|Huawei|Ascend' || return -1

  # 签发AI-VAULT证书
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault $image openssl x509 -req -in /home/AiVault/.ai-vault/cert/svc/svc.csr -CA /home/AiVault/.ai-vault/ca.pem -CAkey /home/AiVault/.ai-vault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/svc.pem -days 3650 -extfile /etc/ssl/openssl.cnf -extensions v3_req -passin pass:"${passwd}" || return -1
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault $image openssl x509 -req -in /home/AiVault/.ai-vault/cert/mgmt/mgmt.csr -CA /home/AiVault/.ai-vault/ca.pem -CAkey /home/AiVault/.ai-vault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/mgmt.pem -days 3650 -extfile /etc/ssl/openssl.cnf -extensions v3_req -passin pass:"${passwd}" || return -1

  # 导入AI-VAULT证书
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image  /home/AiVault/ai-vault x509 -type MGMT -caFile /home/AiVault/.ai-vault/ca.pem -certFile /home/AiVault/.ai-vault/mgmt.pem | grep 'fingerprint' || return -1
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image  /home/AiVault/ai-vault x509 -type SVC -caFile /home/AiVault/.ai-vault/ca.pem -certFile /home/AiVault/.ai-vault/svc.pem | grep 'fingerprint' || return -1

  # 生成服务证书私钥
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault $image bash -c "openssl rand -writerand ~/.rnd" || return -1
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault $image openssl genrsa -out /home/AiVault/.ai-vault/cert/server.key 4096 || return -1
  # 生成服务证书CSR
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault $image openssl req -new -key /home/AiVault/.ai-vault/cert/server.key -subj '/CN=aivault' -out /home/AiVault/.ai-vault/cert/server.csr || return -1
  # 生成服务证书
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /bin/bash -c "openssl x509 -req -in /home/AiVault/.ai-vault/cert/server.csr -CA /home/AiVault/.ai-vault/ca.pem -CAkey /home/AiVault/.ai-vault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/cert/server.pem -days 3650 -sha256 -extfile /etc/ssl/openssl.cnf -extensions v3_req -passin pass:${passwd}" || return -1
  # 口令加密
  docker run --rm -v "${base_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /bin/bash -c "/home/AiVault/ai-whitebox enc -p ${passwd} > /home/AiVault/.ai-vault/encrypted_password" || return -1
}
# 导入证书失败后多次尝试
function update_certificate(){
  operation_log_info "start update certificate"
  for i in {1..3}
  do
    export_certificate $1
    if [ $? == 0 ];then
      echo "update certificate success"
      return 0
    else
      echo "update certificate $i times"
    fi
  done
  log_error "update certificate faild"
  exit 1
}

# 安装docker
docker version > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "docker is not installed"
  exit 1
fi

# 加载镜像
image=$4

# 指定svc端口
svc_port=$2

# 指定mgmt端口
mgmt_port=$3

# 是否更新证书
update_cert=$5

# 指定IP
aivault_ip=$6

# 指定aivault可选参数
aivault_args=$7  

# 非首次安装，不更新证书
if [ -d "/home/AiVault/.ai-vault/cert" ] && [ "${update_cert}" == "n" ]; then
  run_docker
fi

# 非首次安装，更新证书
if [ -d "/home/AiVault/.ai-vault/cert" ] && [ "${update_cert}" == "y" ]; then
  export LD_LIBRARY_PATH=/home/AiVault/lib:$LD_LIBRARY_PATH
  passwd=$1
  update_certificate "/home/AiVault"
  run_docker
fi

# 首次安装
# 初始化用户
useradd -d /home/AiVault -u 9001 -m AiVault
mkdir -p /home/AiVault/.ai-vault
chown AiVault -R "$cur_dir"
chown AiVault -R /home/AiVault
# 签发证书
export LD_LIBRARY_PATH=/home/AiVault/lib:$LD_LIBRARY_PATH

# 读取私钥口令，同时作为新服务证书私钥口令
passwd=$1

update_certificate $cur_dir

cp -af "$cur_dir"/.ai-vault /home/AiVault/

# 清理临时文件
rm -rf /home/AiVault/.ai-vault/cert/server.csr
[ -f /home/AiVault/.ai-vault/ca.srl ] && rm -f /home/AiVault/.ai-vault/ca.srl
[ -f /home/AiVault/.ai-vault/mgmt.pem ] && rm -f /home/AiVault/.ai-vault/mgmt.pem
[ -f /home/AiVault/.ai-vault/svc.pem ] && rm -f /home/AiVault/.ai-vault/svc.pem

run_docker
