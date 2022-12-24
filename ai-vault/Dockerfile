FROM openresty/openresty:buster

RUN sed -i "s/deb.debian.org/repo.huaweicloud.com/g" /etc/apt/sources.list
RUN sed -i "/openresty.org/d" /etc/apt/sources.list
RUN apt-get update && \
    apt-get install -y build-essential libssl1.1 zlib* procps sqlite3 python3 python3-pip haveged net-tools

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
COPY cert-manager/ ./cert-manager
# ai-tool is an executable file
COPY ai-tool ./ai-tool
COPY apigw/nginx/ ./nginx
COPY build/run.sh ./run.sh
COPY ai-vault ./ai-vault
COPY lib ./lib
RUN chown -R AiVault:AiVault ./
RUN chmod -R 700 ./
USER AiVault
ENV LD_LIBRARY_PATH=/home/AiVault/lib
CMD bash -c /home/AiVault/run.sh
