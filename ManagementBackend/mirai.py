import requests
import ujson
import time
from requests import HTTPError


def sendQQMessage(message, url, authKey, bot, targets):
    try:
        r = ujson.loads(requests.post(url + 'auth', json={'authKey': authKey}).text)
        print(r)
        session = r['session']
    except:
        raise HTTPError("mirai couldn't connect")
    finally:
        r = ujson.loads(requests.post(url + 'verify', json={'sessionKey': session, 'qq': bot}).text)
        print(r)
        for it in targets:
            r = ujson.loads(requests.post(url + 'sendGroupMessage', json={'sessionKey': session, 'target': it,
                                                'messageChain': [{"type": "Plain", "text": message}]}).text)
            print(r)
            time.sleep(0.5)
        r = ujson.loads(requests.post(url + 'release', json={'sessionKey': session, 'qq': bot}).text)
        print(r)


def sendAtAllQQMessage(message, url, authKey, bot, targets):
    try:
        r = ujson.loads(requests.post(url + 'auth', json={'authKey': authKey}).text)
        print(r)
        session = r['session']
    except:
        raise HTTPError("mirai couldn't connect")
    finally:
        r = ujson.loads(requests.post(url + 'verify', json={'sessionKey': session, 'qq': bot}).text)
        print(r)
        for it in targets:
            r = ujson.loads(requests.post(url + 'sendGroupMessage', json={'sessionKey': session, 'target': it,
                                                'messageChain': [{"type": "AtAll"}, {"type": "Plain", "text": message}]}).text)
            print(r)
            time.sleep(0.5)
        r = ujson.loads(requests.post(url + 'release', json={'sessionKey': session, 'qq': bot}).text)
        print(r)