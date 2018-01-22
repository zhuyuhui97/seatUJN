# !/usr/bin/env python
# coding=utf-8

import requests
import json

__author__ = 'lepecoder'
__time__ = '2018-1-22'

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


print(get_seat_id('第九阅览室南区299', 'WMUDGMODO901223225'))
