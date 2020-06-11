#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from conf.settings import *
from utils.logger import logger
from utils.proxy import get_remote_proxies, get_data5u_proxies
import random
from datetime import datetime, timedelta
import time
import re
import requests
import execjs
from Crypto.Cipher import AES
import base64
import pymysql
import requests
from json.decoder import JSONDecodeError
import re
from lxml.html import tostring
from bs4 import BeautifulSoup, Comment
from html import unescape
from lxml import etree
import redis
import pymongo
from apscheduler.schedulers.gevent import GeventScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import gc
from queue import Queue
import pytesseract
from PIL import Image

requests.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5

LOG = logger()


class BaseCrawl(object):
    """基本类"""
    proxy_dict = {
        1: get_remote_proxies,
        2: get_data5u_proxies,
        3: ''
    }

    def __init__(self, ):
        self._start_time = time.time()
        self.header = self.headers_list  # UA头
        self.proxies = None  # 代理
        self._temp_container = set()  # 临时容器
        self._formal_container = set()  # 正式容器
        self._error_container = set()  # 异常容器
        self._data_conn = None  # 数据句柄
        self._mysql_conn = None  # mysql的句柄
        self._data_conn_flag = None  # 数据库句柄类型，后续根据这个进行操作
        self.queue = Queue(maxsize=120)  # 队列

    @property
    def headers_list(self):
        """
        读取模板格式
        :return:
        """
        return USER_AGENT

    @property
    def get_headers(self):
        ua = random.choice(self.header)
        header = {
            'User-Agent': ua
        }
        return header

    def change_container(self, flag, types):
        """
        修改容器类型
        :param flag: 临时还是正式容器
        :param types: 要转成的类型
        :return:
        """
        _types_dict = {
            'list': list,
            'tuple': tuple,
            'dict': dict,
            'set': set
        }
        if flag not in ('temp', 'formal', 'error'):
            raise ValueError('需要指定目标容器')
        if types not in _types_dict:
            raise ValueError('不符合的容器类型')
        if flag == 'temp':
            self._temp_container = _types_dict[types](self._temp_container)
        if flag == 'formal':
            self._formal_container = _types_dict[types](self._formal_container)
        if flag == 'error':
            self._error_container = _types_dict[types](self._error_container)

    def get_proxy(self):
        """
        随机获取一个代理
        :return:
        """
        if self.proxies:
            proxies = random.choice(self.proxies)
            return proxies

    def get_proxies(self, is_online=False):
        """
        随机获取各个地方的代理池
        :param is_online: 是否是线上
        :return:
        """
        if not is_online:
            flag = random.randint(1, 3)
        else:
            flag = random.randint(1, 2)
        func = self.proxy_dict[flag]
        if func:
            self.proxies = func()
        else:
            self.proxies = None

    def time_to_timestemp(self, date):
        """
        转换日期格式为时间戳
        :return:
        """
        if not date:
            return

        if ':' in date:
            try:
                timestemp = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M")))
            except Exception:
                timestemp = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))
        else:
            timestemp = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        return timestemp

    def timestemp_to_time(self, times):
        """
        时间戳转为日期格式
        :param times: 时间戳
        :return:
        """
        time_array = time.localtime(times)
        style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return style_time

    def get_sleep_time(self):
        """
        获取一个随机不定的停顿时间
        :return:
        """
        # number = random.uniform(3, 5)
        number = random.uniform(0.8, 3)
        number = round(number, 2)
        return number

    def get_sleep_time_v2(self):
        """
        获取一个随机不定的停顿时间
        :return:
        """
        # number = random.uniform(3, 5)
        number = random.uniform(4, 8)
        number = round(number, 2)
        return number

    def filter_data(self, data):
        """
        过滤数据
        :param data: 待审核的数据
        :return:
        """
        # if not re.search(r'[\u4e00-\u9fa5]', data):  # 只有数字和字母，屏蔽掉
        #     return True
        for key in FILTER_KEYWORDS:  # 含有屏蔽关键词，屏蔽掉
            if key in data:
                return True

    def normal_request(self, url, data=None, is_solve=True, headers=None):
        """
        通用的请求函数
        :param url: 请求网址
        :param data: 请求参数
        :param is_solve: 是否需要对返回结果解码
        :param headers: 请求头，如果不带默认就是随机获取
        :return:
        """
        req = None
        proxy = self.get_proxy()
        try:
            headers = headers if headers else self.get_headers
            headers.update({'Connection': 'close'})
            if data:
                req = requests.post(url, headers=headers, data=data, verify=False, proxies=proxy,
                                    timeout=(3, 5))
            else:
                req = requests.get(url, headers=headers, verify=False, proxies=proxy, timeout=(3, 5))
        except Exception:
            headers = headers if headers else self.get_headers  # 错误请求后应该换下请求头，固定请求头除外
            headers.update({'Connection': 'close'})
            time.sleep(self.get_sleep_time_v2())
            # 先判断是否还有代理,删除上次出错的代理
            if proxy and self.proxies and proxy in self.proxies:
                self.proxies.remove(proxy)
                # 最后判断还有没有代理，没有就跳出去
                if not self.proxies:
                    self.get_proxies()
            try:
                # 拿到新的代理去请求
                proxy = self.get_proxy()
                if data:
                    req = requests.post(url, headers=headers, data=data, verify=False, proxies=proxy,
                                        timeout=(3, 5))
                else:
                    req = requests.get(url, headers=headers, verify=False, proxies=proxy, timeout=(3, 5))
            except Exception:
                pass
        if req and req.status_code == 200:
            if is_solve:  # 需要解析，返回已解析过的数据
                res = self.solve_response(req)
                if res:
                    return res
            else:  # 不需要解析直接返回response对象
                return req

    def solve_response(self, response, url=None):
        """
        对返回数据解码
        :param url: 解析链接
        :param response: 响应对象
        :return:
        """
        # 拿到请求体，接触数据
        result = ''
        try:
            result = response.content.decode('utf-8')
        except Exception:
            try:
                result = response.content.decode('gbk')
            except Exception:
                try:
                    result = response.content.decode('gb18030')
                except Exception:  # 数据异常
                    try:
                        result = response.text
                    except Exception:
                        try:
                            result = response.content.decode('utf-8', 'ignore')
                        except Exception:
                            try:
                                result = response.content.decode('gbk', 'ignore')
                            except Exception:
                                try:
                                    result = response.content.decode('gb18030', 'ignore')
                                except Exception as e:  # 数据异常
                                    LOG.error('decode_url__sp2__%s__sp1__error__sp2__%s' % (url, e))
        if result:
            return result

    def get_rsa_key(self, res, js=JS):
        """
        破解福建省的rsa加密
        :param res: 网址返回源码结果
        :param js: js的rsa加密方式
        :return:
        """
        start_index = res.index('function RsaFunc')
        end_index = res.index('var isReflash = false;')
        rsafunc = res[start_index:end_index]
        rsafunc += 'return RsaEncrypted;\n}'
        js += rsafunc
        cx = execjs.compile(js)
        cookie = cx.call('RsaFunc')
        return cookie

    def add_to_16(self, s):
        """
        转为16位编码
        :param s:
        :return:
        """
        while len(s) % 16 != 0:
            s += (16 - len(s) % 16) * chr(16 - len(s) % 16)
        return str.encode(s)  # 返回bytes

    def get_secret_url(self, text, key):
        """
        加密链接
        :param text: 待加密的字符串
        :param key: key值
        :return:
        """
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器，本例采用ECB加密模式
        encrypted_text = str(base64.encodebytes(aes.encrypt(self.add_to_16(text))), encoding='utf8').replace('\n',
                                                                                                             '')  # 加密
        encrypted_text = encrypted_text.replace('/', "^")  # ddd.replace(/\//g, "^")
        return encrypted_text[:-2]

    def get_real_url(self, first_url, key=AES_KEY):
        """
        aes加密
        :param first_url: 未加密的url
        :param key: key值
        :return:
        """
        aa = first_url.split('/')
        aaa = len(aa)
        bbb = aa[aaa - 1].split('.')
        ccc = bbb[0]
        secret_text = self.get_secret_url(ccc, key=key)
        return first_url.replace(ccc, secret_text)

    def get_file_name(self):
        """
        开始请求
        :param data:
        :return:
        """
        now = time.time()
        file_name = time.strftime("%Y%m%d%H%M%S", time.localtime(now))
        self.file = open('%s.txt' % str(file_name), 'w', encoding='utf-8')
        return file_name + '.txt'

    def get_redis_conn(self, pool=POOL):
        """
        创建连接数据库的句柄
        :return:
        """
        conn = redis.Redis(connection_pool=pool)
        return conn

    def get_mysql_conn(self):
        """
        获取mysql的句柄
        :return:
        """
        conn = pymysql.connect(host=REMOTE_MYSQL_HOST, port=REMOTE_MYSQL_PORT, user=REMOTE_MYSQL_USER,
                               passwd=REMOTE_MYSQL_PASSWORD, db=REMOTE_MYSQL_DB)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        self._mysql_conn = conn
        return cursor

    def get_mongodb_conn(self, db=''):
        """
        获取mongodb的句柄
        :param db:
        :return:
        """
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        return client

    def get_sql_cursor(self, sql_type, *args, **kwargs):
        """
        获取数据句柄
        :param sql_type: file,redis,mysql,mongodb
        :param args:
        :param kwargs:
        :return:
        """
        if sql_type == 'file':
            self._data_conn = self.get_file_name()
            self._data_conn_flag = 'file'
        elif sql_type == 'redis':
            self._data_conn = self.get_redis_conn()
            self._data_conn_flag = 'redis'
        elif sql_type == 'mysql':
            self._data_conn = self.get_mysql_conn()
            self._data_conn_flag = 'mysql'
        elif sql_type == 'mongodb':
            self._data_conn = self.get_mongodb_conn()
            self._data_conn_flag = 'mongodb'
        else:
            raise ValueError('不存在的数据库句柄')

    def save_file(self):
        """
        写入数据
        :return:
        """
        data = ''  # 从正式库读取数据
        if not data:
            print('没有数据')
            return
        file_name = self.get_file_name()  # 初始化输出文件
        print('正在存储数据到根目录下的文件 %s，请稍等片刻....' % file_name)
        for item in data:
            '业务逻辑'
            # self.file.write()
        print('已写入 %s 条信息' % len(data))
        # 备份当次已采集数据
        print('存储完毕！')

    def save_redis(self):
        """
        保存到redis
        :return:
        """
        conn = self.get_redis_conn(pool=FIRST_POOL)
        for item in self._formal_container:
            '业务逻辑'
            pass

        print('已保存')
        conn.close()

    def save_mongodb(self):
        """
        保存到mongodb
        :return:
        """

    def save_mysql(self):
        """
        保存到mysql
        :return:
        """
        sql = 'replace into ....'
        for item in self._formal_container:
            "业务逻辑"
            self._data_conn.execute(sql)
            pass
        self._mysql_conn.close()

    def save_data(self):
        """
        保存数据
        :return:
        """
        if not self._data_conn_flag:
            raise ValueError('输出数据库类型未知')
        if self._data_conn_flag == 'file':
            self.save_file()
        elif self._data_conn_flag == 'redis':
            self.save_redis()
        elif self._data_conn_flag == 'mongodb':
            self.save_mongodb()
        elif self._data_conn_flag == 'msyql':
            self.save_mysql()
        self._data_conn.close()

    def login_user(self):
        """
        登录组件
        :return:
        """
        login_url = ''
        data = "用户名,密码"
        self.normal_request(login_url, data=data)

    def get_apscheduler(self):
        """获取定时任务类"""
        cls = BlockingScheduler
        return cls()

    def move_data_queue(self):
        """
        移动数据到queue里
        :return:
        """
        if self.queue.full() or len(self.item_data) == 0:  # 队列已满或者数据为空，跳出去
            return
        print('正在移动数据到队列内')
        try:
            for i in range(120):
                if len(self._temp_container) == 0:  # 在取数据中途数据为空，跳出去
                    break
                item = self.item_data.pop()
                if self.queue.full():  # 队列存满，将数据再加回去退出
                    if item not in self.item_data:
                        self.item_data.append(item)
                    break
                else:  # 没存满，放进队列里
                    self.queue.put(item)
        except Exception as e:
            LOG.error('data to queue error__sp2__%s' % e)
        gc.collect()  # 不定期垃圾回收

    def save_data_redis(self):
        """
        保存
        :return:
        """
        if self.queue.empty():  # 如果队列里为空跳出去
            return
        conn = self.get_redis_conn()
        print('当前已获取 %s 条数据，正在保存中......' % self.queue.qsize())
        for i in range(120):
            if self.queue.empty():  # 如果队列里为空跳出去
                break
            item = self.queue.get()
            conn.lpush('data', json.dumps(item))
        print('已保存')
        conn.close()
        gc.collect()  # 不定期垃圾回收

    def deduplicate(self,data):
        """
        去重
        :return:
        """
        # 根据实际情况去重

    def get_current_time(self):
        """
        获取当前时间戳
        :return:
        """
        return time.time()

    def get_execute_time(self):
        """
        耗时组件
        :return:
        """
        print('总共用时 %s'%(self.get_current_time() - self._start_time))

    def crawl(self):
        '业务逻辑'
        pass

    def ocr_get_data(self,data):
        """
        ocr提取
        :param data: 图片名
        :return:
        """
        img_path = os.path.join(BASE_DIR,data)
        if not os.path.exists(img_path):
            raise ValueError('图片位置有误')
        if not os.path.isfile(img_path):
            raise ValueError('不是文件')
        pytesseract.pytesseract.tesseract_cmd = OCR_PATH

        data = pytesseract.image_to_string(Image.open(img_path),
                                           config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        if data:
            return data

    def regex_data(self,part,data,flag):
        """
        正则匹配组件
        :param part: 正则表达式
        :param data: 待匹配数据
        :param flag: 全部还是只是某一个
        :return:
        """
        function = getattr(re,flag)
        if function:
            data = function(part,data,re.S)
            return data


    def error_level(self):
        """异常等级"""
        error_dict = {
            0:'warning',
            1:'error',
            2:''
        }

    def freed_memory(self):
        """
        释放内存
        :return:
        """
        gc.collect()

    def auth_area(self,area, source):
        """
        验证匹配的地区是否属于当前省市来源网址
        :param area: 地区
        :param source: 来源网址名
        :return:
        """
        if not area or not source:
            return
        # 查询到来源对应的省市
        current_province = None
        for province in CITY_PROVINCE:
            if province in source:
                current_province = province  # 这里其实可以直接使用city变量，但是多线程时怕数据有误
                break
        # 从省市去取从属的所有地区名数组
        citys = CITYLIST.get(current_province)
        if not citys:
            area = '全国'
        else:
            # 验证当前匹配的地区名是否在地区名数组内
            if area not in citys:
                area = current_province
        return area


    def run(self):
        """
        入口方法
        :return:
        """
        # 获取定时对象
        sched = self.get_apscheduler()
        # 一定时间内将数据存入queue内
        sched.add_job(self.move_data_queue, 'interval', seconds=APS_QUEUE_INTERVAL, max_instances=3)
        # 一定时间内将queue中的数据存库
        sched.add_job(self.save_data_redis, 'interval', seconds=APS_REDIS_INTERVAL, max_instances=3)
        # 启动定时任务
        sched.start()
        # 程序启动时立即运行
        self.crawl()
        # try:
        #     # 获取定时对象
        #     sched = self.get_apscheduler()
        #     # 一定时间内将数据存入queue内
        #     sched.add_job(self.move_data_queue, 'interval', seconds=APS_QUEUE_INTERVAL, max_instances=3)
        #     # 一定时间内将queue中的数据存库
        #     sched.add_job(self.save_data_redis, 'interval', seconds=APS_REDIS_INTERVAL, max_instances=3)
        #     # 启动定时任务
        #     sched.start()
        #     # 程序启动时立即运行
        #     self.request_sites()
        #     # 从错误日志里读取，这个暂时用不到，不开启
        #     # self.get_log_urls()
        # except Exception as e:
        #     LOG.error('run_function__sp2__%s' % e)

        # 如果还有数据没存完
        if self.item_data:
            self.item_data = self.deduplicate(self._formal_container)
            self.move_data_queue()
            # 存库
            self.save_data_redis()


