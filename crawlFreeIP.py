import requests
from lxml.html import etree
from getFreeIPS.config import parserList
#用于检测编码格式
import chardet
import random
import os
# sqlchemy config

from getFreeIPS import config
from getFreeIPS.model import engine, session, IP

import gevent
from getFreeIPS.config import MAX_CHECK_CONCURRENT_PER_PROCESS, MINNUM, MAX_DOWNLOAD_CONCURRENT


#统计 ip 数目
global g_count
g_count = 0

#check the ip address is available or not

def check_ip(ip):
    returnValue = os.system('ping -c 1 %s' % ip)
    if returnValue:
        return False
    else:
        return True



def XpathPraser(response, parser):
    '''
    针对xpath方式进行解析
    :param response:
    :param parser:
    :return:
    '''
    # proxylist = []
    root = etree.HTML(response)
    proxys = root.xpath(parser['pattern'])

    spawns = []
    for proxy in proxys:
        try:
            ip = proxy.xpath(parser['position']['ip'])[0].text
            port = proxy.xpath(parser['position']['port'])[0].text
            type = 0
            protocol = 0

            # country = text_('')
            # area = text_('')
            # if text_('省') in addr or self.AuthCountry(addr):
            #     country = text_('国内')
            #     area = addr
            # else:
            #     country = text_('国外')
            #     area = addr
        except Exception as e:
            continue
        # updatetime = datetime.datetime.now()
        # ip，端口，类型(0高匿名，1透明)，protocol(0 http,1 https http),country(国家),area(省市),updatetime(更新时间)

        # proxy ={'ip':ip,'port':int(port),'type':int(type),'protocol':int(protocol),'country':country,'area':area,'updatetime':updatetime,'speed':100}
        # proxy = {'ip': ip, 'port': int(port), 'types': int(type), 'protocol': int(protocol), 'country': country,
        #          'area': area, 'speed': 100}
        # spawns.append(gevent.joinall(check_and_store_ValidIP(ip, port, type, protocol)))
        # if len(spawns) >= MAX_DOWNLOAD_CONCURRENT:
        #     gevent.joinall(spawns)
        #     spawns = []
        # gevent.joinall(spawns)
        check_and_store_ValidIP(ip, port, type, protocol)




def check_and_store_ValidIP(ip,port,type,protocol):
    if check_ip(ip):
        print("ip: %s port: %s type: %d protocol: %d" % (ip, port, type, protocol))
        proxy = IP(id=session.query(IP).count() + 1, ip=ip, port=port, types=int(type), protocol=int(protocol))
        session.add(proxy)
        try:
            session.commit()
        except Exception:
            session.rollback()




def download(url):
    try:
        r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT)
        r.encoding = chardet.detect(r.content)['encoding']
        if (not r.ok) or len(r.content) < 500:
            raise ConnectionError
        else:
            return r.text

    except Exception:
        count = 0  # 重试次数
        # proxylist = sqlhelper.select(10)
        proxylist = session.query(IP).all()[1:20]

        if not proxylist:
            return None

        while count < config.RETRY_TIME:
            try:
                proxy = random.choice(proxylist)
                ip = proxy.ip
                port = proxy.port
                proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}

                r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT, proxies=proxies)
                r.encoding = chardet.detect(r.content)['encoding']
                if (not r.ok) or len(r.content) < 500:
                    raise ConnectionError
                else:
                    return r.text
            except Exception:
                count += 1


def crawl(parser):
    if parser['type'] == 'xpath':
        for url in parser['urls']:
            html_text = download(url=url)

            XpathPraser(html_text, parser)



def startCrawl():
    spawns = []
    for p in parserList:
        spawns.append(gevent.spawn(crawl, p))
        if len(spawns) >= MAX_DOWNLOAD_CONCURRENT:
            gevent.joinall(spawns)
            spawns = []
    gevent.joinall(spawns)
    gevent.sleep(1)



if __name__ == "__main__":
    import time
    start_time = time.time()
    startCrawl()
    end_time = time.time()
    print("all complete! spend %d seconds" % (end_time - start_time))

