"""存放数据结构
"""

from __future__ import annotations

import enum
import json
from pathlib import Path
import numpy as np
import pandas as pd

from dataclasses import dataclass
from functools import cached_property

from typing import List, Dict


class CityEnum(enum.IntEnum):
    """城市枚举类

    ## Examples

    - 可以用 `CityEnum.修格里城` 来访问修格里城这个城市
    - 也可以用 `CityEnum["修格里城"]` 来访问修格里城这个城市
    - 还可以用 `CityEnum(1)` 来访问修格里城这个城市

    注意: 编号从 1 开始
    """
    修格里城 = enum.auto()
    七号自由港 = enum.auto()
    """沟槽的, 记得特殊处理, 一般字符串可能是 `"7号自由港"` """
    澄明数据中心 = enum.auto()
    阿妮塔能源研究所 = enum.auto()
    曼德矿场 = enum.auto()
    淘金乐园 = enum.auto()
    铁盟哨站 = enum.auto()
    荒原站 = enum.auto()
    阿妮塔战备工厂 = enum.auto()
    
    def __getitem__(self: type[enum._EnumMemberT], name: str) -> enum._EnumMemberT:
        if name == "7号自由港":
            return self["七号自由港"]
        return super().__getitem__(name)
    
    @enum.DynamicClassAttribute
    def name(self):
        __name = super(CityEnum, self).name
        if __name == "七号自由港":
            return "7号自由港"
        return __name

    def __repr__(self) -> str:
        return f"城市({self.name})"

    def __str__(self) -> str:
        return self.__repr__()


CITIES: List[City] = list(CityEnum)
"""可用城市列表"""


class Product(enum.IntEnum):
    """商品类

    注意: 编号从 1 开始
    """

    # TODO: Complete this
    发动机 = enum.auto()
    # 弹丸加速装置 = enum.auto()
    红茶 = enum.auto()
    沃德烤鸡 = enum.auto()
    高档餐具 = enum.auto()
    罐头 = enum.auto()
    沃德山泉 = enum.auto()
    沙金 = enum.auto()
    青金石 = enum.auto()
    漆黑矿渣 = enum.auto()
    玛瑙 = enum.auto()
    # 铁矿石 = enum.auto()
    # 石英砂 = enum.auto()
    阿妮塔202军用无人机 = enum.auto()
    铅矿石 = enum.auto()
    精钢 = enum.auto()
    黄铜 = enum.auto()
    曼德工具箱 = enum.auto()
    修格里严选礼包 = enum.auto()
    电子配件 = enum.auto()
    充电电池 = enum.auto()
    钛矿石 = enum.auto()
    海盐 = enum.auto()
    录像带 = enum.auto()
    石材 = enum.auto()
    斑节虾 = enum.auto()
    啤酒 = enum.auto()
    形态共振瞄准器 = enum.auto()
    铁轨用特种钢材 = enum.auto()
    黄铜线圈 = enum.auto()
    火澄石 = enum.auto()
    高导磁硅钢片 = enum.auto()
    子弹 = enum.auto()
    靛红五月军用食品 = enum.auto()
    年货大礼包 = enum.auto()
    录音带 = enum.auto()
    负片炮弹 = enum.auto()
    火车玩具 = enum.auto()
    石墨 = enum.auto()
    锂电池 = enum.auto()
    汽配零件 = enum.auto()
    石英矿 = enum.auto()
    绿松石 = enum.auto()
    人工晶花 = enum.auto()
    荧光棒 = enum.auto()
    扬声器 = enum.auto()
    阿妮塔101民用无人机 = enum.auto()
    钢筋混凝土轨枕 = enum.auto()
    抗污染防护服 = enum.auto()
    坚果 = enum.auto()
    建材 = enum.auto()
    家用太阳能电池组 = enum.auto()
    桦石发财树 = enum.auto()
    土豆 = enum.auto()
    汽油 = enum.auto()
    塑胶炸药 = enum.auto()
    砂石 = enum.auto()
    钛合金 = enum.auto()
    航天纪念品 = enum.auto()
    碳纤维 = enum.auto()
    游戏卡带 = enum.auto()
    家电 = enum.auto()

    def __repr__(self) -> str:
        return f"商品({self.name})"

    def __str__(self) -> str:
        return self.__repr__()


PRODUCTS: List[Product] = list(Product)
"""可用商品列表"""

# TODO: consider move this to json
CITY_PRODUCT_MAP: Dict[CityEnum, Product] = {
    CityEnum.修格里城: [
        Product["发动机"],
        # Product["弹丸加速装置"],
        Product["红茶"],
        Product["沃德烤鸡"],
        Product["高档餐具"],
        Product["罐头"],
        Product["沃德山泉"],
    ],
    CityEnum.淘金乐园: [
        Product["沙金"],
        Product["青金石"],
        Product["漆黑矿渣"],
        Product["玛瑙"],
        # Product["铁矿石"],
        # Product["石英砂"],
    ],
}

# TODO: 价格表有缺项, 补全后启用
# CITY_PRODUCT_TABLE_FNAME = "城市商品表.json"
# CITY_PRODUCT_TABLE_DIR = Path(__file__).parent / CITY_PRODUCT_TABLE_FNAME
# __table = {}
# with open(CITY_PRODUCT_TABLE_DIR, "r") as f:
#     __table = json.load(f)

# for city_name in __table:
#     CITY_PRODUCT_MAP[CityEnum[city_name]] = list(map(Product.__getitem__, __table[city_name]))


class City:
    """城市类
    """

    def __init__(self, name: str) -> None:
        try:
            self.id: CityEnum = CityEnum[name]
        except KeyError:
            raise ValueError(f"City {name} is not available now")

    def travel_cost(self, target: City) -> int:
        """不考虑用户的其他加成(即无加成)时两站之间行驶的疲劳值消耗"""
        # TODO: Make this not fixed
        return 25

    def __repr__(self) -> str:
        return f"城市({self.id.name})"

    @cached_property
    def products(self) -> list[Product]:
        try:
            return list(map(Product, CITY_PRODUCT_MAP[self.id.name]))
        except KeyError:
            raise ValueError(f"快催开发者添加城市 {self.id} 的商品列表")
        finally:
            return []

    @property
    def tax_rate(self):
        """固定税率, 这里取 8% 作为平均估计"""
        # TODO: Make this not fixed
        return 0.08

# 加载基础价格表并检查其格式(确保包含所有代码中用到的商品和城市)


DEFAULT_PRICE_TABLE_FNAME = "基础价格表.csv"

DEFAULT_PRICE_TABLE_DIR = Path(__file__).parent / DEFAULT_PRICE_TABLE_FNAME

DEFAULT_PRICE: pd.DataFrame = pd.read_csv(DEFAULT_PRICE_TABLE_DIR, index_col=0)

# TO ndarry

# Check if all cities and products are included

try:
    assert all((city.name in DEFAULT_PRICE.index) for city in CITIES)
except:
    for city in CITIES:
        if city.id.name not in DEFAULT_PRICE.index:
            print(f"城市 {city.id.name} 不在价格表中")
    raise ValueError("城市列表不匹配")

try:
    assert all((product.name in DEFAULT_PRICE.columns)
               for product in PRODUCTS)
except:
    for product in PRODUCTS:
        if product.name not in DEFAULT_PRICE.columns:
            print(f"商品 {product.name} 不在价格表中")
    raise ValueError("商品列表不匹配")

# Sort by city & product index

DEFAULT_PRICE = DEFAULT_PRICE.reindex(labels=map(
    lambda x: x.name, CITIES), columns=map(lambda x: x.name, PRODUCTS))

DEFAULT_PRICE_MATRIX = DEFAULT_PRICE.to_numpy()


@dataclass
class GameData():
    """游戏数据类
    """

    price: np.ndarray = DEFAULT_PRICE_MATRIX
