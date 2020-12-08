# webhook模块
##### 由于整套物资管理系统均只有一人开发和维护，代码中多有bug少有注释请见谅，若有其他问题请提issue
### 本程序基于GNU GPL 3.0协议开放源代码，在使用源代码时请务必注意以下几点
1. 任何基于本程序修改或衍生发布的代码应同样使用GPL 3.0协议开放源代码，并在显要位置提及本仓库。
2. 强烈建议其他以任何形式间接接触本程序的代码使用GPL 3.0协议开放源代码，并在文档中提及本仓库。
3. 若您将此代码用于盈利，则必须在显要位置说明此代码可以免费获得。
4. 您使用此代码及其衍生代码造成的一切后果本仓库不负任何责任。

## 联系开发者
本人联系方式
> QQ 3040585972  
> WX abc55660745abc  
> email zuoqingyu@nuaa.edu.cn  

欢迎骚扰（bushi

## 已经实现的功能
1. 接受github、svn的webhook推动，将仓库更新事件通过mirai发送至qq群，随时掌握工作进度
2. github与svn推送鉴权，防止假消息轰炸

## 使用
### 服务器端配置
本仓库使用Docker，可一键运行，请按如下代码进行配置，配置前请先安装好docker  
或使用[物资管理系统一键包](https://github.com/nuaa-rm/web_system)
```shell script
docker pull bismarckkk/webhook
docker run -d \
    --name=management_backend \
    -p 8002:8002 \
    -v /home/bismarck/web_system:/code/config \
    -v /etc/localtime:/etc/localtime \
    bismarckkk/webhook
```
其中8001对应你在`settings.json`中配置的webhook端口  
`settings.json`请到 [物资管理系统一键包](https://github.com/nuaa-rm/web_system) 下载并配置  
/home/bismarck/web_system为存放`settings.json`目录
建议在前面套一层nginx或者httpd以使用https（自己不想配置的话可以用一键包

### github端配置
在需要推送的仓库的setting里新建webhook推送到服务器，注意secret与服务器配置一致，具体操作流程可百度
推送地址为`您的webhook服务器地址/github`

### svn端设置
我偷懒用了ones的svn webhook代码，回头把脚本和配置方法一块发上来
1. 将`webhook.py`下载至您的SVN服务器，并在服务器上配置好python2.7环境
2. 执行如下指令
```shell script
cd ${WEBHOOK_PATH}
python webhook.py add \
# 注意：Windows 用户需提前准备 Python 2.7 环境
--repo_dir ${SVN_REPO_PATH} \
# 请将 ${SVN_REPO_PATH} 替换成 SVN 代码仓的路径，例如 Linux：/opt/svn/your_repo，Windows：C:\svn\your_repo
--webhook_url https://rm.bismarck.xyz/webhook/svn \
# 推送服务器地址为`您的webhook服务器地址/svn`
--secret_key 1122334455 \
# 此处设置应与配置文件中svn_secret相同
--link_url http://your_link_url/{commit_id}
# 根据第三方代码提交详情的链接规律，填写 link_url 的参数值
请将 http://your_link_url/ 替换成链接中除 Commit ID 以外的部分；系统会将 {commit_id} 处理成实际 Commit ID
# 以下举例指定 Upsource 链接的方法：
# 1. 在 Upsource 中选取某次代码提交的详情链接，例如 http://47.112.x.x:x/your_project/revision/123
# 2. 将链接中的 Commit ID 替换成 {commit_id}，例如 http://47.112.x.x:x/your_project/revision/{commit_id}
# 3. 将替换后的链接写入命令，例如 --link_url http://47.112.x.x:x/your_project/revision/{commit_id}
```  
  
`setting.json`里还有些要配置的见一键包的readme  