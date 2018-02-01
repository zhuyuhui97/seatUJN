# !/usr/bin/env python
# coding=utf-8
import requests
import json
import time
import sys

'''
如果有快到时间的预约，
1. 取消当前预约
2. 重新预约后面的时间
'''

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


def get_local_date():
    localtime = time.localtime(time.time())
    ans = str(localtime.tm_year) + '-' + str(localtime.tm_mon) + '-' + str(localtime.tm_mday)
    return ans


nowDate = get_local_date()
nowHour = int(time.strftime("%H", time.localtime()))


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


'''
## 我的预约
http://seat.ujn.edu.cn/rest/v2/history/1/1000?token=K70M9XXYLL01204845

最多1000条记录
```json
{
    "status": "success",
    "data": {
        "reservations": [
            {
                "id": 3669317,
                "date": "2018-1-22",
                "begin": "07:00",
                "end": "11:00",
                "awayBegin": null,
                "awayEnd": null,
                "loc": "主校区2层213室区第一阅览室001号",
                "stat": "CANCEL"
            },
            {
                "id": 3669318,
                "date": "2018-1-22",
                "begin": "07:00",
                "end": "11:00",
                "awayBegin": null,
                "awayEnd": null,
                "loc": "主校区2层213室区第一阅览室001号",
                "stat": "CANCEL"
            }
            }
'''


# 查看我的预约
def get_history(token):
    url = 'http://seat.ujn.edu.cn/rest/v2/history/1/1000?token=' + token
    r = requests.get(url)
    resp = json.loads(r.text)
    if resp['status'] == 'fail':
        print('查看预约失败' + r.text)
        return -1
    # print(resp)
    need_free = False
    for raw in resp['data']['reservations']:
        # 预约状态+当天+预约时长大于1小时+已到预约时间
        # print('stat ,'+raw['stat'])
        # print('date ,'+raw['date'], nowDate)
        # print('hour ,'+str(int(raw['begin'][:2])-1) ,str(nowHour))
        if raw['stat'] == 'RESERVE' and raw['date'] == nowDate and int(raw['end'][:2]) - int(
                raw['begin'][:2]) > 1 and int(raw['begin'][:2]) - 1 == nowHour:
            print('需要续约')
            need_free = True
            # cancle the reservation
            # http://seat.ujn.edu.cn/rest/v2/cancel/3669325?token=75FG9DTUZA01210118
            cancleUrl = 'http://seat.ujn.edu.cn/rest/v2/cancel/' + str(raw['id']) + '?token=' + token
            r1 = requests.get(cancleUrl)
            resp1 = json.loads(r1.text)
            if resp1['status'] == 'fail':
                print('取消当前预约失败' + r1.text)
                return -1
            # 预约后面的时间
            # http://seat.ujn.edu.cn/rest/v2/freeBook
            # POST `token=HLIU9P4HYW01214703&startTime=960&endTime=1200&seat=15343&date=2018-01-21`
            freeBookUrl = 'http://seat.ujn.edu.cn/rest/v2/freeBook'
            seat = get_seat_id(raw['loc'][10:-1], token)
            if seat == -1:
                print("查找座位" + raw['loc'] + '失败')
                return -1
            param = {
                'token': token,
                'startTime': str((int(raw['begin'][:2]) + 1) * 60),
                'endTime': str(int(raw['end'][:2]) * 60),
                'seat': seat,
                'date': nowDate
            }
            r = requests.post(freeBookUrl, data=param)
            resp2 = json.loads(r.text)
            if resp2['status'] == 'fail':
                print('续约失败  ，' + r.text)
                return -1
            print('续约成功 ' + r.text)
            break
    if not need_free:
        print("无需续约")
    return 1


if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print('----------------------' + now + '-----------------------')
    f = open(sys.path[0] + '/config.json', 'r', encoding='utf8')
    info = json.load(f)
    for i in info['stu']:
        token1 = get_token(i['username'], i['password'])
        if token1 != -1:
            print(i['username'] + '登陆成功')
            status = get_history(token1)
