# 配置文件解读
本配置文件使用json语法
```json5
{
  "httpd": {
    "http_port": 80,
    "https_port": 443
  },
  // 若您不需要在服务器前端再套一层分发就不要再改这个了，若有需要我相信应该也能知道咋改
  // 补充：该配置暂时不受支持，因为一些docker的原因，后续将会修复
  "webhook": {
    "enable": true,
    // 在这里设置是否启用模块，下面有这个项目的模块都可以设置
    "name2user": {
      "这里填git或者svn用户名": "这里填真实姓名",
      "这里填git或者svn用户名2": "这里填真实姓名2"
    },
    "github_secret": "github webhook设置的secret",
    "svn_secret": "svn webhook设置的secret",
    "port": 8002,
    // 此处为webhook的工作端口，将会使用httpd或者nginx进行映射
    "targets": [1234567, 12345678],
    // 此处为收到新push后需要发送消息的群聊（QQ群）
  },
  "mysql": {
    "host": "mysql主机地址",
    "user": "访问用户名",
    "password": "访问密码",
    "db": "数据库名"
  },
  // 如果使用一键包建立mysql数据库则host填写本机公网IP或域名，并开放mysql端口，用户名填写root
  // 密码必须与在quick_start中输入的值相同，其余自行补充
  // 网页端和小程序端需共用mysql以保证数据同步
  "mirai": {
    "url": "mirai工作地址，注意最后要带/",
    "authkey": "mirai_http_api的authkey",
    "qq": 12345678
  },
  // 本系统所有QQ推送相关均使用mirai实现，需要配置mirai相关参数
  // 最后一个qq为机器人qq
  "web": {
    "qq_oauth": {
      "appid": "qq开放平台appid",
      "appkey": "qq开放平台appkey"
    },
    // 网页端基于qq oauth登录，懒得实现本地登录了，需要按下面步骤申请并填写
    "port": 8000,
    // 网页端工作端口，回头也得映射
    "targets": [1234567],
    // 有新的申请需要审批时推送消息的qq群（一般是队长团群）
    "title": "网站标题",
    "subtitle": "网站副标题",
    "website": "网站网址"
  },
  "wx_backend": {
    "wx_miniprogram": {
      "wxid": "微信小程序id",
      "wxkey": "微信小程序key"
    },
    // 需要填微信小程序相关参数，下面会有步骤
    "port": 8001,
    // 小程序后端工作端口
    "targets": [1234567],
    // 有新的申请需要审批时推送消息的qq群（一般是队长团群）
    "punch": {
      "punchWifiList": {
        "签到地点A": ["附近WIFI BSSID", "附近WIFI BSSID", "附近WIFI BSSID"],
        "签到地点B": ["附近WIFI BSSID", "附近WIFI BSSID", "附近WIFI BSSID"]
      },
      // 设置签到地点及bssid
      "targets": [1234567]
      // 每天晚上23点自动推送签到情况的群聊
    }
  }
}
```