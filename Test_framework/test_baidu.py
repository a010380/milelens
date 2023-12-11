import os
import time
import unittest  # 單元測試模塊
from selenium import webdriver  # 引入瀏覽器驅動
from selenium.webdriver.common.by import By  # 引入xpath查找模塊
from utils.config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH  # 引入配置
from utils.log import logger # 引入日志模塊
from utils.file_reader import ExcelReader  # 引入xls讀取模塊
from utils.HTMLTestRunner import HTMLTestRunner
from utils.mail import Email
from test.page.milelens_result_page import MilelensLoginPage, MilelensResultPage

class TestBaiDu(unittest.TestCase):
    URL = Config().get('URL')
    excel = DATA_PATH + '/milelens.xlsx'

    def sub_setUp(self):
        # 初始頁面是Milelens Login page，傳入瀏覽器類型打開瀏覽器
        self.page = MilelensLoginPage(browser_type='chrome').get(self.URL, maximize_window=True)

    def sub_tearDown(self):
        pass

    def test_search(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            with self.subTest(data=d):
                self.sub_setUp()
                self.page.login('kson01@mailnesia.com', 'Pass1234')   #回推到19行 self.page = MilelensLoginPage(browser_type='chrome').get(self.URL, maximize_window=True)
                time.sleep(2)


                self.page = MilelensResultPage(self.page)  # 頁面跳轉到result page
                links = self.page.result_links
                for link in links:
                    logger.info(link.text)
                self.sub_tearDown()

if __name__ == '__main__':
    unittest.main()

    report = REPORT_PATH + '\\report.html'
    print(report)
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='克森全站', description='修改html報告')
        runner.run(TestBaiDu('test_search'))

    # e = Email(title='百度搜索測試報告',
    #           message='這是今天的測試報告，請查收！',
    #           receiver='...',
    #           server='...',
    #           sender='...',
    #           password='...',
    #           path=report
    #           )
    # e.send()