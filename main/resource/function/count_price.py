import csv
import pandas as pd
import numpy as np
import re
import json
import requests

import resource.function.base_action as base

def t4(start_city, end_city):
    with open("resource/setting/city_buy_inf.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    buy_product = data[base.city_name_transition(start_city)]
    start_city = base.city_name_transition(start_city)
    end_city = base.city_name_transition(end_city)


    city_sell_map = np.array(pd.read_csv("resource/setting/商品售出价格表.csv", header=None).values.tolist())
    city_buy_map = np.array(pd.read_csv("resource/setting/商品收购价格表.csv", header=None).values.tolist())
    city_num_map = np.array(pd.read_csv("resource/setting/商品数量价格表.csv", header=None).values.tolist())

    product = city_sell_map[1:, 0].tolist()

    product_sell_map = city_sell_map[1:, 1:].astype(float).astype(int)
    product_buy_map = city_buy_map[1:, 1:].astype(float).astype(int)
    product_num_map = city_num_map[1:, 1:].astype(float).astype(int)

    usecity = ["修格里城", "淘金乐园", "铁盟哨站", "荒原站", "曼德矿场", '澄明数据中心', "7号自由港", "阿妮塔战备工厂",
               "阿妮塔能源研究所"]

    trade_list = []
    for i in buy_product:
        dis = product_buy_map[product.index(i)][usecity.index(end_city)] - product_sell_map[product.index(i)][
            usecity.index(start_city)]
        if dis > 0:
            trade_list.append([i, dis])

    trade_list = sorted(trade_list, reverse=True, key=lambda x: x[1])
    print(trade_list)
    return trade_list


def t3(FATIGUE, PRODUCT_BUY_PRICES, PRODUCT_SELL_PRICES, PRODUCTS_IDX_TO_NAME, CITY_LIST, GET_PRODUCT_LOTS):
    # 货车的容量
    CAPACITY = 600

    # 货车的最大行驶疲劳
    MAX_FATIGUE = 600

    BUY_LOT_MODIFIER = 2.5  # 买入时的数量调整系数（声望）
    GENERAL_TAX = 0.065  # 假设买卖时的税率一样

    # FATIGUE 无向图，城市之间的疲劳，对称矩阵
    FATIGUE = FATIGUE.astype(float).astype(int)
    CITIY_NUM = len(FATIGUE)  # 9

    # 可买入的产品数量，第一维是产品，第二维是城市
    PRODUCT_LOTS = GET_PRODUCT_LOTS.astype(float).astype(int)
    PRODUCT_NUM = len(PRODUCT_LOTS)  # 74

    # 产品的买入和卖出价格，第一维是产品，第二维是城市
    PRODUCT_BUY_PRICES = PRODUCT_BUY_PRICES.astype(float).astype(int)
    PRODUCT_SELL_PRICES = PRODUCT_SELL_PRICES.astype(float).astype(int)

    print(CITIY_NUM, PRODUCT_NUM, PRODUCT_SELL_PRICES[1, 2])

    # 问题描述：
    # 有 CITIY_NUM 个城市，一个含有 PRODUCT_NUM 件商品的列表，一个容量为 CAPACITY 的货车。
    # 任意两个城市之间均可达，并存在疲劳 FATIGUE[i][j]。
    # 商品列表列出了第i个商品在第j个城市的：可买入数量 PRODUCT_LOTS[i][j]、购入价 PRODUCT_BUY_PRICES[i][j]、卖出价 PRODUCT_SELL_PRICES[i][j]。
    # 找到这样的一个顶点和一条路径与买卖行动列表，使得移动总疲劳小于 MAX_FATIGUE 时，总利润 profit 最大，并且（总利润 profit /总疲劳 fatigue）最大。
    # 额外的约束条件：货车每次到站时，必须卖出所有商品并尽可能买入商品。

    # 预先计算每两个城市之间可以买卖的商品利润总额，PROFIT[i][j]表示从i城市买入到j城市卖出的总利润
    PROFIT = np.zeros((CITIY_NUM, CITIY_NUM), dtype=int)
    BUYS = []  # 从i城市买入到j城市卖出的商品列表和数量
    for i in range(CITIY_NUM):
        BUYS.append([])
        for j in range(CITIY_NUM):
            if i == j:
                BUYS[i].append([])
                continue
            profits = []
            for k in range(PRODUCT_NUM):
                if PRODUCT_LOTS[k][i] > 0:
                    s_profit = PRODUCT_SELL_PRICES[k][j] - PRODUCT_BUY_PRICES[k][i]
                    s_profit -= s_profit * GENERAL_TAX  # 卖出时的税
                    s_profit -= PRODUCT_BUY_PRICES[k][i] * GENERAL_TAX  # 买入时的花费
                    profits.append((k, s_profit))
            profits.sort(key=lambda x: x[1], reverse=True)
            profit = 0
            cap = CAPACITY
            for idx, p in profits:
                if p > 0:
                    buy = min(cap, int(PRODUCT_LOTS[idx][i] * BUY_LOT_MODIFIER))
                    profit += p * buy
                    cap -= buy
                    BUYS[i].append((idx, buy))
                    if cap == 0:
                        break
            PROFIT[i][j] = profit
    # print(PROFIT)

    # 计算每单位疲劳的利润
    PROFIT_PER_DISTANCE = np.zeros((CITIY_NUM, CITIY_NUM), dtype=float)
    for i in range(CITIY_NUM):
        for j in range(CITIY_NUM):
            if i == j:
                continue
            PROFIT_PER_DISTANCE[i][j] = PROFIT[i][j] / FATIGUE[i][j]

    # 找到最大单次利润，理论上界
    profit_upper_bound = np.max(PROFIT_PER_DISTANCE)
    profit_lower_bound = 0
    print(f"start with [{profit_lower_bound}, {profit_upper_bound}]")

    # 设定（总利润/总疲劳）最大的路径上的（总利润/总疲劳）为 r
    # 则有 r <= max_profit_per_fatigue
    # 由则问题转化为寻找一条路径 sum p / sum f >= r, 变形为 sum p - r * sum f >= 0
    # 设定新图的权重为 w = p - r * f,
    # 假设经过的城市数量 N > ||V||, 则问题转化为寻找权重最大环路

    def bellman_ford(W, r):
        fatigue = np.zeros(CITIY_NUM, dtype=float)
        predecessor = -1 * np.ones(CITIY_NUM, dtype=int)
        fatigue[0] = 0
        for i in range(1, CITIY_NUM - 1):
            fatigue[i] = np.inf
        # relax edges repeatedly
        for _ in range(CITIY_NUM - 1):
            for u in range(CITIY_NUM):
                for v in range(CITIY_NUM):
                    if fatigue[u] + W[u][v] < fatigue[v]:
                        fatigue[v] = fatigue[u] + W[u][v]
                        predecessor[v] = u
        # check for negative-weight cycles
        for u in range(CITIY_NUM):
            for v in range(CITIY_NUM):
                if u != v and fatigue[u] + W[u][v] < fatigue[v]:
                    cycle = []
                    # trace back the cycle
                    for _ in range(CITIY_NUM):
                        v = predecessor[v]
                    cycle_vertex = v
                    while True:
                        cycle.append(cycle_vertex)
                        cycle_vertex = predecessor[cycle_vertex]
                        if cycle_vertex == v or cycle_vertex == -1:
                            break
                    cycle.reverse()

                    # 计算环路的总利润
                    cycle_profit = 0
                    for i in range(len(cycle) - 1):
                        cycle_profit += PROFIT[cycle[i]][cycle[i + 1]]
                    cycle_profit += PROFIT[cycle[-1]][cycle[0]]

                    # 计算环路的总疲劳
                    cycle_fatigue = 0
                    for i in range(len(cycle) - 1):
                        cycle_fatigue += FATIGUE[cycle[i]][cycle[i + 1]]
                    cycle_fatigue += FATIGUE[cycle[-1]][cycle[0]]

                    # 计算环路的总利润/总疲劳
                    cycle_profit_per_fatigue = cycle_profit / cycle_fatigue

                    if cycle_profit_per_fatigue >= r:
                        return cycle, cycle_profit, cycle_fatigue, cycle_profit_per_fatigue
        return None

    # 二分查找最大利润 r
    EPS = 1
    cycle_result = None
    while profit_upper_bound - profit_lower_bound > EPS:
        r = (profit_upper_bound + profit_lower_bound) / 2

        # 构造新图
        # 新图的权重为 w = r * d - p
        # 问题转化为求负权环
        W = r * np.array(FATIGUE, dtype=float) - PROFIT

        # 快速检查是否不存在负权
        if not np.any(W < 0):
            profit_upper_bound = r
            continue

        # Bellman-Ford算法求解负权环
        result = bellman_ford(W, r)
        if result:
            cycle_result = result
            profit_lower_bound = r
        else:
            profit_upper_bound = r

    print('基于以下参数搜索：')
    print(f"容量: {CAPACITY}, 买入时数量调整系数: {BUY_LOT_MODIFIER}, 税率: {GENERAL_TAX}")
    print('最佳环路', '->'.join([CITY_LIST[i] for i in cycle_result[0]]))
    print(f"总利润: {cycle_result[1]}, 总疲劳: {cycle_result[2]}, 单位利润: {cycle_result[3]}")
    print([CITY_LIST[i] for i in cycle_result[0]])
    return [CITY_LIST[i] for i in cycle_result[0]], cycle_result[1], cycle_result[2], cycle_result[3]


def t2(data=None):
    product = []
    city = []
    if not data:
        with open("resource/setting/price_inf.json", "r", encoding="utf-8") as f:
            data = json.load(f)

    for i in data:
        if i["type"] == "sell":
            pass
        elif i["type"] == "buy":
            pass
        if i["name"] not in product:
            product.append(i["name"])
        if i["station"] not in city:
            city.append(i["station"])

    usecity = ["修格里城", "淘金乐园", "铁盟哨站", "荒原站", "曼德矿场", '澄明数据中心', "7号自由港", "阿妮塔战备工厂",
               "阿妮塔能源研究所"]

    product_sell_map = np.zeros((len(product) + 1, len(usecity) + 1)).astype(str)
    product_sell_map[0, 0] = "cat"
    product_sell_map[1:, 0] = product
    product_sell_map[0, 1:] = usecity

    product_buy_map = np.zeros((len(product) + 1, len(usecity) + 1)).astype(str)
    product_buy_map[0, 0] = "cat"
    product_buy_map[1:, 0] = product
    product_buy_map[0, 1:] = usecity

    product_num_map = np.zeros((len(product) + 1, len(usecity) + 1)).astype(str)
    product_num_map[0, 0] = "cat"
    product_num_map[1:, 0] = product
    product_num_map[0, 1:] = usecity

    city_buy_inf = {i: [] for i in usecity}

    for i in data:
        if i["station"] not in usecity:
            continue
        if i["type"] == "buy":
            product_sell_map[product.index(i["name"]) + 1][usecity.index(i["station"]) + 1] = i["price"]

        elif i["type"] == "sell":
            product_num_map[product.index(i["name"]) + 1][usecity.index(i["station"]) + 1] = i["stock"]
            product_buy_map[product.index(i["name"]) + 1][usecity.index(i["station"]) + 1] = i["price"]
            city_buy_inf[i["station"]].append(i["name"])

    pd.DataFrame(product_buy_map).to_csv(path_or_buf="resource/setting/商品售出价格表.csv", header=None, index=None)
    pd.DataFrame(product_sell_map).to_csv(path_or_buf="resource/setting/商品收购价格表.csv", header=None, index=None)
    pd.DataFrame(product_num_map).to_csv(path_or_buf="resource/setting/商品数量价格表.csv", header=None, index=None)

    with open("resource/setting/city_buy_inf.json", "w", encoding="utf-8") as f:
        json.dump(city_buy_inf, f, ensure_ascii=False)

    city_tired_map = np.array(pd.read_csv("resource/setting/城市路程疲劳表.csv", header=None).values.tolist())

    # t3(FATIGUE=city_tired_map[1:, 1:], PRODUCT_BUY_PRICES=product_buy_map[1:, 1:],
    #    PRODUCT_SELL_PRICES=product_sell_map[1:, 1:], CITY_LIST=usecity, GET_PRODUCT_LOTS=product_num_map[1:, 1:],
    #    PRODUCTS_IDX_TO_NAME=None)
    return [city_tired_map, product_buy_map, product_sell_map, usecity, product_num_map]


def t1():
    try:
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0'
        }
        # 注意请求不要太频繁
        data = requests.get(
            'https://reso-data.kmou424.moe/api/fetch/goods_info?uuid=5d9b7836-6474-4e44-881c-78ea9e116334',
            headers=HEADERS
        ).json()
        with open("resource/setting/price_inf.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except:
        print("获取更新失败，使用上次更新数据")
        with open("resource/setting/price_inf.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    return data


def temp():
    data = t1()
    inf = t2(data)
    result = t3(FATIGUE=inf[0][1:, 1:], PRODUCT_BUY_PRICES=inf[1][1:, 1:], PRODUCT_SELL_PRICES=inf[2][1:, 1:],
                CITY_LIST=inf[3], GET_PRODUCT_LOTS=inf[4][1:, 1:], PRODUCTS_IDX_TO_NAME=None)
    # t4("修格里城", "7号自由港")




