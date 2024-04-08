"""从 resonance.breadio.wiki 获取价格表
"""

import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0'
}


def get_price_table():
    data = requests.get(
        'https://resonance.breadio.wiki/api/product',
        headers=HEADERS
    ).json()
    prices = data.get("latest")
    from . import CityEnum, Product, GameData
    for item in prices:
        product_name = item.get("name", None)
        city_name = item.get("targetCity", None)
        if product_name == None or city_name == None:
            continue
        try:
            product = Product[product_name]
            city = CityEnum[city_name]
            price = item.get("price", None)
            assert isinstance(price, int) or isinstance(price, float)
            # print(f"价格更新: {city} {product} {price}")
            GameData.price[city.value - 1, product.value - 1] = item.get("price")
        except:
            continue
