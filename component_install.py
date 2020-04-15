#!/usr/bin/python
# coding:utf-8
import os, sys, json

# 接收到的json字符串存入临时文件
with open('/tmp/inventory.json', 'w') as f:
    json.dump(sys.argv[1], f)

# 读入json 字符串读入，返回list 对象
with open('/tmp/inventory.json', 'r') as f:
    data_json = json.load(f)
data_analytical = json.loads(data_json)

# 查看传入的json 中是否有重复ip
ip_list = []
for i in range(len(data_analytical)):
    ip_list.append(data_analytical[i]["ip"])

if __name__ == '__main__':
    path = "/tmp"
    if len(ip_list) == len(set(ip_list)):
        # 没有重复ip使用正常方式( 单机或者集群都可以）
        os.system("ansible-playbook -i ansible_inventory.py playbook/install_elasticsearch.yml")
    else:
        # 如果有重复ip 统一使用单节点安装安装后进行 集群配置
        j =0
        file_list = []
        for i in data_analytical:
            with open("/tmp/inventory." + str(j) + "json", "w") as f:
                json.dump(i, f, ensure_ascii=False)
            file_list.append("/tmp/inventory." + str(j) + "json")
            j = j + 1

        # 生成的文件覆盖/tmp/inventory.json文件进行循环执行，确保按照目录不同进行单机多节点安装
        for tmpfile in file_list:
            os.rename(tmpfile, "/tmp/inventory.json")
            # 按照单节点安装，安装后修改安装目录
            os.system("ansible-playbook -i ansible_inventory.py playbook/install_elasticsearch.yml")
