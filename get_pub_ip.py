#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import time


def get_pub_ip():
    response_info = requests.get("https://ip.tool.lu").text
    public_ip = response_info.split("\n")[0].split(" ")[1]
    return public_ip


if __name__ == "__main__":
    print("start get public ip")
    ip_list = [str(get_pub_ip().strip("\r"))]
    print("公网出口ip列表:" + str(ip_list))
    while True:
        time.sleep(5)
        current_ip = get_pub_ip()
        if current_ip.strip("\r") not in ip_list:
            ip_list.append(str(get_pub_ip().strip("\r")))
            print("公网出口ip列表:" + str(ip_list))