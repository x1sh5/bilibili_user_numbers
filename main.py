from urllib import request
import re
import time


class bilibiliNUm():
    def __init__(self,opener,Request,giveNum=200000000):
        self.opener = opener
        self.Request = Request
        self.giveNum = giveNum
        self.evalueNum = giveNum*2
        self.top = self.evalueNum
        self.baseurl = Request.full_url

    def is_have_page(self):      
        self.Request.full_url = self.baseurl + str(self.evalueNum)
        res = self.opener.open(self.Request)
        reshtml = res.read().decode("utf-8","ignore")
        r = re.search(r'(?<=<title>)\S{1,50}(?=的个人空间 - 哔哩哔哩)',reshtml)
        if r:
            self.giveNum = self.evalueNum

            if self.top > self.evalueNum:
                self.evalueNum = int((self.giveNum + self.top)/2)
            else:
                self.evalueNum = int(self.giveNum*2)
        else:
            self.top = self.evalueNum
            self.evalueNum =  int((self.giveNum + self.top)/2)
        print("查找中：最大id:%d" %self.evalueNum)
        time.sleep(1)

    def find_the_num(self):
        while self.giveNum!=self.evalueNum:
            self.is_have_page()
        return self.evalueNum


if __name__ == '__main__':
    url = 'https://space.bilibili.com/'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'X-Client-Data': 'CI22yQEIpLbJAQjBtskBCKmdygEIjrnKAQj4x8oBCPrPygEItoDLAQjQmssBCOOcywEIqZ3LAQigoMsBCODvywEI8vDLAQjd8ssB',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'UTF-8',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh-SG;q=0.8,zh;q=0.7,ja;q=0.6,en;q=0.5,en-US;q=0.4',
    }

    # 创建http请求管理器
    http_handle = request.HTTPHandler()

    # 创建https管理器
    https_handle = request.HTTPSHandler()

    # 创建求求管理器，将上面3个管理器作为参数属性
    opener =  request.build_opener(http_handle,https_handle)

    req = request.Request(url,headers=headers)

    res = opener.open(req)
    bn = bilibiliNUm(opener,req)
    num = bn.find_the_num()
    localtime = time.asctime(time.localtime(time.time()))
    print('B站{}的用户数是{}'.format(localtime,num))


