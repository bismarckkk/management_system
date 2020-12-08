# NUAA长空御风管理系统
##### 由于整套物资管理系统均只有一人开发和维护，代码中多有bug少有注释请见谅，若有其他问题请提issue，欢迎提PR
### 本程序基于GNU GPL 3.0协议开放源代码，在使用源代码时请务必注意以下几点
1. 任何基于本程序修改或衍生发布的代码应同样使用GPL 3.0协议开放源代码，并在显要位置提及本仓库。
2. 强烈建议其他以任何形式间接接触本程序的代码使用GPL 3.0协议开放源代码，并在文档中提及本仓库。
3. 若您将此代码用于盈利，则必须在显要位置说明此代码可以免费获得。
4. 您使用此代码及其衍生代码造成的一切后果本仓库不负任何责任。

## 目录
- [联系开发者](#联系开发者)
- [项目框架](#项目框架)
- [项目截图](#项目截图)
- [已实现的功能](#已实现的功能)
- [TODO](#TODO)
- [一键使用](#一键使用)
- [一些说明](#备注)
- [项目配置](#项目配置)
- [使用之前](#使用之前)
    - [配置qq_oauth](#配置qq_oauth)
    - [配置微信小程序](#配置微信小程序)
    - [配置https](#配置https)
    - [修改网站图标](#修改网站图标)
    - [域名转发设置](#域名转发设置)
    - [mirai配置](#mirai配置)
- [数据库指南](#数据库指南)

## 联系开发者
本人联系方式
> QQ 3040585972  
> WX abc55660745abc  
> email zuoqingyu@nuaa.edu.cn  

欢迎骚扰（bushi  

## 项目框架
![httpd.png](https://i.loli.net/2020/11/29/FcC6anejrgu1DIX.png)  
1. 网页端物资管理系统: 见本仓库`ManagementWeb`  
2. 小程序物资管理系统：见本仓库`ManagementMiniProgram`  
3. 小程序后端：见本仓库`ManagementBackend`  
4. webhook模块：见本仓库`webhook`  
> mirai利用miraiHttpApi接入：  
> https://github.com/mamoe/mirai  
> https://github.com/project-mirai/mirai-api-http  

## 项目截图
![物资总览与搜索.jpg](https://i.loli.net/2020/12/08/bROJZiUBdDEXaA3.jpg)
![分类查看.jpg](https://i.loli.net/2020/12/08/Ia2Avzy6HsN1CuR.jpg)  
![物品详情.jpg](https://i.loli.net/2020/12/08/XYi3vFfOdLTxzyP.jpg)
![签到签退与请假.jpg](https://i.loli.net/2020/12/08/b9jQOAt85s4rGnC.jpg)
![qq消息推送.jpg](https://i.loli.net/2020/12/08/3z8mM5ShoUAVb9a.jpg)  
  
PS 消息推送里没人签到是因为系统在试运行

## 已实现的功能
1. 物资的按种类管理，及物资新建、借出、项目使用、还入、送修、报废全生命流程管理。
2. 普通成员所有操作均需管理员审批，保障安全。
3. 支持条形码扫描，快速对应物品与ID。
4. 支持多地点WIFI定位签到签退、工时计算、请假管理，保证出勤率
5. 所有申请记录可追溯，确定责任人。
6. 重要信息通过mirai推送到QQ群，第一时间掌握信息。
7. 接受github、svn的webhook推动，将仓库更新事件通过mirai发送至qq群，随时掌握工作进度
8. github与svn推送鉴权，防止假消息轰炸

## TODO
1. 支持httpd代理更换到其他端口（其实现在你自己改配置文件也能实现
2. 网页端修改authkey认证体系，提高系统安全性
3. 加入小程序端审批功能
4. 接入微信订阅消息
5. 接入钉钉

## 一键使用
##### 一键使用前请先完成下述项目配置
一键使用参考流程  
（使用前请确保已经安装python3环境，将用于初始化数据库  
如果部署缓慢请尝试使用阿里云容器镜像加速器  
```shell script
git clone websystem
cd websystem
chmod +x quick_start.sh
sudo ./quick_start.sh
```
`quick_start.sh`参考对话  
```
欢迎使用长空御风管理系统快速开始脚本
请确保您已经按照README的提示填写了setting_example.sh并将其重命名为setting.sh
确认完成上述操作后按任意键继续
> enter
请问您是否需要安装docker(yes/no)
> yes
......
请问您是否需要安装docker-compose(yes/no)
> yes
......
请问您是否需要安装mysql(yes/no)
> yes
......
请设置数据库root账号密码
> 123456
请稍后，正在等待mysql数据库启动
......
docker-compose.yaml写入成功
数据库初始化成功
......
quick-start完成
```

## 备注
目前删除项目、设置管理员等超级管理员功能暂时没有在前端实现，
如需操作请使用数据库软件访问数据库，
参照数据库指南进行操作

## 项目配置
##### 配置文件在仓库中`settings_example.json`
##### 注意配置好后请把名字改成`settings.json`  
具体配置方法参考[config.md](config.md)

## 使用之前
由于使用了qq oauth登录以及小程序，故需要一些提前的配置
##### 注意：微信要求后端地址仅能使用https及443端口，qq oauth强制要求备案号，请保证你使用的域名的主域名已备案

### 配置qq_oauth
在 https://connect.qq.com 登录并注册开发者账号，新建一个应用  
注意此处应用名称必须与备案名称相符，域名可以是备案域名的二级域名  
回调地址是`网页端访问地址/callback`  
申请通过后会获得appid与appkey，填入配置文件即可  

### 配置微信小程序
1. 在微信开放平台注册一个小程序。
2. 进入公众平台->开发管理->开发设置，找到并记录`AppID`与`AppSecret`。
3. 在上述界面，服务器域名中将后端域名加入白名单。

### 配置https
可以用阿里云的免费SSL证书，直接申请过几分钟就能下载，还有小绿锁  
如果使用一键配置脚本请下载apache版本证书文件  
然后将文件解压到`conf/cert`下  
最后修改`conf/extra2/httpd-ssl.conf`文件，将里面的证书文件名改为正确名称

### 修改网站图标
更换`static/favicon.ico`文件即可  

### 域名转发设置
##### 如果用一键包这一项就不用看了
由于上述SSL证书只能保护一个二级域名，本系统可以使用域名转发工作在一个二级域名下  
工作路径如下   
  
二级域名  
|-- /webhook webhook工作域名  
|-- /wx      小程序后端工作域名  
|-- /static  静态文件存放地址  
|-- /        网页端工作域名  
  
Apache配置文件示例
```conf
<VirtualHost *:443>
    ServerName   "二级域名"
    DirectoryIndex index.php index.html
    SSLEngine on
    SSLProtocol all -SSLv2 -SSLv3
    SSLCipherSuite HIGH:!RC4:!MD5:!aNULL:!eNULL:!NULL:!DH:!EDH:!EXP:+MEDIUM
    SSLHonorCipherOrder on
    SSLCertificateFile 你的ssl.crt
    SSLCertificateKeyFile 你的ssl.key
    SSLCertificateChainFile 你的ssl_chain.crt
    ProxyPass /wx http://127.0.0.1:8001/
    ProxyPassReverse /wx http://127.0.0.1:8001/
    ProxyPass /webhook http://127.0.0.1:8002/webhook/
    ProxyPassReverse /webhook http://127.0.0.1:8002/webhook/
    ProxyPass /static http://127.0.0.1:8003/
    ProxyPassReverse /static http://127.0.0.1:8003/
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>

<VirtualHost *:80>
    ServerName   "你的域名"
    RewriteEngine On
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R,L]
</VirtualHost>

<VirtualHost *:8003>
    DocumentRoot "静态文件存放路径"
    DirectoryIndex index.php index.html
</VirtualHost>
```
##### 注意：其中静态文件为本仓库static文件夹中的内容，顺便换logo也在这里面

### mirai配置
具体参考mirai那边的使用方法吧，我实在敲不动了

## 数据库指南
参考[database.md](database.md)
