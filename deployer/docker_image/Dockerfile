# syntax = docker/dockerfile:experimental
FROM ubuntu:18.04 as buildtemp

WORKDIR /tmp

COPY . ./

ENV GIT_SSL_NO_VERIFY=1

RUN sed -i "s@http://.*ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list && \
    apt update && \
    apt install -y --no-install-recommends curl git && \
    curl -kO https://mirrors.huaweicloud.com/python/3.7.9/Python-3.7.9.tgz && \
    git clone https://gitee.com/ascend/trust-ai && \
    cp aivault.tar trust-ai/deployer/resources

FROM ubuntu:18.04

RUN sed -i "s@http://.*ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list && \
    apt update && \
    apt install -y --no-install-recommends make g++ zlib1g zlib1g-dev libssl-dev libffi-dev vim ssh openssl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

ENV PATH=/usr/local/python3.7.9/bin:$PATH \
    LD_LIBRARY_PATH=/usr/local/python3.7.9/lib

RUN --mount=type=cache,target=/tmp,from=buildtemp,source=/tmp \
    tar -xf Python*.tgz && cd Python*/ && ./configure --prefix=/usr/local/python3.7.9 --enable-shared && \
    make -j 20 && make install && cd .. && \
    pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple/ && \
    pip3 config set global.trusted-host mirrors.aliyun.com && \
    pip3 install -U pip setuptools==65.6.0 cryptography==3.3.2 ansible-core==2.11.9 && \
    rm -rf /root/.cache && \
    cp -r /tmp/trust-ai /root && \
    cd /root/trust-ai/deployer && \
    python3 downloader/download.py

WORKDIR /root/trust-ai/deployer
