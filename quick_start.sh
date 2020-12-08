#!/bin/bash

echo "欢迎使用长空御风管理系统快速开始脚本"
echo "请确保您已经按照README的提示填写了setting_example.sh并将其重命名为setting.sh"
echo "确认完成上述操作后按任意键继续"
read anykey

pip3 install ujson pymysql
read -p "请问您是否需要安装docker(yes/no)" choose
if [ $choose = "yes" ]
then
  a=`uname  -a`
  c="centos"
  u="Ubuntu"

  if [[ $a =~ $c ]];then
      yum install -y yum-utils device-mapper-persistent-data lvm2
      yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
      yum makecache fast
      yum -y install docker-ce
      service docker start
  elif [[ $a =~ $u ]];then
      apt-get update
      apt-get -y install apt-transport-https ca-certificates curl software-properties-common
      curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
      add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
      apt-get -y update
      apt-get -y install docker-ce
      apt-get -y install docker.io

  else
      echo "无法识别您的操作系统，请尝试手动安装docker"
      exit
  fi
fi

read -p "请问您是否需要安装docker-compose(yes/no)" choose
if [ $choose = "yes" ]
then
  pip3 install docker-compose
fi

read -p "请问您是否需要安装mysql(yes/no)" choose
if [ $choose = "yes" ]
then
  docker pull mysql:5.7
  read -p "请设置数据库root账号密码" passwd
  docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=${passwd} -d mysql:5.7
  echo "请稍后，正在等待mysql数据库启动"
  sleep 5s
fi

python3 init.py
if [ $? == 1]
then
  exit
fi

docker-compose up -d
echo "quick-start完成"
