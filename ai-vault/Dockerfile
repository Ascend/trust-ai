FROM openresty/openresty:buster

RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN sed -i "/openresty.org/d" /etc/apt/sources.list
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install zlib* -y
RUN apt-get install sqlite3 -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install haveged -y
RUN apt-get install net-tools -y

RUN mkdir ~/.pip \
&& echo '[global] \n\
index-url=http://pypi.douban.com/simple\n\
trusted-host=pypi.douban.com' >> ~/.pip/pip.conf
COPY requirements.txt /
RUN pip3 install --upgrade pip setuptools wheel && pip3 install -r requirements.txt && rm requirements.txt

RUN useradd -d /home/AiVault -u 9001 -m -s /usr/sbin/nologin AiVault
WORKDIR /home/AiVault
COPY user-manager/ ./user-manager
COPY data-manager/ ./data-manager
COPY apigw/nginx/ ./nginx
COPY build/run.sh ./run.sh
RUN chown -R AiVault:AiVault ./
RUN chmod -R 700 ./
USER AiVault
CMD bash -c /home/AiVault/run.sh




