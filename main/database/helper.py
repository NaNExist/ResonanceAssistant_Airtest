#!/usr/bin/python3

SRC = "https://github.com/kmou424/resonance-resodata/raw/main/goods_cities_mapper.json"

import json
from typing import Literal

from dataclasses import dataclass
import pandas as pd
import requests

data: list = requests.get(SRC).json()


#   {
#     "base_price": 803,
#     "id": "addf373d14f4",
#     "name": "白兰地",
#     "station": "7号自由港",
#     "stock": 24,
#     "type": "buy"
#   },

@dataclass
class DataItem:
    base_price: float
    id: str
    name: str
    station: str
    stock: int
    type: Literal["buy", "sell"]
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DataItem':
        return cls(**data)


city_product = {}
prices = pd.DataFrame()

# 城市,发动机,汽配零件,家电
# 修格里城,3363,720,848
# 铁盟哨站,3464,742,848

for item in data:
    if isinstance(item, str):
        continue
    try:
        item = DataItem.from_dict(item)
        if item.type == "sell":
            if item.station not in city_product:
                city_product[item.station] = {}
            city_product[item.station][item.name] = item.stock
        # if item.station not in prices.index:
        #     prices.index.append(item.station)
        prices.loc[item.station, item.name] = item.base_price
    except:
        continue
    

with open("out_城市商品表.json", "w") as f:
    f.write(json.dumps(city_product, ensure_ascii=False, indent=4))

prices.to_csv("out_基础价格表.csv")

