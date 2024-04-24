"""从 索思学会 获取价格表，此处uuid为故意错误部分
"""

import requests
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0'
}


def get_price_table():
    # 注意请求不要太频繁
    data = requests.get(
        'https://reso-data.kmou424.moe/api/fetch/goods_info?uuid=X',
        headers=HEADERS
    ).json()
    with open("../setting/price_inf.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


get_price_table()

