#!/bin/bash
arch="$(arch)"
cur_dir=$(dirname "$(readlink -f "$0")")
# 安装docker
docker version > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "docker is not installed"
  exit 1
fi

# 加载镜像
if [ "$arch" == "aarch64" ]; then
  image="ascendhub.huawei.com/public-ascendhub/ai-vault-arm:0.0.1"
else
  image="ascendhub.huawei.com/public-ascendhub/ai-vault-x86:0.0.1"
fi

# 初始化用户
useradd -d /home/AiVault -u 9001 -m AiVault
mkdir -p /home/AiVault
chown AiVault -R "$cur_dir"
chown AiVault -R /home/AiVault
# 签发证书
export LD_LIBRARY_PATH=/home/AiVault/lib:$LD_LIBRARY_PATH

# 读取私钥口令，同时作为新服务证书私钥口令
passwd=$1


# AI-VAULT导出CSR
docker run --rm -v "${cur_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /home/AiVault/ai-vault req -force -type MGMT -subject 'CN|SiChuan|ChengDu|Huawei|Ascend' || exit 1
docker run --rm -v "${cur_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /home/AiVault/ai-vault req -force -type SVC -subject 'CN|SiChuan|ChengDu|Huawei|Ascend' || exit 1

# 签发AI-VAULT证书
docker run --rm -v "${cur_dir}"/.ai-vault:/home/AiVault/.ai-vault $image openssl x509 -req -in /home/AiVault/.ai-vault/cert/svc/svc.csr -CA /home/AiVault/.ai-vault/ca.pem -CAkey /home/AiVault/.ai-vault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/svc.pem -days 3650 -passin pass:"${passwd}" || exit 1
docker run --rm -v "${cur_dir}"/.ai-vault:/home/AiVault/.ai-vault $image openssl x509 -req -in /home/AiVault/.ai-vault/cert/mgmt/mgmt.csr -CA /home/AiVault/.ai-vault/ca.pem -CAkey /home/AiVault/.ai-vault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/mgmt.pem -days 3650 -passin pass:"${passwd}" || exit 1

# 导入AI-VAULT证书
docker run --rm -v "${cur_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image  /home/AiVault/ai-vault x509 -type MGMT -caFile /home/AiVault/.ai-vault/ca.pem -certFile /home/AiVault/.ai-vault/mgmt.pem | grep 'fingerprint' || exit 1
docker run --rm -v "${cur_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image  /home/AiVault/ai-vault x509 -type SVC -caFile /home/AiVault/.ai-vault/ca.pem -certFile /home/AiVault/.ai-vault/svc.pem | grep 'fingerprint' || exit 1

# 生成服务证书私钥
docker run --rm -v "${cur_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /bin/bash -c "openssl rand -writerand ~/.rnd" || exit 1
docker run --rm -v "${cur_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /bin/bash -c "openssl genrsa -out /home/AiVault/.ai-vault/cert/server.key 4096" || exit 1
# 生成服务证书CSR
docker run --rm -v "${cur_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /bin/bash -c "openssl req -new -key /home/AiVault/.ai-vault/cert/server.key -subj '/CN=aivault' -out /home/AiVault/.ai-vault/cert/server.csr" || exit 1
# 生成服务证书
docker run --rm -v "${cur_dir}"/.ai-vault:/home/AiVault/.ai-vault -e LD_LIBRARY_PATH=/home/AiVault/lib $image /bin/bash -c "openssl x509 -req -in /home/AiVault/.ai-vault/cert/server.csr -CA /home/AiVault/.ai-vault/ca.pem -CAkey /home/AiVault/.ai-vault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/cert/server.pem -days 3650 -sha256 -extensions v3_ca -passin pass:${passwd}" || exit 1

# 清理临时文件
cp -af "$cur_dir"/.ai-vault /home/AiVault/

# 运行docker应用
docker run -d --restart=always -p 9000:9000 -p 5001:5001 -v /home/AiVault/.ai-vault:/home/AiVault/.ai-vault $image bash -c /home/AiVault/run.sh
sleep 3
docker ps | grep $image | grep "Up"
if [ $? -eq 0 ]; then
  echo "Install successful. Please visit https://ip:9000/"
else
  echo "Install failed, please check install step."
fi

rm -rf /home/AiVault/.ai-vault/ca.*
rm -rf /home/AiVault/.ai-vault/*.pem
rm -rf /home/AiVault/.ai-vault/cert/server.csr