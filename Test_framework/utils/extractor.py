# 抽取器，從響應結果中抽取部分數據，這里實現的是json返回數據的抽取，可以自己添加XML格式、普通字符串格式、Header的抽取器

import json
import jmespath
from utils.client import HTTPClient

# 完成了對JSON格式的抽取器，如果返回結果是JSON串，我們可以通過這個抽取器找到我們想要的數據，再進行下一步的操作，或者用來做斷言。
class JMESPathExtractor(object):
    """
    用JMESPath實現的抽取器，對於json格式數據實現簡單方式的抽取。
    """
    def extract(self, query=None, body=None):
        try:
            return jmespath.search(query, json.loads(body))
        except Exception as e:
            raise ValueError("Invalid query: " + query + " : " + str(e))


if __name__ == '__main__':

    res = HTTPClient(url='http://wthrcdn.etouch.cn/weather_mini?citykey=101010100').send()
    print(res.text)
    # {"data": {
    #     "yesterday": {"date": "17日星期四", "high": "高溫 31℃", "fx": "東南風", "low": "低溫 22℃", "fl": "<![CDATA[<3級]]>",
    #                   "type": "多雲"},
    #     "city": "北京",
    #     "aqi": "91",
    #     "forecast": [
    #         {"date": "18日星期五", "high": "高溫 28℃", "fengli": "<![CDATA[<3級]]>", "low": "低溫 22℃", "fengxiang": "東北風",
    #          "type": "多雲"},
    #         {"date": "19日星期六", "high": "高溫 29℃", "fengli": "<![CDATA[<3級]]>", "low": "低溫 22℃", "fengxiang": "東風",
    #          "type": "雷陣雨"},
    #         {"date": "20日星期天", "high": "高溫 29℃", "fengli": "<![CDATA[<3級]]>", "low": "低溫 23℃", "fengxiang": "東南風",
    #          "type": "陰"},
    #         {"date": "21日星期一", "high": "高溫 30℃", "fengli": "<![CDATA[<3級]]>", "low": "低溫 24℃", "fengxiang": "西南風",
    #          "type": "晴"},
    #         {"date": "22日星期二", "high": "高溫 29℃", "fengli": "<![CDATA[<3級]]>", "low": "低溫 24℃", "fengxiang": "北風",
    #          "type": "雷陣雨"}
    #     ],
    #     "ganmao": "各項氣象條件適宜，無明顯降溫過程，發生感冒機率較低。", "wendu": "25"
    #  },
    # "status": 1000,
    # "desc": "OK"}

    j = JMESPathExtractor()
    j_1 = j.extract(query='data.forecast[1].date', body=res.text)
    j_2 = j.extract(query='data.ganmao', body=res.text)
    print(j_1, j_2)
