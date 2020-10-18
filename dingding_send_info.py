#!/usr/bin/env  python
# -*- coding: utf-8 -*-
"""
@author: flySky
"""
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json


def dingDing(monitor_url, response_time):
    timestamp = str(round(time.time() * 1000))
    secret = 'SEC71d6f32ae6c993c28ef83cc56f3dce89da92c2b3446c9ee12b97254d93e45755'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    access_token = 'a29f4414fbc19ef15464183442995cbc57bbb23c6cd021af8371796adc538278'
    url = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(access_token, timestamp,
                                                                                             sign)
    print(url)
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    data = {"msgtype": "text",
            "text": {
                "title": "web站点延迟测试报告",
                "content": "业务报警:\n时间:{}\nweb站点{}\n当前站点访问延迟:{}\n".format(str_time, monitor_url, response_time)
            },
            "at": {"atMobiles": ["18236593202"]}
            }
    headers = {'Content-Type': 'application/json'}
    message = requests.post(url, json.dumps(data), headers=headers).json()
    print(message)
    if message['errmsg'] == 'ok':
        print('钉钉消息推送成功')
    else:
        print('钉钉消息推送失败')


if __name__ == "__main__":
    dingDing("www.baidu.com", "50ms")
