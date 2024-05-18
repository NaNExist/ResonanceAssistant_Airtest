import json
import time

import resource.function.city_guide as guide
import resource.function.trade_action as trade
import resource.function.game_action as game
import resource.function.battle_action as battle
import resource.function.travel_action as travel
import resource.function.base_action as base
import resource.function.count_price as count

from win10toast import ToastNotifier

TN = ToastNotifier()


class temp_program_plan():
    def __init__(self):
        setting = game.read_setting()


def program_plan():
    # todo:    "先读设置" √
    #     "根据设置补充缺失部分"  "直接全部更新，不相信用户"
    #     "启动用户界面"
    #     "根据用户输入启动服务"
    #     "计算方案"
    #     "目前起码得有获取价格的工具，识别体力的部分，识别商品的部分，跑商启动条件 利润/疲劳大于 或者总利润大于某个数，或者疲劳要满了"
    #     "清理澄明度要不默认清理，要不就得到固定城市刷材料"
    #     "最好是先写一个识别仓库、等级、材料、资产然后根据这些算"
    #
    setting = inf_update()

    user_inf = setting["user_inf"]
    mission = setting["mission"]

    loc_city = setting["user_inf"]["loc_city"]
    #
    # while setting["user_inf"]["fatigue_limit"] - setting["user_inf"]["fatigue"] > 300 or setting["user_inf"][
    #     "fatigue"] < 50:
    #     business_traffic(setting, times=1)
    #     setting = inf_update(setting=setting, type=2)
    #     print(setting["user_inf"]["fatigue"])
    # while True:
    #     print("!")
    #     business_traffic(setting = setting, proposal=None)

    #
    daily_work(loc_city=loc_city, parm=3)
    setting = inf_update()
    game.clean_trade_mission(loc_city, setting["mission"]["human_transport"],
                             setting["mission"]["freight_transport"], setting["mission"]["purchase_transport"])


def program_plan_test():
    """
    作为一个长时间的挂机测试函数，要求功能，全自动吃药，满足条件的跑商，自动清理任务
    :return:
    """
    # 开始部分，初始化基本用户参数
    setting = game.read_setting()

    # 进行用户信息更新
    setting = inf_update()
    user_inf = setting["user_inf"]
    mission = setting["mission"]
    sign = setting["sign"]

    while True:

        # if sign["daily_work"] and user_inf["san"] > 240 and user_inf["fatigue"] > 150 and user_inf["fatigue_limit"] - \
        #         user_inf["fatigue"] < 100:
        print("A")
        daily_work(loc_city=user_inf["loc_city"], parm=3)
        setting = inf_update()
        game.clean_trade_mission(setting["user_inf"]["loc_city"], setting["mission"]["human_transport"],
                                 setting["mission"]["freight_transport"], setting["mission"]["purchase_transport"])
        setting = inf_update()

        if count.temp() > 2200 and user_inf["fatigue"] < 500:
            print("B")
            business_traffic(setting, proposal=None)
            setting = inf_update()

        if (not sign["daily_work"]) and user_inf["san_limit"] - user_inf["san"] < 20 and base.get_city_inf(
                city=setting["user_inf"]["loc_city"], information="is_main"):
            print("C")
            battle.test(times=1, enemy=2, difficult=3)

        # base.sleep(600)


def inf_update(setting=None, type=3):
    if not setting:
        setting = game.read_setting()
    if type == 3:
        setting["user_inf"] = game.update_user_inf()
        setting["mission"] = game.update_mission_inf()
    elif type == 2:
        setting["user_inf"] = game.update_user_inf()
    elif type == 1:
        setting["mission"] = game.update_mission_inf()

    setting["time"] = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

    with open("resource/setting/setting.json", "w", encoding="utf-8") as f:
        json.dump(setting, f, ensure_ascii=False)
    return setting


def daily_work(loc_city=None, parm=None):
    print("开始清理日常（铁悬赏and商会任务")
    if not loc_city:
        print("未知城市，识别一下")
        guide.enter_city()
        loc_city = guide.searchcity()
        guide.backmain()
    if not parm:
        print("无任务参数，不进行执行")
        return False
    dayly_mission_travel = ["freeport", "clarity_data_center_administration_bureau", "shoggolith_city", "mander_mine"]
    # 前往最近的有商会有悬赏任务的城市
    while dayly_mission_travel:
        if loc_city not in dayly_mission_travel:
            end_city = base.count_nearest_city(city=loc_city, citylist=dayly_mission_travel)

            print("去", end_city, "接取任务")
            travel.city_travel(startcity=loc_city, endcity=end_city)
            loc_city = end_city
        print("开始接取任务")
        if parm == 3:
            game.access_mission()
            game.clean_battle_mission(city_name=loc_city)
        elif parm == 2:
            game.access_mission()
        elif parm == 1:
            game.clean_battle_mission(city_name=loc_city)
        # game.drink_fatigue()
        dayly_mission_travel = set(dayly_mission_travel) - {loc_city}

    setting = inf_update()

    game.clean_trade_mission(loc_city, setting["mission"]["human_transport"],
                             setting["mission"]["freight_transport"], setting["mission"]["purchase_transport"])


def business_traffic_abandon(setting=None, fatigue_limit=500):
    if not setting:
        print("no setting")
        setting = inf_update()
    loc_city = setting["user_inf"]["loc_city"]

    while setting["user_inf"]["fatigue"] < fatigue_limit:

        print("开始计算新一轮跑商方案")
        data = count.t1()  # t1 api获取数据
        print("获取商品数据完成")
        inf = count.t2(data)  # t2 数据整理出表格
        print("数据表格整理完成")
        result = count.t3(FATIGUE=inf[0][1:, 1:], PRODUCT_BUY_PRICES=inf[1][1:, 1:], PRODUCT_SELL_PRICES=inf[2][1:, 1:],
                          CITY_LIST=inf[3], GET_PRODUCT_LOTS=inf[4][1:, 1:],
                          PRODUCTS_IDX_TO_NAME=None)  # t3 计算方案，返回循环城市列表，总利润，总疲劳，单位利润
        print("计算方案完成")
        # t4 获取起点到终点城市可购买有收益商品的列表，收益降序排序，返回商品列表
        travel_list = [base.city_name_transition(name=i) for i in result[0]]
        # 找一个最近的城市开始循环

        if loc_city not in travel_list:
            print("开始导航到起始城市")
            aim_city = base.count_nearest_city(city=loc_city, citylist=travel_list)
            buy_list = count.t4(start_city=loc_city, end_city=aim_city)  # 计算购买商品
            print("购买途中商品")
            guide.enter_city()  # 开始购买商品
            guide.enter_exchange(cityname=loc_city)
            trade.test(buylist=[i[0] for i in buy_list], buybook=0)
            travel.city_travel(startcity=loc_city, endcity=aim_city)  # 导航到目标城市
            loc_city = aim_city

        offset = travel_list.index(loc_city)  # 计算后续循环偏移量
        for i in range(len(travel_list)):
            buy_list = count.t4(start_city=travel_list[(i + offset) % len(travel_list)],
                                end_city=travel_list[(i + 1 + offset) % len(travel_list)])
            print("购买以下商品：", buy_list)
            guide.enter_city()  # 开始购买商品
            guide.enter_exchange(cityname=loc_city)
            trade.test(buylist=[i[0] for i in buy_list], buybook=0)
            print("前往后续城市：", travel_list[(i + 1 + offset) % len(travel_list)])
            travel.city_travel(startcity=travel_list[(i + offset) % len(travel_list)],
                               endcity=travel_list[(i + 1 + offset) % len(travel_list)])
            loc_city = travel_list[(i + 1 + offset) % len(travel_list)]
        setting = inf_update(type=2)
        loc_city = setting["user_inf"]["loc_city"]


def business_traffic(setting=None, book=0, fatigue_limit=500):
    if not setting:
        print("no setting")
        setting = inf_update()
    loc_city = setting["user_inf"]["loc_city"]

    while setting["user_inf"]["fatigue"] < fatigue_limit:
        print("开始计算新一轮跑商方案")
        # 创建对应参数表
        travel_list, scheme, income, fatigue, income_each_fatigue = count.calculation_scheme(book)
        print("计算方案完成")

        city_list = [i[0] for i in travel_list]
        city_list_CN = [base.city_name_transition(i) for i in city_list]
        book_list = [i[1] for i in travel_list]
        product_map = [i[1] for i in scheme]
        product_list = [[j[0] for j in i] for i in product_map]

        print("计划跑商方案城市为", "→".join(city_list_CN))
        print("利润：", income, "轮次疲劳消耗：", fatigue, "单位利润：", income_each_fatigue)
        print("具体购买商品↓")
        for i, j, k in zip(city_list, book_list, [[j[0] for j in i[1]] for i in scheme]):
            print("城市：", i, "使用", j, "本书；", "购买商品：", k)

        # 找一个最近的城市开始循环
        if loc_city not in city_list:
            print("开始导航到起始城市")
            aim_city = base.count_nearest_city(city=loc_city, citylist=city_list)
            buy_list = count.t4(start_city=loc_city, end_city=aim_city)  # 计算购买商品
            print("购买途中商品")
            guide.enter_city()  # 开始购买商品
            guide.enter_exchange(cityname=loc_city)
            trade.test(buylist=[i[0] for i in buy_list], buybook=0)
            travel.city_travel(startcity=loc_city, endcity=aim_city)  # 导航到目标城市
            loc_city = aim_city

        offset = city_list.index(loc_city)  # 计算后续循环偏移量
        for i in range(len(city_list)):
            print("购买以下商品：", product_list[i])
            guide.enter_city()  # 开始购买商品
            guide.enter_exchange(cityname=loc_city)

            trade.test(buylist=product_list[(i + offset) % len(city_list)],
                       buybook=book_list[(i + offset) % len(city_list)])

            print("前往后续城市：", city_list[(i + 1 + offset) % len(city_list)])

            travel.city_travel(startcity=city_list[(i + offset) % len(city_list)],
                               endcity=city_list[(i + 1 + offset) % len(city_list)])

            loc_city = city_list[(i + 1 + offset) % len(city_list)]
        setting = inf_update(type=2)
        loc_city = setting["user_inf"]["loc_city"]


def monitor_data_notice(book=0, income_set=0, income_each_fatigue_set=0):
    while True:
        print("开始计算跑商方案")
        # 创建对应参数表
        travel_list, scheme, income, fatigue, income_each_fatigue = count.calculation_scheme(book)
        print("计算方案完成")

        city_list = [i[0] for i in travel_list]
        city_list_CN = [base.city_name_transition(i) for i in city_list]

        notice = ""
        if income > income_set != 0:
            notice += "当前最高利润为:" + str(income) + "\n"
        if income_each_fatigue > income_each_fatigue_set != 0:
            notice += "当前最高单位利润为:" + str(income_each_fatigue) + "\n"
        if notice != "":
            notice = "检索到方案：" + "->".join(city_list_CN) + "\n" + str(notice)
            print("当前最高利润为:" + str(income) + "\n","当前最高单位利润为:" + str(income_each_fatigue) + "\n")
            TN.show_toast(title="跑商通知", msg=notice, icon_path="resource/template/action/favicon.ico", duration=10)
            break
        base.sleep(600)

def monitor_data(book=0):

    print("开始计算跑商方案")
    # 创建对应参数表
    travel_list, scheme, income, fatigue, income_each_fatigue = count.calculation_scheme(book)
    print("计算方案完成")

    city_list = [i[0] for i in travel_list]
    city_list_CN = [base.city_name_transition(i) for i in city_list]

    print("检索到方案：" + "->".join(city_list_CN) + "\n" ,"当前最高利润为:" + str(income) + "\n","当前最高单位利润为:" + str(income_each_fatigue) + "\n")

