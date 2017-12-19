# getFreeIPS
Get free proxy IPs from FREE IP SHARE websites
##

The repo reference to the [repo](https://github.com/qiyeboy/IPProxyPool), 
you can think it is a simplified version.
##Description
* config.py

this file is a config file, it includes
free ip share websites that we crawl, the location
of data we stored, user_agents and so on.

* model.py

this file is to descrbe the table structure of data 
we will store, we use sqlalchemy to acheieve this, 
and also, we generate some useful variables, such as
session and so on.

* crawlFreeIP.py

this file actually is a spider, it will crawl the free
ip share websites, get free IP's ip, port, type, protocol
and store it in database, now we support sqlite database,
later, we will add other popular databases. In our opinion,
sqlite is very suitable!

* getFreeIP.py

this file offer methods that get IPs from database for other
module or method's call use.


##Useage:

you can use this as a module

```
from getFreeIPS.getFreeIP import getfreeip
'''
    ip.id
    ip.ip
    ip.port
    ip.types
    ip.protocol
'''
ips = getfreeip(10)
for ip in ips:
    print(ip.ip)

```