"""
在這里添加各種自定義的斷言（測試結果和目標結果是否一致的判斷），斷言失敗拋出AssertionError就OK。
"""

# 判斷http的響應碼和預期狀態碼是否一致
def assertHTTPCode(response, code_list=None):
    res_code = response.status_code
    if not code_list:
        code_list = [200]
    if res_code not in code_list:
        raise AssertionError('響應code不在列表中！')  # 拋出AssertionError，unittest會自動判別為用例Failure，不是Error

def assertNormalError():
    raise AssertionError('errrrror')

def assertVariableError(param):
    if param == False:
        raise AssertionError('沒有' + param)

def assertAnalysisError(param):
    raise AssertionError(param + '這邊有錯誤')