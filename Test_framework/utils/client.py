"""
添加用於測試後台接口的前端client，對於HTTP接口添加HTTPClient，發送http請求。
還可以封裝TCPClient，用來進行tcp鏈接，測試socket接口等等。
"""

import requests
import socket
import json
import requests
import time
import asyncio
from utils.log import logger

METHODS = ['GET', 'POST', 'HEAD', 'TRACE', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']  # 所有支持的前後前交互方法


class UnSupportMethodException(Exception):
    """當傳入的method的參數不是支持的類型時拋出此異常。"""
    pass

# http請求的client。初始化時傳入url、method等，可以添加headers和cookies，但沒有auth、proxy。
class HTTPClient(object):

    def __init__(self, url, method='GET', headers=None, cookies=None):
        """headers: 字典。 例：headers={'Content_Type':'text/html'}，cookies也是字典。"""
        self.url = url
        self.session = requests.session()
        self.method = method.upper()
        if self.method not in METHODS:
            raise UnSupportMethodException('不支持的method:{0}，請檢查傳入參數！'.format(self.method))

        self.set_headers(headers)
        self.set_cookies(cookies)

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    def set_cookies(self, cookies):
        if cookies:
            self.session.cookies.update(cookies)

    def send(self, params=None, data=None, **kwargs):
        response = self.session.request(method=self.method, url=self.url, params=params, data=data, **kwargs)
        response.encoding = 'utf-8'
        logger.debug('{0} {1}'.format(self.method, self.url))
        logger.debug('請求成功: {0}\n{1}'.format(response, response.text))
        return response

# 用於測試TCP協議的socket請求，對於WebSocket，socket.io需要另外的封裝
class TCPClient(object):

    def __init__(self, domain, port, timeout=30, max_receive=102400):
        self.domain = domain
        self.port = port
        self.connected = 0  # 連接後置為1
        self.max_receive = max_receive
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(timeout)

    def connect(self):
        """連接指定IP、端口"""
        if not self.connected:
            try:
                self._sock.connect((self.domain, self.port))
            except socket.error as e:
                logger.exception(e)
            else:
                self.connected = 1
                logger.debug('TCPClient connect to {0}:{1} success.'.format(self.domain, self.port))

    def send(self, data, dtype='str', suffix=''):
        """向服務器端發送send_string，並返回信息，若報錯，則返回None"""
        if dtype == 'json':
            send_string = json.dumps(data) + suffix
        else:
            send_string = data + suffix
        self.connect()
        if self.connected:
            try:
                self._sock.send(send_string.encode())
                logger.debug('TCPClient Send {0}'.format(send_string))
            except socket.error as e:
                logger.exception(e)

            try:
                rec = self._sock.recv(self.max_receive).decode()
                if suffix:
                    rec = rec[:-len(suffix)]
                logger.debug('TCPClient received {0}'.format(rec))
                return rec
            except socket.error as e:
                logger.exception(e)

    def close(self):
        """關閉連接"""
        if self.connected:
            self._sock.close()
            logger.debug('TCPClient closed.')


# 異步並發客戶端
class Asyncio_Client(object):

    def __init__(self):
        self.loop=asyncio.get_event_loop()
        self.tasks=[]

    # 將異步函數介入任務列表。後續參數直接傳給異步函數
    def set_task(self,task_fun,num,*args):
        for i in range(num):
            self.tasks.append(task_fun(*args))

    # 運行，獲取返回結果
    def run(self):
        back=[]
        try:
            f = asyncio.wait(self.tasks)   # 創建future
            self.loop.run_until_complete(f)  # 等待future完成
        finally:
            pass
            # self.loop.run_forever()
            # self.loop.close()  # 當輪訓器關閉以後，所有沒有執行完成的協成將全部關閉