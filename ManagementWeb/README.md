# 物资管理网页端
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
1. 物资的按种类管理，及物资新建、借出、项目使用、还入、送修、报废全生命流程管理。
2. 普通成员所有操作均需管理员审批，保障安全。
3. 支持条形码扫描，快速对应物品与ID。
4. 重要信息通过mirai推送到QQ群，第一时间掌握信息。

## 使用
本仓库使用Docker，可一键运行，请按如下代码进行配置，配置前请先安装好docker  
或使用[物资管理系统一键包](https://github.com/nuaa-rm/web_system)
```shell script
docker pull bismarckkk/management_web
docker run -d \
    --name=management_web \
    -p 8000:8000 \
    -v /home/bismarck/web_system:/code/config \
    -v /etc/localtime:/etc/localtime \
    bismarckkk/management_web
```
其中8001对应你在`settings.json`中配置的网页端端口  
`settings.json`请到 [物资管理系统一键包](https://github.com/nuaa-rm/web_system) 下载并配置  
/home/bismarck/web_system为存放`settings.json`目录
建议在前面套一层nginx或者httpd以使用https（自己不想配置的话可以用一键包  
  
`setting.json`里还有些要配置的见一键包的readme  