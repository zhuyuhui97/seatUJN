## 济南大学图书馆座位自动预约脚本

**注意：**
> 脚本只对西校区有效
> 使用python3 编写
> 用到的模块有：
> - requests
> - json
> - time
> - sys

### api.md
api是从Android端抓包获取

### config.json
记录用户账号和要预约的座位,其中的时间是从0点开始计算的分钟数.
`seat`中的座位号必须是3位

例子：
```json
{
  "stu": [
    {
      "name": "路人甲",
      "username": "220140421164",
      "password": "xxx",
      "seat": "第一阅览室002",
      "startTime": "480",
      "endTime": "720"
    },
    {
      "name": "路人乙",
      "username": "220151222156",
      "password": "xxx",
      "seat": "第九阅览室中区201",
      "startTime": "480",
      "endTime": "720"
    }
  ]
}


```


### freebook.py
按照`config.json`自动预约**`第二天`**的座位,可设置每天05:05自动执行.
`config.json`需作为参数传入且与freebook.py在同一目录下，例如：

```shell
python3 /home/lxp/seatUJN/freebook.py config.json
```

因为周二下午闭馆，因此你可以通过这种方式对周一传入不同的配置文件。

### 自动任务

>windows下设置自动任务

先写一个批处理执行python脚本

```bat
f:
cd F:\作业同步文件夹\seatUJN
python freebook.py config.json
```

然后设置计划任务

![](http://p1f1jwe7c.bkt.clouddn.com/18-1-22/42094914.jpg)
![](http://p1f1jwe7c.bkt.clouddn.com/18-1-22/69343034.jpg)

**windows下未经过验证**


>**linux**下设置自动任务

使用`cron`设置计划任务
```
* 5 5 * * ? /usr/bin/python /home/lxp/document/seatUJN/freebook.py
```

### locToSeat.py
把诸如`第一阅览室001号`转换seatId`22558`

### seatDaemon.py
不摇碧莲守护进程,可以设置每小时运行一次,如果有到期的预约则取消当前预约,重新预约一小时后的时间,结束时间不变.
比如你预约7:59-11:59,在8:03运行的时候发现还没有签到，则取消当前预约并帮你预约8:59-11:59的时间。

**为什么是7:59而不是8:00 ?**

如果是8:00则在8:03-9:00之间，仍有人可以预约`当前-9:00`这不到一小时的时间。

### 我的自动任务

```shell
03   7-21  *    *    * /usr/bin/python3 /root/seatUJN/seatDaemon.py configSeatDaemon.json >> /root/seatUJN/seatDaemon.log
5     5    *    *    2-7 /usr/bin/python3 /root/seatUJN/freebook.py config.json >> /root/seatUJN/freebook.log
5     5    *    *    1 /usr/bin/python3 /root/seatUJN/freebook.py config2.json >> /root/seatUJN/freebook.log
```






