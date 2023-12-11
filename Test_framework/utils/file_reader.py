# 用於文件的讀取,包含配置文件和數據文件的讀取函數.根據文件地址，返回文件中包含的內容

import yaml
import os
from xlrd import open_workbook

# 讀取配置文件yaml文件成配置內容
class YamlReader:
    def __init__(self, yamlfilepath):
        if os.path.exists(yamlfilepath):
            self.yamlfilepath = yamlfilepath
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        # 如果是第一次調用data，讀取yaml文檔，否則直接返回之前保存的數據
        if not self._data:
            with open(self.yamlfilepath, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # load後是個generator，用list組織成列表
        return self._data


class SheetTypeError(Exception):
    pass

# 讀取excel文件中的內容。返回list。
class ExcelReader:
    """
    如：
    excel中內容為：
    | A  | B  | C  |
    | A1 | B1 | C1 |
    | A2 | B2 | C2 |

    如果 print(ExcelReader(excel, title_line=True).data)，輸出結果：
    [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

    如果 print(ExcelReader(excel, title_line=False).data)，輸出結果：
    [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

    可以指定sheet，通過index或者name：
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='BaiDuTest')
    """
    def __init__(self, excelpath, sheet=0, title_line=True):
        if os.path.exists(excelpath):
            self.excelpath = excelpath  # excel文件路徑
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet   # sheet可以是int表示表格的索引，可以是str表示表格的名稱
        self.title_line = title_line  # 是否存在標題行，有標題行，每一行都是都是對應列名的取值；沒有標題行，每一行都是一個列表
        self._data = list()   # 用於存儲每行生成的數據。

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excelpath)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)  # 首行為title
                for col in range(1, s.nrows):
                    # 依次遍歷其余行，與首行組成dict，拼到self._data中
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):
                    # 遍歷所有行，拼到self._data中
                    self._data.append(s.row_values(col))
        return self._data



if __name__ == '__main__':

    y = 'E:\Test_framework\config\config.yml'
    reader = YamlReader(y)
    print(reader.data)

    e = 'E:/Test_framework/data/baidu.xlsx'
    reader = ExcelReader(e, title_line=True)
    print(reader.data)