"""
項目公共內容配置，以及讀取配置文件中的配置。這里配置文件用的yaml，也可用其他如XML,INI等，需在file_reader中添加相應的Reader進行處理。
"""
import os
from .file_reader import YamlReader

# 所有相關文件的路徑

# 通過當前文件的絕對路徑，其父級目錄一定是框架的base目錄，然後確定各層的絕對路徑。如果你的結構不同，可自行修改。
# 之前直接拼接的路徑，修改了一下，用現在下面這種方法，可以支持linux和windows等不同的平台，也建議大家多用os.path.split()和os.path.join()，不要直接+'\\xxx\\ss'這樣 
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
print(f"""
BASE_PATH={BASE_PATH}
CONFIG_FILE={CONFIG_FILE}
DATA_PATH={DATA_PATH}
DRIVER_PATH={DRIVER_PATH}
LOG_PATH={LOG_PATH}
REPORT_PATH={REPORT_PATH}
""")


class Config:
    def __init__(self, config=CONFIG_FILE):
        print('配置文件地址：',config)
        self.config = YamlReader(config).data

    def get(self, element, index=0):
        """
        yaml是可以通過'---'分節的。用YamlReader讀取返回的是一個list，第一項是默認的節，如果有多個節，可以傳入index來獲取。
        這樣我們其實可以把框架相關的配置放在默認節，其他的關於項目的配置放在其他節中。可以在框架中實現多個項目的測試。
        """
        return self.config[index].get(element)