# 在命令行執行python test_load.py來運行
import sys
import os
BASE_PATH = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
BASE_PATH = os.path.dirname(BASE_PATH)
sys.path.append(BASE_PATH)   # 將根目錄添加到系統目錄,才能正常引用其他文件的內容


import unittest
from utils.config import Config, REPORT_PATH,DATA_PATH
from utils.client import Asyncio_Client
from utils.log import logger
from utils.file_reader import YamlReader
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode
import requests,urllib
import random
import time
import io,os
import asyncio,aiohttp

# 服務器高並發壓力測試
class Test_Load(unittest.TestCase):

    config = Config()
    url = config.get('local_url')    # 集群測試
    url = config.get('api_url')      #  華為api網關測試
    print('測試網址：',url)
    images = config.get('images')     # 測試圖片

    num=int(config.get('num'))
    print('測試並發量：', num)
    total_time=0  # 總耗時
    total_payload=0  # 總負載
    total_num=0  # 總並發數
    all_time=[]

    # 設置訪問網址和請求方式
    def setUp(self):
        self.client = Asyncio_Client()
        print('準備工作')


    # 創建一個異步任務
    async def task_func(self):
        data = {'image_id': 2}
        begin = time.time()
        print('開始發送：', begin)
        files = {'image': open(self.image, 'rb')}  # open的目錄啟動命令的目錄，我在server.py目錄啟動，所以使用的這個路徑
        r = requests.post(self.url,data=data,files=files)
        print(r.text)
        end = time.time()
        self.total_time += end - begin
        print('接收完成：', end)

    # 創建一個異步任務，本地測試，所以post和接收幾乎不損耗時間，可以等待完成，主要耗時為算法模塊
    async def task_func1(self,session):

        begin = time.time()
        # print('開始發送：', begin)
        file=open(self.image, 'rb')
        fsize = os.path.getsize(self.image)
        self.total_payload+=fsize/(1024*1024)

        data = {"image_id": "2", 'image':file}
        r = await session.post(self.url,data=data)  #只post，不接收
        result = await r.json()
        self.total_num+=1
        # print(result)
        end = time.time()
        # print('接收完成：', end,',index=',self.total_num)
        self.all_time.append(end-begin)

    # 負載測試
    def test_safety(self):

        print('test begin')
        async_client = Asyncio_Client()  # 創建客戶端
        session = aiohttp.ClientSession()
        for i in range(1):  # 執行10次
            self.all_time=[]
            self.total_num=0
            self.total_payload=0
            self.image = DATA_PATH + "/" + self.images[0]  # 設置測試nayizhang
            print('測試圖片：', self.image)
            begin = time.time()
            async_client.set_task(self.task_func1,self.num,session)  # 設置並發任務
            async_client.run()   # 執行任務

            end=time.time()
            self.all_time.sort(reverse=True)
            print(self.all_time)
            print('並發數量(個)：',self.total_num)
            print('總耗時(s)：',end-begin)
            print('最大時延(s)：',self.all_time[0])
            print('最小時延(s)：', self.all_time[len(self.all_time)-1])
            print('top-90%時延(s)：', self.all_time[int(len(self.all_time)*0.1)])
            print('平均耗時(s/個)：',sum(self.all_time)/self.total_num)
            print('支持並發率(個/s):',self.total_num/(end-begin))
            print('總負載(MB)：',self.total_payload)
            print('吞吐率(MB/S)：',self.total_payload/(end-begin))   # 吞吐率受上行下行帶寬，服務器帶寬，服務器算法性能諸多影響

            time.sleep(3)


        session.close()
        print('test finish')



if __name__ == '__main__':
    suite = unittest.TestSuite()   # 創建測試組


    tests = [Test_Load("test_safety")]  # 添加測試用例列表
    suite.addTests(tests)  # 將測試用例列表添加到測試組中
    # 直接將結果輸出到控制台
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    # 將測試結果輸出到測試報告
    # report = REPORT_PATH + '/report.html'
    # with open(report, 'wb') as f:
    #     runner = HTMLTestRunner(f, verbosity=2, title='華為鑒黃', description='壓力測試html報告')
    #     runner.run(suite)