import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from .browser import Browser
from utils.log import logger
import os, logging
from utils.config import DRIVER_PATH, REPORT_PATH
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 瀏覽器頁面類，主要進行瀏覽器頁面的控制，包括獲取
class Page(Browser):
    def __init__(self, page=None, browser_type='firefox'):
        if page:
            self.driver = page.driver
        else:
            super(Page, self).__init__(browser_type=browser_type)

    # 獲取當前窗口句柄
    @property
    def current_window(self):
        return self.driver.current_window_handle

    #獲取標題
    @property
    def title(self):
        return self.driver.title

    # 獲取當前網址
    @property
    def current_url(self):
        return self.driver.current_url

    # 獲取瀏覽器驅動
    def get_driver(self):
        return self.driver

    # 睡眠一段時間
    def wait(self, seconds=4):
        time.sleep(seconds)

    # 睡眠一段時間
    def free_wait(self, seconds):
        time.sleep(seconds)

    # 隱性等待
    def implicitly_wait(self, seconds=5):
        self.driver.implicitly_wait(seconds)

    # 顯性等待
    def explicitly_wait(self, element):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element)
            )
            logging.info('等待到定位!!!!!!!!!!!!')
            return element
        except:
            logging.error('等待不到定位')
            logging.info('element: ' + element)

    # 執行js腳本
    def execute(self, js, *args):
        self.driver.execute_script(js, *args)

    # 移動到指定元素
    def move_to(self, element):
        ActionChains(self.driver).move_to_element(element).perform()

    # 尋找指定元素
    def find_element(self, *args):
        return self.driver.find_element(*args)

    # 尋找指定的一批元素
    def find_elements(self, *args):
        return self.driver.find_elements(*args)

    # 切換窗口
    def switch_to_window(self, partial_url='', partial_title=''):
        """切換窗口
            如果窗口數<3,不需要傳入參數，切換到當前窗口外的窗口；
            如果窗口數>=3，則需要傳入參數來確定要跳轉到哪個窗口
        """
        all_windows = self.driver.window_handles
        if len(all_windows) == 1:
            logger.warning('只有1個window!')
            self.driver.switch_to.window(all_windows[0])
        elif len(all_windows) == 2:
            other_window = all_windows[1 - all_windows.index(self.current_window)]
            self.driver.switch_to.window(other_window)
        else:
            for window in all_windows:
                self.driver.switch_to.window(window)
                if partial_url in self.driver.current_url or partial_title in self.driver.title:
                    break
        # logger.debug(self.driver.current_url, self.driver.title)
    
    # 切換窗口
    def switchto_window(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
    
    # 返回到主要的瀏覽器窗口或分頁
    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    # 切換frame頁面
    def switch_to_frame(self, param):
        self.driver.switch_to.frame(param)

    # 切換alter
    def switch_to_alert(self):
        return self.driver.switch_to.alert

    # 頁面重新整理
    def refresh(self):
        self.driver.refresh()

    # 上一頁
    def back(self):
        self.driver.back()

    # 執行js
    def execute_script(self, param):
        self.driver.execute_script(param)

    # 畫面往下滑動x pixel
    def scroll_script(self, param):
        self.driver.execute_script("window.scrollBy(0, " + param + ");")

    # 儲存螢幕截圖
    def save_screen_shot(self, name='screen_shot'):
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        screenshot_path = REPORT_PATH + '/screenshot_%s' % day
        print('screenshot_path: ' + screenshot_path)
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)

        tm = time.strftime('%H%M%S', time.localtime(time.time()))
        screenshot = self.driver.save_screenshot(screenshot_path + '/%s_%s.png' % (name, tm))
        print(screenshot_path + '/%s_%s.png' % (name, tm))
        return screenshot

    # 關閉分頁
    def driver_close(self):
        self.driver.close()

    # 將文字轉數字，如果有逗點的話把它刪掉
    def change_to_int(self, param):
        if ',' in param:
            param = param.replace(',', '')
        param = int(param)
        return param
    
    # 檢查網頁存在該關鍵字有幾個
    def check_page_source(self, param):
        keyword_count = self.driver.page_source.count(param)
        return keyword_count
    
    # 使用 ActionChains 模擬 Command + W 鍵盤快捷鍵
    def close_tab(self):
        ActionChains(self.driver).key_down(Keys.COMMAND).send_keys('w').key_up(Keys.COMMAND).perform()