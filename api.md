## 登录
http://seat.ujn.edu.cn/rest/auth?username=220140421164&password=220140421164
获取token
```json
{"status":"success","data":{"token":"T58UTCARF601204212"},"code":"0","message":""}
{"status":"fail","code":"13","message":"登录失败: 密码不正确","data":null}
```


## keep-alive
http://seat.ujn.edu.cn/rest/v2/user/reservations?token=K70M9XXYLL01204845


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
            },
            {
                "id": 3669325,
                "date": "2018-1-21",
                "begin": "19:00",
                "end": "22:00",
                "awayBegin": null,
                "awayEnd": null,
                "loc": "主校区2层213室区第一阅览室001号",
                "stat": "CANCEL"
            },
            {
                "id": 3669326,
                "date": "2018-1-21",
                "begin": "19:00",
                "end": "21:00",
                "awayBegin": null,
                "awayEnd": null,
                "loc": "主校区2层213室区第一阅览室001号",
                "stat": "RESERVE"
            },
            {
                "id": 3669323,
                "date": "2018-1-21",
                "begin": "16:00",
                "end": "20:00",
                "awayBegin": null,
                "awayEnd": null,
                "loc": "主校区2层213室区第一阅览室003号",
                "stat": "CANCEL"
            }
        ]
    },
    "message": "",
    "code": "0"
}
```

## 预约详情(没什么卵用)
http://seat.ujn.edu.cn/rest/view/3669312?token=K70M9XXYLL01204845
```json
{"id":3669312,"receipt":"1164-312-7","onDate":"2018 年 01 月 21 日","begin":"10 : 00","end":"16 : 00","location":"主校区6层601室区第八阅览室北区，座位号003"}
```

## 预约座位
http://seat.ujn.edu.cn/rest/v2/freeBook
POST `token=HLIU9P4HYW01214703&startTime=960&endTime=1200&seat=15343&date=2018-01-21`
return
```json
{"status":"success","data":{"id":3669324,"receipt":"1164-324-7","onDate":"2018 年 01 月 21 日","begin":"16 : 00","end":"20 : 00","location":"主校区3层303室区第二阅览室北区，座位号001","checkedIn":false,"checkInMsg":"请连接此场馆无线网或在触屏机上操作"},"message":"","code":"0"}
```
07:00 -- 420 60*7
11:00 -- 660 60*11

## 取消预约
http://seat.ujn.edu.cn/rest/v2/cancel/3669325?token=75FG9DTUZA01210118
id=3669325
return
```json
{"status":"success","data":null,"message":"","code":"0"}
```

## 签到
http://seat.ujn.edu.cn/rest/v2/checkIn?token=75FG9DTUZA01210118


