import json

import requests

base_url = 'https://mms.pinduoduo.com'
url = base_url + '/janus/api/auth'

body = '{"username":"乐和食品店:冯露","password":"x/oZk1Mbd9JcVoo2lHNLa6EvtFg8wxaSRhQsrjMXw6ii7glsovkf8WegIGE7PLQyJi1edz0CcW6SYsFoh3+4NUXWbJP1X4OzIiDxpkMr1JB6IkecsYpY81lZIviXkbhm83bKwCLY8HiD4lLi7cdUjyUlun2jL5ObCQo3iPDMusU=","passwordEncrypt":true,"verificationCode":"","mobileVerifyCode":"","sign":"","touchevent":{"mobileInputEditStartTime":1620874408492,"mobileInputEditFinishTime":1620874408506,"mobileInputKeyboardEvent":"0|0|0|","passwordInputEditStartTime":1620874408509,"passwordInputEditFinishTime":1620874408518,"passwordInputKeyboardEvent":"0|0|0|","captureInputEditStartTime":"","captureInputEditFinishTime":"","captureInputKeyboardEvent":"","loginButtonTouchPoint":"1262,417","loginButtonClickTime":1620874644471},"fingerprint":{"innerHeight":377,"innerWidth":1741,"devicePixelRatio":2,"availHeight":1095,"availWidth":1745,"height":1120,"width":1792,"colorDepth":30,"locationHref":"https://mms.pinduoduo.com/login","clientWidth":1741,"clientHeight":883,"offsetWidth":1741,"offsetHeight":883,"scrollWidth":2899,"scrollHeight":883,"navigator":{"appCodeName":"Mozilla","appName":"Netscape","hardwareConcurrency":12,"language":"zh","cookieEnabled":true,"platform":"MacIntel","doNotTrack":"1","ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36","vendor":"Google Inc.","product":"Gecko","productSub":"20030107","mimeTypes":"929366d991bcb074a793ac3fe76dcb4a27d30ed8","plugins":"b52df06a1ec8b703e6274d928c7df35f3e741f33"},"referer":"https://mms.pinduoduo.com/home","timezoneOffset":-480},"riskSign":"ea30722422a5ea78e3535552b11884c6507a617e5f680ba671470a5b7825cb7b","timestamp":1620874644481}'

headers = {
    "content-type": "application/json",
    "ETag": "TTLP5ZyhUEFqloUMXbFUGktM14BIi0fH"
}

res = requests.post(url, json=json.loads(body), headers=headers)

print(res.json())
