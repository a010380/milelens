"""
日誌類。通過讀取配置文件，定義日誌級別、日誌文件名、日誌格式等。
一般直接把logger import進去
from utils.log import logger
logger.info('test log')
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from .config import LOG_PATH, Config


class Logger(object):
    def __init__(self, logger_name='framework'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        c = Config().get('log')
        self.log_file_name = c.get('file_name') if c and c.get('file_name') else 'test.log'  # 日誌文件
        self.backup_count = c.get('backup') if c and c.get('backup') else 5  # 保留的日誌數量
        # 日誌輸出級別
        self.console_output_level = c.get('console_level') if c and c.get('console_level') else 'WARNING'
        self.file_output_level = c.get('file_level') if c and c.get('file_level') else 'DEBUG'
        # 日誌輸出格式
        pattern = c.get('pattern') if c and c.get('pattern') else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.formatter = logging.Formatter(pattern)

    def get_logger(self):
        """在logger中添加日誌句柄並返回，如果logger已有句柄，則直接返回
        我們這里添加兩個句柄，一個輸出日誌到控制台，另一個輸出到日誌文件。
        兩個句柄的日誌級別不同，在配置文件中可設置。
        """
        if not self.logger.handlers:  # 避免重覆日誌
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 每天重新創建一個日誌文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH, self.log_file_name),
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger

logger = Logger().get_logger()