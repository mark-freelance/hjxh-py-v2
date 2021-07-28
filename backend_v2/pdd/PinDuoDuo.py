# -*- coding: utf-8 -*-
# __author__ = "pw0rld"
# Date: 2021/07/20
'''
POST DATA
POST /janus/api/auth HTTP/1.1
Host: mms.pinduoduo.com
Connection: close
Content-Length: 2116
Cache-Control: max-age=0
sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
Anti-Content: 0apAfaiU0OQoF99VdOP09lG-3nAgoeXiQejzjSn4v2TohOFzZe_Sn9D8OLzOFZEB2jjuO6wYpCEb8xm6Qy7qCZsanMUfBm3JNMfZmmStVDcWZmRbNNKLM0IQxM1L86xGV8ETA0LKYwO8Y3yHpXlxdeowBYkPFQHdXMDOjacM7YutAiYCZ9fBTEVCAu3VcslzfgpfT3fI4oVOI7lkA8r4OB7AlFwUvXMt8aelZj921pvppl3NUB52jCBX-u9DkSZlCf3jrdXjwVzmd9GW9DxPUV7xrjLrwVEABk948XyPyu9XAWgn-ZeVTagtXn2vU_C1yqylWr0j-MnGdzlEsmyDao3MOkJ39BkMnORVYpDQXKJ3vUF1IB-AIjnLKEriZa-lM_N6OBdTdyAsoPZ0jaAyvEsV2pm4wmJq3a5DhWmrxF-HApDwzLaDPm15JBMWiMPprQeaNwGDQ7wAhfq9kizAZ4DoAk2q
sec-ch-ua-mobile: ?0
ETag: DRG1pLzzRH2BIEIlHBw4Z7fqDqniaqog
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36
DNT: 1
content-type: application/json
Accept: */*
Origin: https://mms.pinduoduo.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://mms.pinduoduo.com/login
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7,bg;q=0.6
Cookie: _crr=DRG1pLzzRH2BIEIlHBw4Z7fqDqniaqog; _bee=DRG1pLzzRH2BIEIlHBw4Z7fqDqniaqog; _f77=74cadbd8-6583-485b-83a2-ecd0ee9f9ef8; _a42=8fe3879f-1110-40f1-bf8c-75a6ad83209f; rcgk=DRG1pLzzRH2BIEIlHBw4Z7fqDqniaqog; rckk=DRG1pLzzRH2BIEIlHBw4Z7fqDqniaqog; ru1k=74cadbd8-6583-485b-83a2-ecd0ee9f9ef8; ru2k=8fe3879f-1110-40f1-bf8c-75a6ad83209f; api_uid=ChDEsmD2vyQuW3iiRYUNAg==; _nano_fp=XpExn5mJXqdxnqXYl9_4fFmsRoOQ34AS9kJxL1hW; mms_b84d1838=3414,120,3397,3434,3432,1202,1203,1204,1205,3417; x-visit-time=1626824805402; JSESSIONID=144EF04E31F03615BCEC8559EBA27C6D

{"username":"乐和食品店:冯露","password":"","passwordEncrypt":true,"verificationCode":"","mobileVerifyCode":"","sign":"","touchevent":{"mobileInputEditStartTime":"","mobileInputEditFinishTime":"","mobileInputKeyboardEvent":"0|0|0|1626824816298","passwordInputEditStartTime":1626824816218,"passwordInputEditFinishTime":1626824816231,"passwordInputKeyboardEvent":"0|0|0|22","captureInputEditStartTime":"","captureInputEditFinishTime":"","captureInputKeyboardEvent":"","loginButtonTouchPoint":"1131,563","loginButtonClickTime":1626824819853},"fingerprint":{"innerHeight":722,"innerWidth":1536,"devicePixelRatio":1.25,"availHeight":824,"availWidth":1536,"height":864,"width":1536,"colorDepth":24,"locationHref":"https://mms.pinduoduo.com/login","clientWidth":1519,"clientHeight":883,"offsetWidth":1519,"offsetHeight":883,"scrollWidth":2788,"scrollHeight":883,"navigator":{"appCodeName":"Mozilla","appName":"Netscape","hardwareConcurrency":8,"language":"zh-CN","cookieEnabled":true,"platform":"Win32","doNotTrack":"1","ua":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36","vendor":"Google Inc.","product":"Gecko","productSub":"20030107","mimeTypes":"5d9afaf50eefd8ebbdc23be79730589c2eb566f2","plugins":"90c6811fe45bd6f0fcceb9a50831c414d7123164"},"referer":"https://mms.pinduoduo.com/home/","timezoneOffset":-480},"riskSign":"42185af6db2581cabfc6ec78edd2c775","timestamp":1626824819867,"crawlerInfo":"0apAfaiU0OQoF99VdOP09lG-3nAgoeXiQejzjSn4v2TohOFzZe_Sn9D8OLzOFZEB2jjuO6wYpCEb8xm6Qy7qCZsanMUfBm3JNMfZmmStVDcWZmRbNNKLM0IQxM1L86xGV8ETA0LKYwO8Y3yHpXlxdeowBYkPFQHdXMDOjacM7YutAiYCZ9fBTEVCAu3VcslzfgpfT3fI4oVOI7lkA8r4OB7AlFwUvXMt8aelZj921pvppl3NUB52jCBX-u9DkSZlCf3jrdXjwVzmd9GW9DxPUV7xrjLrwVEABk948XyPyu9XAWgn-ZeVTagtXn2vU_C1yqylWr0j-MnGdzlEsmyDao3MOkJ39BkMnORVYpDQXKJ3vUF1IB-AIjnLKEriZa-lM_N6OBdTdyAsoPZ0jaAyvEsV2pm4wmJq3a5DhWmrxF-HApDwzLaDPm15JBMWiMPprQeaNwGDQ7wAhfq9kizAZ4DoAk2q"}


'''
import logging

import execjs.runtime_names
import time

import pymongo
import requests

from settings import MONGO_URI, MONGO_DATABASE_NAME
from datetime import datetime

"""
pip3 install execjs
"""


def cookies_operater(cookie):
    cookies = {}
    for line in cookie.split(";"):
        if line.find("=") > 0:
            name, value = line.strip().split("=", 1)  # 处理异常
            cookies[name] = value
    return cookies


def times():
    nowTime = lambda: int(round(time.time() * 1000))  # 生成毫秒级时间戳
    return nowTime()


def get_anti_content(cookies):
    with open("genAntiContent.js", "r", encoding="utf-8") as f:
        ctx = execjs.compile(f.read())
    ret = ctx.call("genAntiContent_poc", cookies)
    return ret


class PingDuoDuoSpider(object):
    def __init__(self, username, password):
        self.password = password
        self.username = username
        self.url = "https://mms.pinduoduo.com/janus/api/auth"
        cookies = "api_uid=rBRIRmD4yihupRY9mj4qAg==; _nano_fp=XpExn5UanqTjXqTon9_QWuL6uwGiCb5BPEFlPPMm; _crr=uEj0fGdlNO5gYeaTr1Lud0LWI5znBanu; _bee=uEj0fGdlNO5gYeaTr1Lud0LWI5znBanu; _f77=b0ad48d9-0715-463d-845c-bdddea682cf2; _a42=57bbeb3e-e337-4c9d-8857-aa42749d82ae; rcgk=uEj0fGdlNO5gYeaTr1Lud0LWI5znBanu; rckk=uEj0fGdlNO5gYeaTr1Lud0LWI5znBanu; ru1k=b0ad48d9-0715-463d-845c-bdddea682cf2; ru2k=57bbeb3e-e337-4c9d-8857-aa42749d82ae; x-visit-time=1626932025203; JSESSIONID=4D8505CC70DF8B943A43A7FE19464473; mms_b84d1838=3414,120,3397,3434,3432,1202,1203,1204,1205,3417; msfe-pc-cookie-captcha-token=pDrTck3ltmrWZv_LOjBenA28ff7b4751bf6d97b"
        cookies = cookies_operater(cookies)
        self.cookies = "_nano_fp=XpExn5UxnqmbX5TYX9_qJfwLrVtMHIxUIMARU6f1; _crr={0}; _bee={1};rcgk={2};rckk={3}; _f77={4}; _a42={5};ru1k={6}\
		; ru2k={7};api_uid={8};x-visit-time={9}; mms_b84d1838=3414,120,3397,3434,3432,1202,1203,1204,1205,3417;" \
            .format(cookies["_crr"], cookies["_bee"], cookies["rcgk"], cookies["rckk"], cookies["_f77"],
                    cookies["_a42"], \
                    cookies["ru1k"], cookies["ru2k"], cookies["api_uid"], times())

    def genc_pass(self):
        with open("encryp.js", "r", encoding="utf-8") as f:
            ctx = execjs.compile(f.read())
        ret = ctx.call("encrypt_Pwd", self.password)
        return ret

    def genc_riskSign(self):
        with open("riskSign.js", "r", encoding="utf-8") as f:
            ctx = execjs.compile(f.read())
        start_time = times()
        riskSign_str = "username={0}&password={1}&ts={2}".format(self.username, self.password, start_time)
        # riskSign_str += nows_time
        ret = ctx.call("riskSign", riskSign_str)
        return ret, start_time

    def get_pass_id(self):
        anti_content = get_anti_content(self.cookies)
        headers = {
            'sec-ch-ua': "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
            'anti-content': anti_content,
            "VerifyAuthToken": "pDrTck3ltmrWZv_LOjBenA28ff7b4751bf6d97b",
            'sec-ch-ua-mobile': "?0",
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B)",
            'dnt': "1",
            'VerifyAuthToken': 'neo_wWX39b4JsAivL6G7vAb837df8882d4048eb',
            'Cookie': self.cookies,
            'content-type': "application/json",
            'accept': "*/*",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'cache-control': "no-cache",
        }
        access_riskSign = self.genc_riskSign()
        data = '''{{"username":"{0}","password":"{1}","passwordEncrypt":true,"verificationCode":"","mobileVerifyCode":"","sign":"","touchevent":{{"mobileInputEditStartTime":"1626833459113","mobileInputEditFinishTime":"1626833459442","mobileInputKeyboardEvent":"0|1|1|186-78","passwordInputEditStartTime":{2},"passwordInputEditFinishTime":{3},"passwordInputKeyboardEvent":"0|0|0|819-1051-1275-1587-1819-1971-2259-2571-2748-3059-3356","captureInputEditStartTime":"{4}","captureInputEditFinishTime":"","captureInputKeyboardEvent":"","loginButtonTouchPoint":"1179,157","loginButtonClickTime":{5}}},"fingerprint":{{"innerHeight":722,"innerWidth":1536,"devicePixelRatio":1.25,"availHeight":824,"availWidth":1536,"height":864,"width":1536,"colorDepth":24,"locationHref":"https://mms.pinduoduo.com/login/?redirectUrl=https%3A%2F%2Fmms.pinduoduo.com%2Fhome","clientWidth":1519,"clientHeight":883,"offsetWidth":1519,"offsetHeight":883,"scrollWidth":2788,"scrollHeight":883,"navigator":{{"appCodeName":"Mozilla","appName":"Netscape","hardwareConcurrency":8,"language":"zh-CN","cookieEnabled":true,"platform":"Win32","doNotTrack":"1","ua":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36","vendor":"Google Inc.","product":"Gecko","productSub":"20030107","mimeTypes":"5d9afaf50eefd8ebbdc23be79730589c2eb566f2","plugins":"90c6811fe45bd6f0fcceb9a50831c414d7123164"}},"referer":"https://mms.pinduoduo.com/home","timezoneOffset":-480}},"riskSign":"{6}","timestamp":{7},"crawlerInfo":"{8}"}}'''.format(
            self.username, self.genc_pass(), times(), times(), times(), times(), access_riskSign[0], access_riskSign[1],
            anti_content)
        # print(self.genc_pass())
        # print(data)
        # print(data)
        reqs = requests.session()
        req = reqs.post(url=self.url, headers=headers, data=data.encode(), verify=False)
        print("request result: ")
        print(req.text)
        login_cookies = requests.utils.dict_from_cookiejar(req.cookies)
        print("login cookie: ")
        print(login_cookies)
        pass_id = login_cookies.get("PASS_ID")
        print("PASS_ID: ")
        print(pass_id)
        return pass_id


if __name__ == '__main__':
    user = ("牧老板食品专营店冯露", "Fl123456...")
    user = ("千寻生鲜:志骐", "Hzq734985..")
    user = ("牧鲜生:志骐", "Hzq706752..")
    user = ("农夫牧场邓雪梅", "Dxm20201201..")
    user = ("乐和食品店:冯露", "FL123456...")
    # user = ("皇家小虎食品旗舰店雷港", "Lg1234567890")
    user = ("皇家小虎食品旗舰店冯露", "Fl123456...")

    """
    get PASS_ID
    """
    username, password = user
    pdd = PingDuoDuoSpider(username, password)
    pass_id = pdd.get_pass_id()

    """
    update database
    """
    if not pass_id:
        logging.warning("PASS_ID 无效，请检查账号信息，或重新登录")
    else:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DATABASE_NAME]
        coll_name = "accounts"
        db[coll_name].update_one({"_id": username}, {
            "$set": {"username": username, "password": password, "PASS_ID": pass_id, "verified_time": datetime.now()}},
                                 upsert=True)
        logging.info(f"updated account of {username} into database: [{MONGO_DATABASE_NAME}, {coll_name}]")
