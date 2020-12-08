from flask import Flask
from flask import request
import mirai
import hmac
import getopt
import sys
import ujson

app = Flask(__name__)

def encryption(data):
    key = github_secret.encode('utf-8')
    obj = hmac.new(key, msg=data, digestmod='sha1')
    return obj.hexdigest()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/webhook/github', methods=['POST'])
def github_hook():
    post_data = request.data
    token = encryption(post_data)
    signature = request.headers.get('X-Hub-Signature', '').split('=')[-1]
    if signature != token:
        return "token认证无效", 401
    r = request.json
    repo_name = r['repository']['name']
    pusher = r['commits'][0]['author']['name']
    try:
        pusher_name = github_name[pusher]
    except:
        pusher_name = '未知名称 ' + pusher
    commit = r['commits'][0]['message']
    ss = '%s 刚刚向GIT仓库 %s 推送更新 %s' % (pusher_name, repo_name, commit)
    print(ss)
    mirai.sendQQMessage(ss, url, authKey, bot, targets)
    return 'ok'


@app.route('/webhook/svn', methods=['POST'])
def svn_hook():
    if svn_secret != request.headers.get('X-Ones-Svn', ''):
        return "token认证无效", 401
    r = request.json
    repo_name = r['repository']
    if repo_name == 'RM2020':
        repo_name = 'RM2021'
    pusher = r['author'][:-1]
    try:
        pusher_name = github_name[pusher]
    except:
        pusher_name = pusher
    commit = r['message'][:-1]
    ss = '%s 刚刚向SVN仓库 %s 推送更新 %s' % (pusher_name, repo_name, commit)
    print(ss)
    mirai.sendQQMessage(ss, url, authKey, bot, targets)
    return 'ok'

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "s:", ["settings="])
    for opt, arg in opts:
        if opt in ("-s", "--settings"):
            file = arg
    f = open(file, 'r')
    settings = ujson.loads(f.read())
    f.close()

    github_name = settings['webhook']['name2user']
    github_secret = settings['webhook']['github_secret']
    svn_secret = settings['webhook']['svn_secret']
    targets = settings['webhook']['targets']
    url = settings['mirai']['url']
    authKey = settings['mirai']['authkey']
    bot = settings['mirai']['qq']
    port = settings['webhook']['port']

    app.run(port=port, host='0.0.0.0')
