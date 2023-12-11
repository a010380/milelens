import logging
logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)  # 輸出所有大於INFO等級的log
fmt = logging.Formatter('%(name)s - %(levelname)s - %(asctime)s - %(message)s')
# 新增StreamHandler，並設定等級為WARNING
stream_hdl = logging.StreamHandler()
stream_hdl.setLevel(logging.DEBUG)
stream_hdl.setFormatter(fmt)
logger.addHandler(stream_hdl)
# 新增FileHandler，並設定等級為DEBUG
file_hdl = logging.FileHandler('test.log')
file_hdl.setLevel(logging.DEBUG)
file_hdl.setFormatter(fmt)
logger.addHandler(file_hdl)

logger.info('I am <info> message.')
logger.debug('I am <debug> message.')  # 不輸出