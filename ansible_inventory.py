#!/usr/bin/env python2
# coding:utf-8
# author: flysky
import json

# meta 返回格式
# "_meta": {
#     "hostvars": {
#         "192.168.8.101": {
#             "ansible_user": "root",
#             "ansible_password": "qweasd"
import sys


def unicode_convert(input):
    if isinstance(input, dict):
        return {unicode_convert(key): unicode_convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [unicode_convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def get_ip_list(data_analytical_arg):
    """
    :param data_analytical_arg: 接受传入的json转化后的字典
    :return: 返回主机list
    """
    host_ip = []
    for i in range(len(data_analytical_arg)):
        host_ip.append(data_analytical_arg[i]["ip"])
    group_name = data_analytical_arg[i]["components"]
    return host_ip, group_name


def get_vars_direct(data_analytical_arg):
    """

    :param data_analytical_arg: json 解析为字典后的对象
    :return: _meta 对用的字典
    """
    meta_arg = {}
    host_direct = {}
    cluster_ip = []
    name_node_list = []

    for x in range(len(data_analytical_arg)):
        cluster_ip.append(data_analytical_arg[x]["ip"] + ":" + data_analytical_arg[x]["server_tcp_port"])
        name_node_list.append("node-" + data_analytical_arg[x]["ip"])

    for i in range(len(data_analytical_arg)):
        # var_direct = {key: value for key, value in data_analytical_arg[i].items() if key != "ip"}
        var_direct = {key: value for key, value in data_analytical_arg[i].items()}
        var_direct["cluster_ip"] = cluster_ip
        var_direct["node_list"] = name_node_list
        var_direct["ip_num"] = len(cluster_ip)
        host_direct[data_analytical_arg[i]["ip"]] = var_direct
    meta_arg["hostvars"] = host_direct
    return meta_arg


def inventory_host(host_list_ip, group_name, meta_arg):
    """

    :param host_list_ip: 传入json 中的主机ip 列表
    :param group_name: 主机组名称
    :param meta_arg: 主机变量字典
    :return:
    """
    # host1ip = ['192.168.2.51','192.168.2.81']
    # group_name = 'test1'
    # data = {group_name: {"hosts": host_list_ip, "vars": vars_direct}}
    data = {group_name: {"hosts": host_list_ip}, "_meta": meta_arg}
    # data = {group_name:{"hosts":host_list_ip,"vars":{"var1":"test1","var2":"test2"}}}
    print(json.dumps(data, indent=4))
    # print(json.dumps(data))


if __name__ == '__main__':
    # 期望接受的json 格式
    # data_json = '[{"ip":"192.168.2.81", "ansible_port":"22", "ansible_ssh_user":"root", "ansible_ssh_pass":"rootroot", "setup_path":"/home/pla", "components":"elasticsearch","server_port":"9200"},' \
    #            '{"ip":"192.168.2.82", "ansible_port":"22", "ansible_ssh_user":"root", "ansible_ssh_pass":"rootroot", "setup_path":"/home/pla", "components":"elasticsearch","server_port":"9200"},' \
    #           '{"ip":"192.168.2.87", "ansible_port":"22", "ansible_ssh_user":"root", "ansible_ssh_pass":"rootroot","setup_path":"/home/pla", "components":"elasticsearch","server_port":"9200"}]'

    # data_json = '[{"ip":"192.168.2.81", "ansible_port":"22", "ansible_ssh_user":"root", "ansible_ssh_pass":"rootroot", "setup_path":"/home/pla", "components":"elasticsearch","server_port":"9200"}]'
    # 解析json字符串为字典
    f = open('/tmp/inventory.json', 'r')
    data_analytical_tmp = unicode_convert(json.load(f))
    f.close()
    if isinstance(data_analytical_tmp, dict):
        data_analytical = []
        data_analytical.append(data_analytical_tmp)
    # print(data_analytical)
    inventory_host(get_ip_list(data_analytical)[0], get_ip_list(data_analytical)[1], get_vars_direct(data_analytical))
    # print(data_json)
