from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import redirect
from flask import abort
from flask import url_for
from urllib import parse
from pylibdmtx.pylibdmtx import decode
from PIL import Image
from io import BytesIO
import time
import mysql
import requests
import ujson
import traceback
import re
import verify_code
import urllib
import datetime
import base64
import mirai
import getopt
import sys

app = Flask(__name__)
state = verify_code.verify_code_m()


@app.route('/')
def hello_world():
    at = request.cookies.get("access_token")
    if at is None:
        res = abort(401)
        res.set_cookie('last_link', request.url)
        return res
    openid = get_openid(at, '/')
    try:
        info = sql.fetchone('members', 'openid', openid)
    except:
        abort(401)
    else:
        if info is None:
            return redirect('/register')
        admin = False
        if info[2] != 0:
            admin = True
        name = info[1]
        return render_template('home.html', web_title=web_title, web_subtitle=web_subtitle, name=name, admin=admin)



def get_openid(at, link):
    r = requests.get("https://graph.qq.com/oauth2.0/me?access_token=" + str(at))
    r = re.findall(r"\((.+?)\)", r.text)[0]
    s = ujson.loads(r)
    if 'openid' in s.keys():
        return s['openid']
    else:
        res = Response(abort(401))
        res.set_cookie('last_link', link)
        return res


def is_admin(at, link):
    openid = get_openid(at, link)
    admin = sql.fetchone('members', 'openid', str(openid))
    if admin is None:
        res = Response(abort(401))
        res.set_cookie('last_link', link)
        return res
    else:
        if admin[2] != 0:
            return True
        else:
            return False


def is_member(at, link):
    openid = get_openid(at, link)
    admin = sql.fetchone('members', 'openid', str(openid))
    if admin is None or admin == []:
        #res = Response(abort(401))
        #res.set_cookie('last_link', link)
        return False
    else:
        return True


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


@app.route('/login')
def login():
    global appid, state
    s = state.new_code()
    return redirect('https://graph.qq.com/oauth2.0/authorize?'
                    'response_type=code&client_id=' + appid + '&'
                    'redirect_uri=' + website + '/callback&'
                    'state=' + s)


@app.route('/callback')
def callback():
    global appid, appkey
    code = request.args.get('code')
    if code is not None:
        r = request.args.get('usercancel')
        ss = request.args.get('state')
        if (r != 0 and r is not None) or state.is_not_code(ss):
            abort(401)
        r = requests.get("https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&"
                         "client_id=" + appid + "&client_secret=" + appkey + "&code=" + code +
                         "&redirect_uri=" + website + "/callback")
        p = parse.parse_qs(r.text)
        if 'access_token' in p.keys():
            if is_member(p['access_token'][0], ''):
                link = request.cookies.get("last_link")
                t = int(p['expires_in'][0])
                if link is None:
                    res = Response(render_template('goto.html', web_title=web_title, web_subtitle=web_subtitle, page_body='无法找到上一级页面，即将返回首页', page_herf=website + ''))
                else:
                    res = Response(render_template('goto.html', web_title=web_title, web_subtitle=web_subtitle, page_body='正在跳转到您上一个访问的页面', page_herf=website + '' + link))
            else:
                res = Response(
                    render_template('goto.html', web_title=web_title, web_subtitle=web_subtitle, page_body='正在跳转到您上一个访问的页面', page_herf=website + '/register'))
            res.set_cookie(key='access_token', value=p['access_token'][0], expires=time.time() + t)
            return res
    else:
        abort(400)


@app.route('/register')
def register():
    at = request.cookies.get("access_token")
    if at is None:
        res = redirect('login')
        res.set_cookie('last_link', url_for('register'))
        return res
    if is_member(at, '/'):
        link = request.cookies.get("last_link")
        if link is None:
            res = Response(render_template('goto.html', web_title=web_title, web_subtitle=web_subtitle, page_body='无法找到上一级页面，即将返回首页', page_herf=website + ''))
        else:
            res = Response(render_template('goto.html', web_title=web_title, web_subtitle=web_subtitle, page_body='正在跳转到您上一个访问的页面', page_herf=website + '' + link))
        return res
    else:
        return render_template('register.html')


@app.route('/register/submit', methods=['POST'])
def submit():
    voidc = ["'", '"', '\\', '<', '>', '(', ')', '.', '=']
    at = request.cookies.get("access_token")
    if at is None:
        res = redirect(url_for('login'))
        res.set_cookie('last_link', request.url)
        return res
    info = {'id': sql.getall('logs')[-1][0] + 1,
            'time': "%s" % (datetime.datetime.now()),
            'openid': get_openid(at, ''),
            'operation': 'register',
            'object': request.form.get('student_number'),
            'name': request.form.get('real_name'),
            'verify': 0
            }
    for sstr in [info['object'], info['name']]:
        if sstr != info['openid']:
            for ccc in voidc:
                if ccc in str(sstr) or len(str(sstr)) == 0 or len(str(sstr)) > 15:
                    return render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='参数非法',
                                           page_body='parameters error:\n"' + str(sstr)
                                           + '" is not vaild')
    try:
        sql.insert('logs', info)
        sql.commit()
    except:
        return render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='未知错误', page_body='Unexpected error:' + traceback.format_exc())
    else:
        return render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='注册完成', page_body='注册完成\n请耐心等待审核通过')


@app.route('/get_object')
def get_list():
    if request.args.get('k') == 'w':
        info = sql.getall('main')
        r = {'物资ID': [], '物资全名': [], '总数': [], '可使用': []}
        for it in info:
            r['物资ID'].append(it[0])
            r['物资全名'].append(it[1])
            r['总数'].append(it[2])
            r['可使用'].append(it[3])
        r = ujson.dumps(r)
        return r
    elif request.args.get('k') == 'o':
        father = request.args.get('f')
        info = sql.fetchall('object', 'father', int(father))
        r = {'对象ID': [], '是否可用': [], '当前位置': [], '备注': []}
        for it in info:
            r['对象ID'].append(it[0])
            if it[2] == 1:
                r['是否可用'].append('是')
            elif it[2] == 0:
                r['是否可用'].append('已借出')
            elif it[2] == 2:
                r['是否可用'].append('维修中')
            elif it[2] == 3:
                r['是否可用'].append('已报废')
            else:
                r['是否可用'].append('申请中')
            r['当前位置'].append(it[3])
            if it[4] is None or it[4] == '' or it[4] == 'None':
                r['备注'].append('无')
            elif len(it[4]) > 20:
                r['备注'].append(it[4][:20] + '...')
            else:
                r['备注'].append(it[4])
        r = ujson.dumps(r)
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
        r = {'对象ID': [], '对象全名': [], '是否可用': [], '当前位置': [], '备注': []}
        for it in info:
            r['对象ID'].append(it[0])
            r['对象全名'].append(sql.fetchone('main', 'id', it[1])[1])
            if it[2] == 1:
                r['是否可用'].append('是')
            elif it[2] == 0:
                r['是否可用'].append('已借出')
            elif it[2] == 2:
                r['是否可用'].append('维修中')
            elif it[2] == 3:
                r['是否可用'].append('已报废')
            else:
                r['是否可用'].append('申请中')
            r['当前位置'].append(it[3])
            if it[4] is None:
                r['备注'].append('无')
            elif len(it[4]) > 20:
                r['备注'].append(it[4][:20] + '...')
            else:
                r['备注'].append(it[4])
        r = ujson.dumps(r)
        return r
    else:
        abort(400)


@app.route('/object')
def obj():
    id = request.args.get('id')
    if id is None:
        abort(401)
    if id == 'False':
        abort(400)
    elif int(id) > 999999:
        r = list(sql.fetchone('object', 'id', int(id)))
        r[1] = sql.fetchone('main', 'id', r[1])[1]
        if r is None:
            return render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='未找到该物资', page_body='未找到该物资')
        #r.append(sql.fetchone('main', 'id', r[1])[1])
        return render_template('object.html', web_title=web_title, web_subtitle=web_subtitle, m=r)
    else:
        return redirect(url_for('show_list', k='o', f=id))


@app.route('/list')
def show_list():
    at = request.cookies.get("access_token")
    if at is None:
        res = redirect(url_for('login'))
        res.set_cookie('last_link', request.url)
        return res
    if not is_member(at, ''):
        abort(401)
    admin = is_admin(at, request.url)
    if request.args.get('k') == 'o':
        ma = sql.fetchone('main', 'id', request.args.get('f'))
        return render_template('list.html', web_title=web_title, web_subtitle=web_subtitle, admin=admin, m=ma, page_title=ma[1])
    elif request.args.get('k') == 'w':
        return render_template('list.html', web_title=web_title, web_subtitle=web_subtitle, admin=admin, t='物资总览', page_title='物资总览')
    elif request.args.get('k') == 's':
        t = request.args.get('t')
        return render_template('list.html', web_title=web_title, web_subtitle=web_subtitle, t='搜索结果 - ' + t, page_title='搜索结果 - ' + t)
    else:
        abort(400)


@app.route('/operation')
def operation():
    id = request.args.get('id')
    at = request.cookies.get("access_token")
    if at is None:
        res = redirect(url_for('login'))
        res.set_cookie('last_link', request.url)
        return
    if not is_member(at, ''):
        abort(401)
    openid = get_openid(at, request.url)
    info = sql.fetchone('members', 'openid', openid)
    if info[2] != 0:
        admin = True
    else:
        admin = False
    obj = False
    if id is None:
        return render_template('operation.html', web_title=web_title, web_subtitle=web_subtitle, obj=False, admin=admin, useable=4)
    elif int(id) > 999999:
        obj = True
        usable = sql.fetchone('object', 'id', int(id))[2]
        return render_template('operation.html', web_title=web_title, web_subtitle=web_subtitle, obj=obj, admin=admin, useable=usable)
    else:
        return render_template('operation.html', web_title=web_title, web_subtitle=web_subtitle, obj=obj, admin=admin, useable=0)


def is_vaild(sstr):
    voidc = ["'", '"', '\\', '<', '>', '(', ')', '.', '=']
    for ccc in voidc:
        if ccc in str(sstr):
            return render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='参数非法',
                                   page_body='parameters error:\n"' + str(sstr)
                                             + '" is not vaild')


@app.route('/operation/submit', methods=['POST'])
def o_submit():
    at = request.cookies.get("access_token")
    if at is None:
        res = redirect(url_for('login'))
        res.set_cookie('last_link', request.url)
        return res
    if not is_member(at, ''):
        abort(401)
    id = sql.getall('logs')[-1][0] + 1
    info = {'id': id,
            'time': "%s" % (datetime.datetime.now()),
            'openid': get_openid(at, ''),
            'operation': request.form.get('op'),
            'object': request.form.get('oid'),
            'name': request.form.get('name'),
            'num': request.form.get('num'),
            'do': request.form.get('do'),
            'wis': request.form.get('where'),
            'verify': 0
            }
    if info['operation'] == 'use':
        info['wis'] = request.form.get('pwhere')
    if info['do'] == '':
        info['do'] = None
    is_vaild(info['name'])
    is_vaild(info['do'])
    if is_admin(at, ''):
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
        else:
            abort(400)
        sql.commit()
        if msg != '':
            mirai.sendQQMessage(msg + '，已自动审批通过', url, authKey, bot, targets)
        return render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='操作成功', page_body='操作成功')
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
            msg += '，请在 ' + website + ' 审批'
            mirai.sendQQMessage(msg, url, authKey, bot, targets)
        return render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='申请已提交', page_body='申请已提交\n正在等待管理员通过')


def ver(at, k, id, mode=0):
    if at is None:
        res = redirect(url_for('login'))
        res.set_cookie('last_link', request.url)
        return res
    is_admin(at, '/verify', web_title=web_title, web_subtitle=web_subtitle, page_title='待审批列表')
    if id is None:
        return render_template('verify.html')
    else:
        id = int(id)
        r = sql.fetchone('logs', 'id', id)
        info = {
            'id': id,
            'time': r[1],
            'openid': r[2],
            'operation': r[3],
            'object': r[4],
            'name': r[5],
            'num': r[6],
            'do': r[7],
            'verify': 1,
            'wis': r[9],
        }
        if k == 'y' or mode == 1:
            name = sql.fetchone('members', 'openid', get_openid(at, ''))[1]
            if info['operation'] == 'in':
                sql.update('logs', ['verify', 'id'], [1, id])
                sql.update('logs', ['approver', 'id'], [name, info['object']])
                sql.update('object', ['useable', 'id'], [1, info['object']])
                sql.update('object', ['wis', 'id'], [info['wis'], info['object']])
                sql.update('object', ['do', 'id'], [info['do'], info['object']])
            elif info['operation'] == 'use' or info['operation'] == 'out':
                if int(sql.fetchone('object', 'id', info['object'])[2]) == 1 or int(sql.fetchone('object', 'id', info['object'])[2]) == 4:
                    if info['operation'] == 'out':
                        sql.update('logs', ['verify', 'id'], [1, id])
                        sql.update('logs', ['approver', 'id'], [name, info['object']])
                        sql.update('object', ['useable', 'id'], [0, info['object']])
                        name = sql.fetchone('members', 'openid', info['openid'])[1]
                        sql.update('object', ['wis', 'id'], [name, info['object']])
                        sql.update('object', ['do', 'id'], [info['do'], info['object']])
                    elif info['operation'] == 'use':
                        sql.update('logs', ['verify', 'id'], [1, id])
                        sql.update('logs', ['approver', 'id'], [name, info['object']])
                        sql.update('object', ['useable', 'id'], [0, info['object']])
                        sql.update('object', ['wis', 'id'], [info['wis'], info['object']])
                        sql.update('object', ['do', 'id'], [info['do'], info['object']])
                else:
                    if mode == 0:
                        return render_template('goto.html', web_title=web_title, web_subtitle=web_subtitle, page_body='操作失败\n物品已被使用',
                                               page_herf=website + '/verify')
                    else:
                        return True
            elif info['operation'] == 'register':
                sql.update('logs', ['verify', 'id'], [1, id])
                mi = {
                    'openid': info['openid'],
                    'name': info['name'],
                    'admin': 0,
                    'stu_id': info['object']
                }
                sql.insert('members', mi)
            elif info['operation'] == 'leave':
                sql.update('logs', ['verify', 'id'], [1, id])
                info2 = {'id': sql.getall('punch')[-1][0] + 1,
                        'time': "%s" % (datetime.datetime.now()),
                        'week': str(time.strftime('%W')),
                        'openid': info['openid'],
                        'name': sql.fetchone('members', 'openid', info['openid'])[1],
                        'clas': 'leave',
                        'worktime': info['num']
                        }
                sql.insert('punch', info2)
            else:
                abort(400)
        else:
            if info['operation'] == 'out' or info['operation'] == 'use':
                use = sql.fetchone('main', 'id', int(str(info['object'])[:6]))[3] + 1
                sql.update('main', ['useable', 'id'], [use, int(str(info['object'])[:6])])
            sql.update('logs', ['verify', 'id'], [2, int(id)])
            name = sql.fetchone('members', 'openid', get_openid(at, ''))[1]
            sql.update('logs', ['approver', 'id'], [name, int(id)])
        try:
            sql.commit()
        except:
            if mode == 0:
                return render_template('goto.html', web_title=web_title, web_subtitle=web_subtitle, page_body='操作失败，异常错误\n即将返回', page_herf=website + '/verify')
            else:
                return False
        if mode == 0:
            return render_template('goto.html', web_title=web_title, web_subtitle=web_subtitle, page_body='操作成功\n即将返回', page_herf=website + '/verify')
        else:
            return True


@app.route('/verify')
def ve():
    return ver(request.cookies.get("access_token"), request.args.get('k'), request.args.get('id'))


@app.route('/verifyAll')
def vall():
    idList = sql.fetchall('logs', 'verify', 0)
    noS = 0
    for i in idList:
        try:
            if not ver(request.cookies.get("access_token"), 'y', i[0]):
                noS += 1
        except:
            noS += 1
    return render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='审批', page_body='已成功通过%i项申请  %i项通过失败  请手动返回' % (len(idList)-noS, noS))


@app.route('/verify/list')
def ve_list():
    r = sql.fetchall('logs', 'verify', 0)
    if r == ():
        return '{"暂无需要确认操作":""}'
    info = {
        'ID': [],
        '时间': [],
        '申请人': [],
        '操作类型': [],
        '操作对象': [],
        '位置': [],
        '备注': []
    }
    for it in r:
        info['ID'].append(str(it[0]))
        info['时间'].append(str(it[1]))
        if it[3] == 'in':
            info['操作类型'].append('还入')
        elif it[3] == 'use':
            info['操作类型'].append('使用')
        elif it[3] == 'register':
            info['操作类型'].append('注册')
        elif it[3] == 'leave':
            info['操作类型'].append('请假')
        else:
            info['操作类型'].append('借出')
        if it[3] == 'register':
            info['申请人'].append(sql.fetchone('logs', 'id', it[0])[5])
        else:
            info['申请人'].append(sql.fetchone('members', 'openid', it[2])[1])
        info['操作对象'].append(str(it[4]))
        info['位置'].append(str(it[9]))
        info['备注'].append(str(it[8]))
    return ujson.dumps(info)


@app.route('/search')
def search():
    l = sql.getall('main')
    key_words = []
    for it in l:
        if it[0] is not None and it[0] != 0:
            key_words.append(str(it[0]))
        if it[1] is not None and it[1] != 0:
            key_words.append(str(it[1]))
    print(ujson.dumps(key_words))
    return render_template('search.html', web_title=web_title, web_subtitle=web_subtitle, key_words=ujson.dumps(key_words))


@app.route('/whole')
def whole():
    return redirect(url_for('show_list', k='w'))


@app.route('/exit')
def exit_login():
    res = Response(render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='注销成功', page_body='注销成功'))
    res.delete_cookie('access_token')
    res.delete_cookie('last_link')
    return res


def base64_to_image(base64_str, image_path=None):
    try:
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
    except:
        print(base64_str)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    return img


@app.route('/scan', methods=['POST'])
def scan_code():
    i = base64_to_image(request.form.get('filein'))
    rate = 600 / i.size[0]
    i = i.resize((int(i.size[0] * rate), int(i.size[1] * rate)), Image.ANTIALIAS)
    i.save('1.png')
    r = decode(i)
    if len(r) != 0:
        r = r[0].data
    else:
        r = 'False'
    return r


@app.route('/random')
def random():
    if request.cookies.get("CKYF_Random_DO") is None:
        return render_template('random.html')
    else:
        return render_template('page2.html', web_title=web_title, web_subtitle=web_subtitle, page_title='抽奖', page_body='你已经参与过抽奖了哦，给别人留点机会吧')


@app.route('/random/submit', methods=['POST'])
def r_submit():
    voidc = ["'", '"', '\\', '<', '>', '(', ')', '.', '=']
    info = {'student_id': request.form.get('student_number'),
            'name': request.form.get('real_name'),
            'time': "%s" % (datetime.datetime.now())}
    for sstr in [info['student_id'], info['name']]:
        for ccc in voidc:
            if ccc in str(sstr) or len(str(sstr)) == 0 or len(str(sstr)) > 15:
                return render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='参数非法',
                                       page_body='parameters error:\n"' + str(sstr)
                                       + '" is not vaild')
    if sql.fetchone('random', 'student_id', info['student_id']) is not None:
        return render_template('page2.html', web_title=web_title, web_subtitle=web_subtitle, page_title='抽奖', page_body='你填写的学号已经被人填写了哦，检查下拼写吧')
    try:
        sql.insert('random', info)
        sql.commit()
    except:
        return render_template('page2.html', web_title=web_title, web_subtitle=web_subtitle, page_title='未知错误', page_body='Unexpected error:' + traceback.format_exc())
    else:
        res = Response(render_template('page2.html', web_title=web_title, web_subtitle=web_subtitle, page_title='信息填写完成', page_body='信息填写完成\n稍等片刻即将开奖哦'))
        res.set_cookie("CKYF_Random_DO", "1", max_age=1200)
        return res


@app.errorhandler(400)
def no_canshu(error):
    return render_template('page.html', web_title=web_title, web_subtitle=web_subtitle, page_title='参数错误', page_body=error)


@app.errorhandler(401)
def no_auth(error):
    return render_template('unauth.html', web_title=web_title, web_subtitle=web_subtitle, page_body=str(error), page_herf=url_for('login'))


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
    targets = settings['web']['targets']
    port = settings['web']['port']
    appid = settings['web']['qq_oauth']['appid']
    appkey = settings['web']['qq_oauth']['appkey']
    website = settings['web']['website']
    web_title = settings['web']['title']
    web_subtitle = settings['web']['subtitle']

    sql = mysql.MySql(settings['mysql'])

    app.run(port=port, host='0.0.0.0')


