#!usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import struct
import time
import json
from utils.logger import logger
from conf.settings import PROXY_TOKEN, PROXY_COUNT, PROXY_PORT, PROXY_HOST
import requests

LOG = logger()


class ProxyClient:

    def __init__(self):
        self.host = PROXY_HOST
        self.port = PROXY_PORT
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def auth(self):
        """
        认证
        :return:
        """
        sign1 = struct.pack('>i', 1)
        params = {"token": PROXY_TOKEN}
        params_byte = bytes(json.dumps(params), 'utf-8')
        params_len = len(params_byte)
        dump_params = struct.pack('>i', params_len)
        auth_params = sign1 + dump_params + params_byte

        return auth_params

    def get_proxy(self):
        """
        获取代理
        :return:
        """
        sign2 = struct.pack('>i', 2)
        params = {"count": PROXY_COUNT}
        params_byte = bytes(json.dumps(params), 'utf8')
        params_len = len(params_byte)
        dump_params = struct.pack('>i', params_len)
        proxy_params = sign2 + dump_params + params_byte
        return proxy_params

    def run(self):
        try:
            self.conn.connect((self.host, self.port))
            auth_params = self.auth()
            self.conn.send(auth_params)
            self.conn.recv(4)
            header_pack = self.conn.recv(4)
            header_len = struct.unpack('>i', header_pack)[0]
            header_byte = self.conn.recv(header_len)
            header = json.loads(header_byte.decode('utf-8'))
            if header.get('code') == 403:  # 认证失败
                return
            elif header.get('code') == 700:  # 无可用ip
                # 记录日志
                LOG.info('no proxies')
            elif header.get('code') == 200:
                proxy_params = self.get_proxy()
                self.conn.send(proxy_params)
                self.conn.recv(4)
                data_len = struct.unpack('>i', self.conn.recv(4))[0]
                data_byte = self.conn.recv(data_len)
                data = json.loads(data_byte.decode('utf-8'))
                proxies = data.get('ips')
                proxies_list = []
                for item in proxies:
                    ip_address = item.get('ip_address')
                    if ip_address:
                        ip = {'http': 'http://' + ip_address}
                        if ip not in proxies_list:
                            proxies_list.append(ip)
                return proxies_list
        except:
            self.conn.close()
            time.sleep(10)  # 断开连接后,每10s重新连接一次
            ProxyClient().run()


def get_remote_proxies():
    """
    获取远端代理
    :return:
    """
    client = ProxyClient()
    proxy_list = client.run()
    if proxy_list:
        print('已从远程端获取代理')
        # print(proxy_list)
        return proxy_list


def get_data5u_proxies():
    """
    获取data5u网站的代理
    :return:
    """
    print('正在获取data5u的代理')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    order = "258139f92232f62604502fd31d2dee54"
    api_url = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
    res = requests.get(api_url, headers=headers, timeout=(2, 5), verify=False)
    result = res.content.decode('utf-8')
    res.close()
    if 'too many request' not in result:
        result = result.split('\n')[:-1]
    else:
        # print('过频')
        time.sleep(2)
        res = requests.get(api_url, headers=headers, timeout=(2, 5), verify=False)
        result = res.content.decode('utf-8')
        res.close()
        if 'too many request' not in result:
            result = result.split('\n')[:-1]
        else:
            return
    proxies = [{'http': 'http://' + ip} for ip in result]
    return proxies


if __name__ == "__main__":
    get_remote_proxies()
