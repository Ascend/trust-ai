# aiguard python库离线安装FAQ

## 环境依赖

1. 一台已联网的Linux环境，且Linux环境的架构（arm64/x86_64）和待安装的环境一致。
2. 环境上已经安装所需的python版本、pip工具及打包工具。
3. 无网络环境上的python版本与联网时下载使用的python版本一致。

### Linux系统流程

1. 执行'pip3 -V'查看pip工具绑定的python版本，确认是要使用的python版本。
2. 创建一个空目录，进入创建的目录，创建一个requirements.txt文件，将要下载的python库依赖放入requirements.txt，内容参考如下：

    ```text
    urllib3==1.26.5
    esdk-obs-python
    pexpect==4.8.0
    pycryptodome==3.12.0
    click==8.0.4
    ```

3. 创建一个新目录用于存放下载的依赖（以pylibs为例，创建其他目录时请将pylibs替换为对应目录），在当前目录执行`pip3 download -r requirements.txt -d pylibs`将依赖下载到指定目录。
4. 进入pylibs目录，执行`tar -cf aiguard_pip.tar *`将下载的python库打包成aiguard_pip.tar文件。
5. 将aiguard_pip.tar和requirements.txt文件拷贝到无网络环境上相同目录，在aiguard_pip.tar文件所在目录创建一个空目录（以pylibs为例），执行`tar -xf aigruar_pip.tar -C pylibs`解压到pylibs目录。
6. 进入aiguard_pip.tar所在目录，root用户执行`pip3 install --force-reinstall -r requirements --no-index --find-links pylibs`，非root用户执行`pip3 install --force-reinstall -r requirements --no-index --find-links pylibs --user`
