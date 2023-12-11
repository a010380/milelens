# pycharm中如果無法引入自定義模塊，要先在pycharm中右鍵點擊項目根目錄->標記目錄為Resource Root，然後再右鍵點擊項目根目錄->根源。這樣就能引用項目根目錄下的所有自定義模塊了。
import sys
import os
dir_common = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(dir_common)   # 將根目錄添加到系統目錄,才能正常引用其他文件的內容
print('系統根目錄',dir_common)

