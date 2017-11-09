# -*- encoding: utf-8 -*-


import subprocess
import logging
import time
from threading import Timer
from lxml import etree


def curl(url):
    cmd = ['curl', '--connect-timeout', '8', '-m', '8', url,"--user-agent","Mozilla"]
    getit = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer = Timer(8, lambda process: process.kill(), [getit])
    try:
        timer.start()
        stdout, stderr = getit.communicate()
    finally:
        timer.cancel()
    if isinstance(stdout, str) and len(stdout):
        return stdout
    else:
        return []


def download(name, url):
    cmd = ['curl', '--connect-timeout', '8', '-m', '12', '-o', name, url]
    getit = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer = Timer(13, lambda process: process.kill(), [getit])
    try:
        timer.start()
        stdout, stderr = getit.communicate()
    finally:
        timer.cancel()
    if isinstance(stdout, str) and len(stdout):
        return stdout
    else:
        return []




previous =  []

def main(time_flag):
    global previous
    source = curl('http://www.oinbag.com/')
    if source is not []:
        html = etree.HTML(source)
        img_time = html.xpath('//label[@class="event-time"]/text()')
        starttime = img_time[0]
        endtime = img_time[-1]
        # 转换成时间戳
        starttime = time.mktime(time.strptime(starttime, "\n%Y/%m/%d %H:%M:%S"))
        endtime = time.mktime(time.strptime(endtime, "\n%Y/%m/%d %H:%M:%S"))
        if endtime > time_flag:
            pass
        else:
            return 0

        img1 = html.xpath('//div[@class="img-list-container"]/ul/li[@class="event-img-file"]/a/img/@src')
        img1_name = html.xpath('//div[@class="img-list-container"]/ul/li[@class="event-img-file"]/a/img/@alt')

        for i in range(len(img1)):
            if img1_name[i] not in  previous:
                image_url = img1[i][:-30]
                image_url = image_url[:image_url.find("x-oss")-1]
                download("./plates/"+'_'+str(i)+"_"+img1_name[i].encode('utf-8')+'.jpg',image_url )
                logging.critical('download '+img1_name[i].encode('utf-8')+'_'+str(i)+'.jpg')
        previous = img1_name
        return starttime
    else:
        return 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='collector.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.CRITICAL)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    count = 1
    while 1:
        gettime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        logging.critical("This is the " + str(count) + " time to start:" + gettime)
        time_flag = 0
        res = main(time_flag)
        if res == 0:
            time.sleep(20)
        else:
            time_flag = res
            time.sleep(100)
        count += 1

