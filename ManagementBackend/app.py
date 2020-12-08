from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import redirect
from flask import abort
from flask import url_for
from urllib import parse
import time
import mysql
import requests
import ujson
import traceback
import re
import urllib
import datetime
from auth import verify_code_m
import mirai
import getopt
import sys
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
vc = verify_code_m()


@app.route('/getUserInfo')
def getUserInfo():
    c = request.args.get('code')
    if c is None or c == '':
        abort(401)
    p = {
        'appid': wxid,
        'secret': wxkey,
        'js_code': c,
        'grant_type': 'authorization_code'
    }
    r = requests.get("https://api.weixin.qq.com/sns/jscode2session", params=p)
    rr = ujson.loads(r.text)
    if rr['openid'] == request.args.get('openid'):
        key = vc.v_code['openid']
    else:
        key = vc.new_code(rr['openid'])
    u = sql.fetchone('members', 'openid', str(rr['openid']))
    if u is None:
        u = 0
    elif u[2] != 0:
        u = 2
    else:
        u = 1
    r = {
        'openid': rr['openid'],
        'key': key,
        'u': u
    }
    return ujson.dumps(r)


@app.route('/register/submit')
def submit():
    voidc = ["'", '"', '\\', '<', '>', '(', ')', '.', '=']
    at = request.args.get("openid")
    if at is None:
        abort(403)
    if not vc.is_code(at, request.args.get("key")):
        abort(401)
    info = {'id': sql.getall('logs')[-1][0] + 1,
            'time': "%s" % (datetime.datetime.now()),
            'openid': at,
            'operation': 'register',
            'object': request.args.get('st'),
            'name': request.args.get('re'),
            'verify': 0
            }
    for sstr in [info['object'], info['name']]:
        if sstr != info['openid']:
            for ccc in voidc:
                if ccc in str(sstr) or len(str(sstr)) == 0 or len(str(sstr)) > 15:
                    abort(401)
    try:
        sql.insert('logs', info)
        sql.commit()
    except:
        abort(402)
    else:
        return "success"


@app.route('/object')
def getObject():
    at = request.args.get("openid")
    if not vc.is_code(at, request.args.get("key")):
        abort(401)
    id = request.args.get('id')
    if id is None:
        abort(403)
    r = list(sql.fetchone('object', 'id', int(id)))
    if r is None:
        abort(403)
    r[1] = sql.fetchone('main', 'id', r[1])[1]
    u = r[2]
    if r[2] == 0:
        r[2] = '使用中'
    elif r[2] == 1:
        r[2] = '可用'
    elif r[2] == 2:
        r[2] = '维修中'
    elif r[2] == 3:
        r[2] = '已报废'
    else:
        r[2] = '申请中'
    r = {
        'id': str(r[0]),
        'father': r[1],
        'usable': str(r[2]),
        'where': r[3],
        'remark': r[4],
        'un': u
    }
    return ujson.dumps(r)


def is_admin(openid):
    admin = sql.fetchone('members', 'openid', str(openid))
    if admin is None:
        abort(401)
    else:
        if admin[2] != 0:
            return True
        else:
            return False


def is_vaild(sstr):
    voidc = ["'", '"', '\\', '<', '>', '(', ')', '.', '=']
    for ccc in voidc:
        if ccc in str(sstr):
            abort(400)


@app.route('/operation')
def op():
    at = request.args.get("openid")
    if not vc.is_code(at, request.args.get("key")):
        abort(401)
    id = sql.getall('logs')[-1][0] + 1
    print(id)
    info = {'id': id,
            'time': "%s" % (datetime.datetime.now()),
            'openid': request.args.get('openid'),
            'operation': request.args.get('op'),
            'object': request.args.get('oid'),
            'name': request.args.get('name'),
            'num': request.args.get('num'),
            'do': request.args.get('do'),
            'wis': request.args.get('where'),
            'verify': 0
            }
    if info['operation'] == 'use':
        info['wis'] = request.args.get('pwhere')
    if info['do'] == '':
        info['do'] = None
    is_vaild(info['name'])
    is_vaild(info['do'])
    print(is_admin(info['openid']))
    if is_admin(info['openid']):
        info['verify'] = 1
        info['approver'] = sql.fetchone('members', 'openid', info['openid'])[1]
        sql.insert('logs', info)
        msg = ''
        if info['operation'] == 'in':
            sql.update('object', ['useable', 'id'], [1, info['object']])
            sql.update('object', ['wis', 'id'], [info['wis'], info['object']])
            sql.update('object', ['do', 'id'], [info['do'], info['object']])
            use = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[3] + 1
            sql.update('main', ['useable', 'id'], [use, int(str(info['object'])[:6])])
            name = sql.fetchone('members', 'openid', info['openid'])[1]
            obj = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[1]
            msg = "%s 还入 %s %s 到 %s 仓库" % (name, obj, str(info['object']), info['wis'])
        elif info['operation'] == 'out':
            sql.update('object', ['useable', 'id'], [0, info['object']])
            name = sql.fetchone('members', 'openid', info['openid'])[1]
            sql.update('object', ['wis', 'id'], [name, info['object']])
            sql.update('object', ['do', 'id'], [info['do'], info['object']])
            name = sql.fetchone('members', 'openid', info['openid'])[1]
            obj = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[1]
            msg = "%s 借出 %s %s" % (name, obj, str(info['object']))
        elif info['operation'] == 'use':
            sql.update('object', ['useable', 'id'], [0, info['object']])
            sql.update('object', ['wis', 'id'], [info['wis'], info['object']])
            sql.update('object', ['do', 'id'], [info['do'], info['object']])
            name = sql.fetchone('members', 'openid', info['openid'])[1]
            obj = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[1]
            msg = "%s 因 %s 项目使用 %s %s" % (name, info['wis'], obj, str(info['object']))
        elif info['operation'] == 'cre':
            sql.update('object', ['useable', 'id'], [1, info['object']])
            sql.update('object', ['wis', 'id'], [info['wis'], info['object']])
            sql.update('object', ['do', 'id'], [info['do'], info['object']])
            use = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[3] + 1
            sql.update('main', ['useable', 'id'], [use, int(str(info['object'])[:6])])
        elif info['operation'] == 'cbf':
            sql.update('object', ['useable', 'id'], [1, info['object']])
            use = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[3] + 1
            sql.update('main', ['useable', 'id'], [use, int(str(info['object'])[:6])])
        elif info['operation'] == 'bf':
            sql.update('object', ['useable', 'id'], [3, info['object']])
            use = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[3] - 1
            sql.update('main', ['useable', 'id'], [use, int(str(info['object'])[:6])])
            sql.update('object', ['do', 'id'], [info['do'], info['object']])
        elif info['operation'] == 're':
            sql.update('object', ['useable', 'id'], [2, info['object']])
            use = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[3] - 1
            sql.update('main', ['useable', 'id'], [use, int(str(info['object'])[:6])])
            sql.update('object', ['do', 'id'], [info['do'], info['object']])
            sql.update('object', ['wis', 'id'], ['送修中', info['object']])
        elif info['operation'] == 'addc':
            last = sql.getall('main')[-1][0]
            inf = {
                'id': last + 1,
                'name': info['name'],
                'total': 0,
                'useable': 0
            }
            sql.insert('main', inf)
        elif info['operation'] == 'addo':
            i = sql.fetchone('main', 'id', info['object'])
            sql.update('main', ['total', 'id'], [i[2] + int(info['num']), info['object']])
            sql.update('main', ['useable', 'id'], [i[3] + int(info['num']), info['object']])
            i = sql.fetchall('object', 'father', info['object'])
            if i != ():
                i = i[-1][0] + 1
            else:
                i = int(info['object']) * 100 + 1
            for j in range(int(info['num'])):
                ins = {
                    'id': i + j,
                    'father': int(info['object']),
                    'useable': 1,
                    'wis': info['wis'],
                    'do': info['do']
                }
                sql.insert('object', ins)
        elif info['operation'] == 'leave':
            info2 = {'id': sql.getall('punch')[-1][0] + 1,
                     'time': "%s" % (datetime.datetime.now()),
                     'week': str(time.strftime('%W')),
                     'openid': info['openid'],
                     'name': sql.fetchone('members', 'openid', info['openid'])[1],
                     'clas': 'leave',
                     'worktime': info['num']
                     }
            sql.insert('punch', info2)
            name = sql.fetchone('members', 'openid', info['openid'])[1]
            msg = "%s 因 %s 希望请假 %s 天" % (name, info['do'], str(info['num']))
        else:
            abort(400)
        sql.commit()
        if msg != '':
            mirai.sendQQMessage(msg + '，已自动审批通过', url, authKey, bot, targets)
        return 'success'
    else:
        msg = ''
        if info['operation'] == 'in':
            name = sql.fetchone('members', 'openid', info['openid'])[1]
            obj = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[1]
            msg = "%s 还入 %s %s 到 %s 仓库" % (name, obj, str(info['object']), info['wis'])
        elif info['operation'] == 'out':
            name = sql.fetchone('members', 'openid', info['openid'])[1]
            obj = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[1]
            msg = "%s 借出 %s %s" % (name, obj, str(info['object']))
        elif info['operation'] == 'use':
            name = sql.fetchone('members', 'openid', info['openid'])[1]
            obj = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[1]
            msg = "%s 因 %s 项目使用 %s %s" % (name, info['wis'], obj, str(info['object']))
        elif info['operation'] == 'leave':
            name = sql.fetchone('members', 'openid', info['openid'])[1]
            msg = "%s 因 %s 希望请假 %s 天" % (name, info['do'], str(info['num']))
        if info['operation'] == 'out' or info['operation'] == 'use':
            use = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[3] - 1
            sql.update('main', ['useable', 'id'], [use, int(str(info['object'])[:6])])
            sql.update('object', ['useable', 'id'], [4, info['object']])
        sql.insert('logs', info)
        sql.commit()
        if msg != '':
            msg += '，请在 https://rm.bismarck.xyz 审批'
            mirai.sendQQMessage(msg, url, authKey, bot, targets)
        return 'wait'


@app.route('/searchList')
def searchList():
    at = request.args.get("openid")
    if not vc.is_code(at, request.args.get("key")):
        abort(401)
    l = sql.getall('main')
    key_words = []
    for it in l:
        if it[0] is not None and it[0] != 0:
            key_words.append(str(it[0]))
        if it[1] is not None and it[1] != 0:
            key_words.append(str(it[1]))
    return ujson.dumps(key_words)


@app.route('/getList')
def getList():
    at = request.args.get("openid")
    if not vc.is_code(at, request.args.get("key")):
        abort(401)
    if request.args.get('k') == 'w':
        info = sql.getall('main')
        r = []
        for it in info:
            inf = {'id': it[0], 'name': it[1], 'total': it[2], 'use': it[3]}
            r.append(inf)
        r = ujson.dumps(r)
        return r
    elif request.args.get('k') == 'o':
        father = request.args.get('f')
        info = sql.fetchall('object', 'father', int(father))
        r = []
        for it in info:
            inf = {'id': it[0]}
            if it[2] == 1:
                inf['use'] = '可用'
            elif it[2] == 0:
                inf['use'] = '使用中'
            elif it[2] == 2:
                inf['use'] = '维修中'
            elif it[2] == 3:
                inf['use'] = '已报废'
            else:
                inf['use'] = '申请中'
            inf['where'] = it[3]
            r.append(inf)
        r = ujson.dumps({sql.fetchone('main', 'id', int(father))[1]: r})
        return r
    elif request.args.get('k') == 's':
        st = urllib.parse.unquote(request.args.get('t'))
        ob = sql.getall('object')
        info = []
        for obj in ob:
            for it in obj:
                if str(it).find(st) != -1 and obj not in info:
                    info.append(obj)
        ob = sql.getall('main')
        for name in ob:
            if str(name[1]).find(st) != -1:
                d = sql.fetchall('object', 'father', name[0])
                for it in d:
                    if it not in info:
                        info.append(it)
        rr = {}
        for it in info:
            name = sql.fetchone('main', 'id', it[1])[1]
            if name not in rr.keys():
                rr[name] = []
        for it in info:
            inf = {'id': it[0]}
            if it[2] == 1:
                inf['use'] = '可用'
            elif it[2] == 0:
                inf['use'] = '使用中'
            elif it[2] == 2:
                inf['use'] = '维修中'
            elif it[2] == 3:
                inf['use'] = '已报废'
            else:
                inf['use'] = '申请中'
            inf['where'] = it[3]
            rr[sql.fetchone('main', 'id', it[1])[1]].append(inf)
        r = ujson.dumps(rr)
        return r
    else:
        abort(400)


@app.route('/backgroundLoad')
def backgroundLoad():
    if request.args.get('appid') != 'wxb5b986324fab12a9':
        abort(400)
    openid = request.args.get('token')
    if openid is None:
        abort(401)
    u = sql.fetchone('members', 'openid', openid)
    if u is None:
        u = 0
    elif u[2] != 0:
        u = 2
    else:
        u = 1
    info = sql.getall('main')
    r = []
    key_words = []
    for it in info:
        inf = {'id': it[0], 'name': it[1], 'total': it[2], 'use': it[3]}
        r.append(inf)
        if it[0] is not None and it[0] != 0:
            key_words.append(str(it[0]))
        if it[1] is not None and it[1] != 0:
            key_words.append(str(it[1]))
    rr = ujson.dumps(r)
    r = {
        'openid': openid,
        'key': vc.new_code(openid),
        'u': u,
        'mlist': rr,
        'words': key_words
    }
    return ujson.dumps(r)


@app.route('/punch')
def punch():
    at = request.args.get("openid")
    if not vc.is_code(at, request.args.get("key")):
        abort(401)
    id = sql.getall('punch')[-1][0] + 1
    info = {'id': id,
            'time': "%s" % (datetime.datetime.now()),
            'openid': at,
            'name': sql.fetchone('members', 'openid', at)[1]}
    sql.insert('punch', info)
    sql.commit()
    return "success"


@app.route('/getPunchWifiList')
def getPunchList():
    at = request.args.get("openid")
    if not vc.is_code(at, request.args.get("key")):
        abort(401)
    r = ['50:fa:84:85:0c:1b', '80:f6:2e:12:61:90', '40:b4:f0:aa:60:04']
    return ujson.dumps(r)


@app.route('/logs')
def getLog():
    at = request.args.get("openid")
    if not vc.is_code(at, request.args.get("key")):
        abort(401)
    r = list(sql.fetchall('logs', 'openid', at))
    for i in range(len(r)):
        info = {
            'id': r[i][0],
            'time': r[i][1],
            'object': r[i][4],
            'name': r[i][5],
            'wis': r[i][9],
            'do': r[i][7],
            'approver': r[i][10]
        }
        if r[i][8] == 0:
            info['verify'] = '待审批'
        elif r[i][8] == 1:
            info['verify'] = '已通过'
        elif r[i][8] == 2:
            info['verify'] = '被退回'
        if r[i][3] == 'register':
            info['operation'] = '注册'
        elif r[i][3] == 'addo':
            info['operation'] = '新增对象'
            info['name'] = sql.fetchone('main', 'id', int(info['object']))[1]
        elif r[i][3] == 'addc':
            info['operation'] = '新增物资'
        elif r[i][3] == 'leave':
            info['operation'] = '请假'
        else:
            if info['object'] is not None:
                t = sql.fetchone('main', 'id', int(info['object'] / 100))
                if t is None:
                    info['name'] = "获取错误"
                else:
                    info['name'] = t[1]
            if r[i][3] == 'in':
                info['operation'] = '还入'
            elif r[i][3] == 'out':
                info['operation'] = '借出'
            elif r[i][3] == 'use':
                info['operation'] = '使用'
            elif r[i][3] == 're':
                info['operation'] = '送修'
            elif r[i][3] == 'cre':
                info['operation'] = '送修结束'
            elif r[i][3] == 'bf':
                info['operation'] = '报废'
            elif r[i][3] == 'cbf':
                info['operation'] = '取消报废'
            elif r[i][3] == 'leave':
                info['operation'] = '请假'
        r[i] = info
    if len(r) > 25:
        r = r[:-25]
    return ujson.dumps(r[::-1])


@app.route('/punchNew', methods=['POST'])
def punchNew():
    print(request.json)
    data = request.json
    at = data["openid"]
    if not vc.is_code(at, data["key"]):
        abort(401)
    listt = {}
    for (location, wifi) in wifiList.items():
        listt[location] = len(set(wifi).intersection(set(data['wifi'])))
    listt = sorted(listt.items(), key=lambda kv: (kv[1], kv[0]))[-1]
    re = {'status': 'false'}
    if listt[1] != 0:
        re['status'] = 'true'
        re['location'] = listt[0]
    else:
        return re
    nlist = sql.fetchall('punch', 'week', str(time.strftime('%W')))
    st = True
    for it in nlist:
        if it[3] == at:
            timeIt = datetime.datetime.strptime(it[2], '%Y-%m-%d %H:%M:%S.%f')
            if timeIt.date() == datetime.datetime.today().date():
                st = False
    if st:
        info = {'id': sql.getall('punch')[-1][0] + 1,
                'time': "%s" % (datetime.datetime.now()),
                'week': str(time.strftime('%W')),
                'openid': at,
                'name': sql.fetchone('members', 'openid', at)[1],
                'location': str(listt[0]),
                'clas': 'punch'
                }
        sql.insert('punch', info)
        sql.commit()
    else:
        re['status'] = 'retry'
    return ujson.dumps(re)


@app.route('/punchQuit', methods=['POST'])
def punchQuitNew():
    print(request.json)
    data = request.json
    at = data["openid"]
    if not vc.is_code(at, data["key"]):
        abort(401)
    listt = {}
    for (location, wifi) in wifiList.items():
        listt[location] = len(set(wifi).intersection(set(data['wifi'])))
    listt = sorted(listt.items(), key=lambda kv: (kv[1], kv[0]))[-1]
    re = {'status': 'false'}
    if listt[1] != 0:
        re['status'] = 'true'
        re['location'] = listt[0]
    else:
        return re
    nlist = sql.fetchall('punch', 'week', str(time.strftime('%W')))
    punchOk = False
    noQuit = True
    quitId = 0
    punchTime = None
    for it in nlist:
        if it[3] == at:
            timeIt = datetime.datetime.strptime(it[2], '%Y-%m-%d %H:%M:%S.%f')
            if timeIt.date() == datetime.datetime.today().date():
                if it[6] == 'punch':
                    punchOk = True
                    punchTime = timeIt
                else:
                    noQuit = False
                    quitId = it[0]
    if punchOk:
        if noQuit:
            info = {'id': sql.getall('punch')[-1][0] + 1,
                    'time': "%s" % (datetime.datetime.now()),
                    'week': str(time.strftime('%W')),
                    'openid': at,
                    'name': sql.fetchone('members', 'openid', at)[1],
                    'location': str(listt[0]),
                    'clas': 'quit',
                    'worktime': str(round((datetime.datetime.now() - punchTime).seconds / 3600, 2))
                    }
            sql.insert('punch', info)
            sql.commit()
        else:
            sql.update('punch', ['time', 'id'], ["%s" % (datetime.datetime.now()), quitId])
            sql.update('punch', ['location', 'id'], [str(listt[0]), quitId])
            sql.update('punch', ['worktime', 'id'], [str(round((datetime.datetime.now() - punchTime).seconds / 3600, 2)), quitId])
            sql.commit()
    elif not punchOk:
        re['status'] = 'noPunch'
    else:
        re['status'] = 'retry'
    return ujson.dumps(re)


def look4punch():
    nlist = sql.fetchall('punch', 'week', str(time.strftime('%W')))
    worktime = {
        '左清宇': '未签到',
        '段政': '未签到',
        '邱励寒': '未签到',
        '李晓童': '未签到',
        '李新鹏': '未签到',
        '张健烨': '未签到',
        '廖乐成': '未签到',
        '孙淼': '未签到',
        '张皓程': '未签到',
        '杨云集': '未签到',
        '张澳淋': '未签到',
        '刘子逸': '未签到',
        '池烨恒': '未签到',
        '王泽诚': '未签到',
        '项安黎': '未签到',
        '伍雨童': '未签到',
        '陈和灏': '未签到',
        '陈宏昱': '未签到',
        '蔡哲豪': '未签到',
        '申鑫冉': '未签到',
        '彭施聪': '未签到',
        '郑皓振': '未签到',
        '王威奇': '未签到',
        '樊俊伟': '未签到',
        '叶宇林': '未签到',
        '肖佳妮': '未签到'
    }
    for it in nlist:
        timeIt = datetime.datetime.strptime(it[2], '%Y-%m-%d %H:%M:%S.%f')
        if timeIt.date() == datetime.datetime.today().date():
            name = sql.fetchone('members', 'openid', it[3])[1]
            if it[6] == 'punch':
                worktime[name] = '已签到'
            elif it[6] == 'quit':
                worktime[name] = str(it[7])
    ss = '今日签到状况：\n'
    for key, value in sorted(worktime.items(), key = lambda kv:(kv[1], kv[0])):
        ss += '%s：%s\n' % (key, value)
    ss = ss[:-1]
    mirai.sendQQMessage(ss, url, authKey, bot, targets2)


def remindQuit():
    mirai.sendAtAllQQMessage("即将结算工时，请及时签退", url, authKey, bot, targets2)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "s:", ["settings="])
    for opt, arg in opts:
        if opt in ("-s", "--settings"):
            file = arg
    f = open(file, 'r')
    settings = ujson.loads(f.read())
    f.close()

    url = settings['mirai']['url']
    authKey = settings['mirai']['authkey']
    bot = settings['mirai']['qq']
    targets = settings['wx_backend']['targets']
    targets2 = settings['wx_backend']['punch']['targets']
    wxkey = settings['wx_backend']['wx_miniprogram']['wxkey']
    wxid = settings['wx_backend']['wx_miniprogram']['wxid']
    port = settings['wx_backend']['port']
    sql = mysql.MySql(settings['mysql'])
    wifiList = settings['wx_backend']['punch']['punchWifiList']

    scheduler = BackgroundScheduler()
    scheduler.add_job(remindQuit, 'cron', hour='22', minute='50')
    scheduler.add_job(look4punch, 'cron', hour='23')
    scheduler.start()

    app.run(port=port, host='0.0.0.0')
