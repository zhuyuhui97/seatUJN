## 济南大学图书馆座位自动预约脚本

### api.md
api是从Android端抓包获取

### config.json
`config.json`是配置文件,记录用户账号和要预约的座位,其中的时间是从0点开始计算的分钟数.
`seat`中的座位号必须是3位

### freebook.py
按照`config.json`自动预约`第二天`的座位,可设置每天05:05自动执行.

>windows

先写一个批处理执行python脚本

```bat
f:
cd F:\作业同步文件夹\seatUJN
python freebook.py
```

然后设置计划任务

![](http://p1f1jwe7c.bkt.clouddn.com/18-1-22/42094914.jpg)
![](http://p1f1jwe7c.bkt.clouddn.com/18-1-22/69343034.jpg)

>linux

使用`cron`设置计划任务
```
* 5 5 * * ? /usr/bin/python /home/lxp/document/seatUJN/freebook.py
```

### locToSeat.py
把诸如`第一阅览室001号`转换seatId`22558`

### seatDaemon.py
不摇碧莲守护进程,可以设置每小时运行一次,如果有快到期的预约则取消当前预约,重新预约一小时后的时间,结束时间不变.







