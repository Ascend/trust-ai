cp -af user-manager .ai-vault/
cp -af data-manager .ai-vault/
cp -af cert-manager .ai-vault/
cp -af nginx .ai-vault/
cp -af ai-vault .ai-vault/
cp -af lib .ai-vault/
chmod 700 -R .ai-vault


cd /home/AiVault/.ai-vault/cert || exit

export LD_LIBRARY_PATH=/home/AiVault/.ai-vault/lib

ip=`ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`

# 启动AI-VAULT
/home/AiVault/.ai-vault/ai-vault run -ip ${ip} -mgmtPort 5000 -servicePort 5001 $@ &

sed -i "s/docker_ip/${ip}/g" /home/AiVault/.ai-vault/nginx/conf/nginx.conf
sed -i "s/docker_ip/${ip}/g" /home/AiVault/.ai-vault/user-manager/configuration/install_param.json

# 启动APIGW
mkdir -p /home/AiVault/.ai-vault/nginx/logs
/usr/local/openresty/nginx/sbin/nginx -p /home/AiVault/.ai-vault/nginx/ -c conf/nginx.conf

# 启动data-manager
python3 ../data-manager/run.py &

# 启动user-manager
python3 ../user-manager/run.py &

# 启动cert-manager
python3 ../cert-manager/run.py &

# 监测程序是否正常运行中
while true
do
   if [ -f "/home/AiVault/.ai-vault/data-manager/restart_flag" ]; then
     sleep 10
     continue
   fi
   num1=`ps -u AiVault -ef|grep "/home/AiVault/.ai-vault/ai-vault run"|grep -v grep|wc -l`
   if test $[num1] -ne $[1]
   then
     exit 1
   fi
   num2=`ps -u AiVault -ef|grep "/usr/local/openresty/nginx/sbin/nginx -p /home/AiVault/.ai-vault/nginx/ -c conf/nginx.conf"|grep -v grep|wc -l`
   if test $[num2] -ne $[1]
   then
     exit 1
   fi
   num3=`ps -u AiVault -ef|grep "python3 ../data-manager/run.py"|grep -v grep|wc -l`
   if test $[num3] -ne $[1]
   then
     exit 1
   fi
   num4=`ps -u AiVault -ef|grep "python3 ../user-manager/run.py" |grep -v grep|wc -l`
   if test $[num4] -ne $[1]
   then
     exit 1
   fi
   num5=`ps -u AiVault -ef|grep "python3 ../cert-manager/run.py" |grep -v grep|wc -l`
   if test $[num5] -ne $[1]
   then
     exit 1
   fi
   sleep 10
done
