# !/usr/bin/env python
# coding=utf-8
__author__ = 'lepecoder'
__time__ = '2018-3-17'

import time
import requests
import json
import sys

def get_token(username, password):
    url = 'http://seat.ujn.edu.cn/rest/auth'
    param = {
        'username': username,
        'password': password
    }
    r = requests.get(url, params=param)
    resp = json.loads(r.text)
    if resp['status'] == 'fail':
        print(username + '   ' + r.text)
        return -1
    else:
        return resp['data']['token']


def checkin(token):
    url = 'http://seat.ujn.edu.cn/rest/v2/checkIn?token='
    r = requests.get(url=url+token)
    print(r.text+'\n')

if __name__ == '__main__':
    if sys.argv.__len__() <= 1:
        print("请传入配置文件名称")
        sys.exit()
    filename = sys.argv[1]
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print('----------------------' + now + '-----------------------')
    f = open(sys.path[0] + '/' + filename, 'r', encoding='utf8')
    info = json.load(f)
    for i in info['stu']:
        token1 = get_token(i['username'], i['password'])
        checkin(token1)

