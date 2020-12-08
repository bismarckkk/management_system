import pymysql
import ujson
import os


head = '''version: '2'
services:
'''

httpd = '''  httpd:
    image: httpd
    volumes:
    - __httpd_conf__:/usr/local/apache2/conf
    - __httpd_static__:/usr/local/apache2/htdocs
    network_mode: "host"
    container_name:
      httpd
'''

web = '''  web:
    image: registry.cn-hangzhou.aliyuncs.com/bismarckkk/management_web:1.0
    ports:
    - __web_port__:__web_port__
    volumes:
    - __config__:/code/config
    container_name:
      web
'''

wx = '''  wx:
    image: registry.cn-hangzhou.aliyuncs.com/bismarckkk/management_backend:1.0
    ports:
      - __wx_port__:__wx_port__
    volumes:
      - __config__:/code/config
    container_name:
      wx_backend
'''

webhook = '''  webhook:
    image: registry.cn-hangzhou.aliyuncs.com/bismarckkk/webhook:1.0
    ports:
      - __webhook_port__:__webhook_port__
    volumes:
      - __config__:/code/config
    container_name:
      webhook
'''


if __name__ == '__main__':
    f = open('settings.json', 'r')
    settings = ujson.loads(f.read())
    f.close()

    path = os.getcwd()

    httpd = httpd.replace('__httpd_conf__', str(os.path.join(path, 'conf')))
    httpd = httpd.replace('__httpd_static__', str(os.path.join(path, 'static')))
    httpd = httpd.replace('__out_http__', str(settings['httpd']['http_port']))
    httpd = httpd.replace('__out_https__', str(settings['httpd']['https_port']))

    docker = head + httpd
    if settings['web']['enable']:
        web = web.replace('__web_port__', str(settings['web']['port']))
        web = web.replace('__config__', str(path))
        docker += web
    if settings['wx_backend']['enable']:
        wx = wx.replace('__wx_port__', str(settings['wx_backend']['port']))
        wx = wx.replace('__config__', str(path))
        docker += wx
    if settings['webhook']['enable']:
        webhook = webhook.replace('__webhook_port__', str(settings['webhook']['port']))
        webhook = webhook.replace('__config__', str(path))
        docker += webhook

    f = open('docker-compose.yaml', 'w')
    f.write(docker)
    f.close()
    print("docker-compose.yaml写入成功")

    conn = pymysql.connect(host=settings['mysql']['host'], user=settings['mysql']['user'],
                           password=settings['mysql']['password'])
    sql = "CREATE DATABASE IF NOT EXISTS %s" % settings['mysql']['db']
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.close()

    conn = pymysql.connect(settings['mysql']['host'], settings['mysql']['user'],
                           settings['mysql']['password'], settings['mysql']['db'])
    cursor = conn.cursor()
    sql1 = '''CREATE TABLE `logs` (
  `id` int(255) NOT NULL,
  `time` text NOT NULL,
  `openid` text NOT NULL,
  `operation` text NOT NULL,
  `object` int(255) DEFAULT NULL,
  `name` text,
  `num` int(11) DEFAULT NULL,
  `do` text,
  `verify` int(255) DEFAULT NULL,
  `wis` text,
  `approver` text,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
    sql2 = '''CREATE TABLE `main` (
  `id` int(6) NOT NULL,
  `name` text NOT NULL,
  `total` int(11) NOT NULL,
  `useable` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
    sql3 = '''CREATE TABLE `members` (
  `openid` text NOT NULL,
  `name` text NOT NULL,
  `admin` int(6) NOT NULL,
  `stu_id` text NOT NULL,
  PRIMARY KEY (`openid`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
    sql4 = '''CREATE TABLE `object` (
  `id` int(10) NOT NULL,
  `father` int(255) NOT NULL,
  `useable` int(2) NOT NULL,
  `wis` text NOT NULL,
  `do` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
    sql5 = '''CREATE TABLE `punch` (
  `id` int(255) NOT NULL,
  `week` text,
  `time` text,
  `openid` text,
  `name` text,
  `location` text,
  `clas` text,
  `worktime` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
    sql6 = '''CREATE TABLE `random` (
  `student_id` varchar(255) NOT NULL,
  `name` text NOT NULL,
  `time` text NOT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
    sql7 = '''INSERT INTO logs(`id`,
 `time`, `openid`, `operation`, `object`,
 `name`, `do`, `verify`, `approver`)
 VALUES (0, '0000', '0000', 'addc', 100000,
 'test', 'test', 1, 'system')'''
    sql8 = '''INSERT INTO main(`id`,
 `name`, `total`, `useable`)
 VALUES (100000, 'test', 0, 0)'''
    sql9 = '''INSERT INTO punch(`id`)
 VALUES (0)'''
    cursor.execute(sql1)
    cursor.execute(sql2)
    cursor.execute(sql3)
    cursor.execute(sql4)
    cursor.execute(sql5)
    cursor.execute(sql6)
    cursor.execute(sql7)
    cursor.execute(sql8)
    cursor.execute(sql9)

    conn.close()

    print('数据库初始化成功')
