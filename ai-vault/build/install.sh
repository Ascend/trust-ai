#!/bin/bash
arch="$(arch)"

# 安装docker
docker version > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "docker already install"
else
  tar -zxf docker-20.10.12.tgz
  cp docker/* /usr/bin/
  cp -af docker.service /etc/systemd/system
	systemctl enable docker.service
	systemctl start docker
fi

# 加载镜像
image="ai-vault_${arch}.tar"
docker load < "${image}"

# 初始化用户
useradd -d /home/AiVault -u 9001 -m AiVault
cp ai-vault /home/AiVault/
cp -r lib /home/AiVault/
cp ca.pem /home/AiVault/
cp ca.key /home/AiVault/
chown AiVault:AiVault -R /home/AiVault
chown AiVault:AiVault -R .
chmod 700 /home/AiVault/ai-vault
# 签发证书
export LD_LIBRARY_PATH=/home/AiVault/lib:$LD_LIBRARY_PATH

# 读取私钥口令，同时作为新服务证书私钥口令
read -sp "Enter password for ca.key > " passwd
printf "\n"

# AI-VAULT导出CSR
su AiVault -c "/home/AiVault/ai-vault req -type MGMT -subject 'CN|SiChuan|ChengDu|Huawei|Ascend'" || exit 1
su AiVault -c "/home/AiVault/ai-vault req -type SVC -subject 'CN|SiChuan|ChengDu|Huawei|Ascend'" || exit 1

# 签发AI-VAULT证书
su AiVault -c "openssl x509 -req -in /home/AiVault/.ai-vault/cert/svc/svc.csr -CA /home/AiVault/ca.pem -CAkey /home/AiVault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/svc.pem -days 3650 -passin pass:'${passwd}'" || exit 1
su AiVault -c "openssl x509 -req -in /home/AiVault/.ai-vault/cert/mgmt/mgmt.csr -CA /home/AiVault/ca.pem -CAkey /home/AiVault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/mgmt.pem -days 3650 -passin pass:'${passwd}'" || exit 1

# 导入AI-VAULT证书
su AiVault -c "/home/AiVault/ai-vault x509 -type MGMT -caFile /home/AiVault/ca.pem -certFile /home/AiVault/.ai-vault/mgmt.pem" || exit 1
su AiVault -c "/home/AiVault/ai-vault x509 -type SVC -caFile /home/AiVault/ca.pem -certFile /home/AiVault/.ai-vault/svc.pem" || exit 1

# 生成服务证书私钥
su AiVault -c "openssl rand -writerand ~/.rnd" || exit 1
su AiVault -c "openssl genrsa -out /home/AiVault/.ai-vault/cert/server.key 4096" || exit 1
# 生成服务证书CSR
su AiVault -c "openssl req -new -key /home/AiVault/.ai-vault/cert/server.key -subj '/CN=aivault' -out /home/AiVault/.ai-vault/cert/server.csr" || exit 1
# 生成服务证书
su AiVault -c "openssl x509 -req -in /home/AiVault/.ai-vault/cert/server.csr -CA /home/AiVault/ca.pem -CAkey /home/AiVault/ca.key -CAcreateserial -out /home/AiVault/.ai-vault/cert/server.pem -days 3650 -sha256 -extensions v3_ca -passin pass:'${passwd}'" || exit 1

# 清理临时文件
rm -f /home/AiVault/.ai-vault/cert/server.csr
rm -r /home/AiVault/ai-vault
rm -rf /home/AiVault/lib
rm -f /home/AiVault/ca.pem
rm -f /home/AiVault/ca.key
rm -f /home/AiVault/ca.srl
rm -rf /home/AiVault/.ai-vault/*.pem

# 运行docker应用
docker run -d --restart=always -p 9000:9000 -p 5001:5001 -v /home/AiVault/.ai-vault:/home/AiVault/.ai-vault ai-vault:v1 bash -c /home/AiVault/run.sh
sleep 3
docker ps | grep "ai-vault:v1" | grep "Up"
if [ $? -eq 0 ]; then
  echo "Install successful, please visit https://ip:9000/"
else
  echo "Install failed, please check install step."
fi
