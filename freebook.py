# !/usr/bin/env python
# coding=utf-8

import requests
import json
import time

# 按照config.json的配置预约第二天的座位


# 座位转换
# from '第一阅览室001' to seat-id = 22558
ROOM = """ 
       {"status":"success","data":[{"roomId":41,"room":"第一阅览室","floor":2,"reserved":0,"inUse":0,"away":0,"totalSeats":136,"free":136},{"roomId":12,"room":"第二阅览室中区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":11,"room":"第二阅览室北区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":196,"free":196},{"roomId":13,"room":"第二阅览室南区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":172,"free":172},{"roomId":15,"room":"第十一阅览室中区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":14,"room":"第十一阅览室北区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":188,"free":188},{"roomId":16,"room":"第十一阅览室南区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":156,"free":156},{"roomId":18,"room":"第三阅览室中区","floor":4,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":17,"room":"第三阅览室北区","floor":4,"reserved":0,"inUse":0,"away":0,"totalSeats":148,"free":148},{"roomId":19,"room":"第三阅览室南区","floor":4,"reserved":0,"inUse":0,"away":0,"totalSeats":120,"free":120},{"roomId":21,"room":"第十阅览室中区","floor":4,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":22,"room":"第十阅览室南区","floor":4,"reserved":0,"inUse":0,"away":0,"totalSeats":164,"free":164},{"roomId":35,"room":"第九阅览室中区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":34,"room":"第九阅览室北区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":195,"free":195},{"roomId":36,"room":"第九阅览室南区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":172,"free":172},{"roomId":32,"room":"第四阅览室中区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":31,"room":"第四阅览室北区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":148,"free":148},{"roomId":33,"room":"第四阅览室南区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":164,"free":164},{"roomId":38,"room":"第五阅览室中区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":8,"room":"第五阅览室北区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":59,"free":59},{"roomId":37,"room":"第五阅览室南区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":173,"free":173},{"roomId":47,"room":"第八阅览室中区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":9,"room":"第八阅览室北区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":204,"free":204},{"roomId":40,"room":"第八阅览室南区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":176,"free":176},{"roomId":27,"room":"第七阅览室中区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":46,"room":"第七阅览室北区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":132,"free":132},{"roomId":28,"room":"第七阅览室南区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":108,"free":108},{"roomId":24,"room":"第六阅览室中区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":23,"room":"第六阅览室北区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":132,"free":132},{"roomId":25,"room":"第六阅览室南区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":108,"free":108}],"message":"","code":"0"}
"""
ROOM = json.loads(ROOM)
ROOM = ROOM['data']


def get_seat_id(loc, token):
    local_room = loc[:-3]
    local_seat = loc[-3:]
    room_id = [x for x in ROOM if x['room'] == local_room][0]['roomId']
    room_layer_url = 'http://seat.ujn.edu.cn/rest/v2/room/layoutByDate/' + str(room_id) + '/2017-01-2' \
                                                                                          '2?token=' + token
    r = requests.get(room_layer_url)
    layer = json.loads(r.text)
    layer = layer['data']['layout']

    seat_id = [x for x in layer if layer[x]['type'] == 'seat' and layer[x]['name'] == local_seat]
    if seat_id.__len__() == 0:
        print('找不到' + loc)
        return -1
    else:
        seat_id = layer[seat_id[0]]['id']
        return seat_id


'''
http://seat.ujn.edu.cn/rest/auth?username=220140421164&password=220140421164
获取token                                    

{"status":"success","data":{"token":"T58UTCARF601204212"},"code":"0","message":""}
{"status":"fail","code":"13","message":"登录失败: 密码不正确","data":null}

'''


def getToken(username, password):
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


'''
http://seat.ujn.edu.cn/rest/v2/freeBook
POST `token=HLIU9P4HYW01214703&startTime=960&endTime=1200&seat=15343&date=2018-01-21`
'''


def freeBook(token, startTime, endTime, seat):
    tomorrow = time.strftime("%Y-%m-%d", time.localtime(86400 + time.time()))
    url = 'http://seat.ujn.edu.cn/rest/v2/freeBook'
    para = {
        'token': token,
        'startTime': startTime,
        'endTime': endTime,
        'seat': seat,
        'date': tomorrow
    }
    r = requests.post(url, data=para)
    resp = json.loads(r.text)
    if resp['status'] == 'fail':
        print(r.text)
        return -1
    else:
        return 1


if __name__ == '__main__':
    f = open('config.json', 'r', encoding='utf8')
    info = json.load(f)
    # print(info)
    # print(len(info['stu']))
    for i in info['stu']:
        token = getToken(i['username'], i['password'])
        if token != -1:
            seat_id = get_seat_id(i['seat'], token)
            if seat_id != -1:
                status = freeBook(token, i['startTime'], i['endTime'], seat_id)
            else:
                status = -1
        if token != -1 and status != -1:
            print(i['name'] + 'success！！')
