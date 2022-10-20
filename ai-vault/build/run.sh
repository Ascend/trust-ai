cp -af user-manager .ai-vault/
cp -af data-manager .ai-vault/
cp -af nginx .ai-vault/
cp -af ai-vault .ai-vault/
cp -af lib .ai-vault/
chmod 500 .ai-vault/ai-vault


cd /home/AiVault/.ai-vault/cert || exit

export LD_LIBRARY_PATH=/home/AiVault/.ai-vault/lib:$LD_LIBRARY_PATH

ip=`ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`

# 启动AI-VAULT
../ai-vault  run -ip ${ip} -mgmtPort 5000 -servicePort 5001 &

sed -i "s/pod_ip/${ip}/g" /home/AiVault/.ai-vault/nginx/conf/nginx.conf

# 启动APIGW
mkdir -p /home/AiVault/.ai-vault/nginx/logs
/usr/local/openresty/nginx/sbin/nginx -p /home/AiVault/.ai-vault/nginx/ -c conf/nginx.conf

# 启动data-manager
python3 ../data-manager/run.py &

# 启动user-manager
python3 ../user-manager/run.py
