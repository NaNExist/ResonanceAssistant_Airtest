import json

import resource.function.city_guide as guide
import resource.function.trade_action as trade
import resource.function.game_action as game
import resource.function.battle_action as battle
import resource.function.travel_action as travel
import resource.function.base_action as base
import resource.function.count_price as count

from win10toast import ToastNotifier


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

    while setting["user_inf"]["fatigue_limit"] - setting["user_inf"]["fatigue"] > 300 or setting["user_inf"][
        "fatigue"] < 50:
        business_traffic(setting, times=1)
        setting = inf_update(setting=setting, type=2)
        print(setting["user_inf"]["fatigue"])

    dayly_work(loc_city=loc_city, parm=3)
    setting = inf_update()
    game.clean_trade_mission(base.city_name_transition(loc_city), setting["mission"]["human_transport"],
                             setting["mission"]["freight_transport"], setting["mission"]["purchase_transport"])


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
    with open("resource/setting/setting.json", "w", encoding="utf-8") as f:
        json.dump(setting, f, ensure_ascii=False)
    return setting


def dayly_work(loc_city=None, parm=None):
    if not loc_city:
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
            travel.citytravel(startcity=loc_city, endcity=end_city)
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

    game.clean_trade_mission(base.city_name_transition(loc_city), setting["mission"]["human_transport"],
                             setting["mission"]["freight_transport"], setting["mission"]["purchase_transport"])


def count_business_proposal():
    data = count.t1()  # t1 api获取数据
    inf = count.t2(data)  # t2 数据整理出表格
    result = count.t3(FATIGUE=inf[0][1:, 1:], PRODUCT_BUY_PRICES=inf[1][1:, 1:], PRODUCT_SELL_PRICES=inf[2][1:, 1:],
                      CITY_LIST=inf[3], GET_PRODUCT_LOTS=inf[4][1:, 1:],
                      PRODUCTS_IDX_TO_NAME=None)  # t3 计算方案，返回循环城市列表，总利润，总疲劳，单位利润
    city_list = [base.city_name_transition(i) for i in result[0]]
    product_list = []

    for i in range(len(city_list)):
        product_list.append(
            count.t4(start_city=city_list[i % len(city_list)], end_city=city_list[(i + 1) % len(city_list)]))
    print("!", result, "!")
    print("?", product_list, "?")
    return [result, product_list]


def business_traffic(setting, times=1, proposal=None):
    if not setting:
        setting = game.read_setting()
    loc_city = setting["user_inf"]["loc_city"]
    if not proposal:
        print("")

    while times != 0:
        data = count.t1()  # t1 api获取数据
        inf = count.t2(data)  # t2 数据整理出表格
        result = count.t3(FATIGUE=inf[0][1:, 1:], PRODUCT_BUY_PRICES=inf[1][1:, 1:], PRODUCT_SELL_PRICES=inf[2][1:, 1:],
                          CITY_LIST=inf[3], GET_PRODUCT_LOTS=inf[4][1:, 1:],
                          PRODUCTS_IDX_TO_NAME=None)  # t3 计算方案，返回循环城市列表，总利润，总疲劳，单位利润
        # t4 获取起点到终点城市可购买有收益商品的列表，收益降序排序，返回商品列表
        travel_list = [base.city_name_transition(name=i) for i in result[0]]
        # 找一个最近的城市开始循环
        if loc_city not in travel_list:
            aim_city = base.count_nearest_city(city=loc_city, citylist=travel_list)
            buy_list = count.t4(start_city=loc_city, end_city=aim_city)  # 计算购买商品
            print("购买途中商品")
            guide.enter_city()  # 开始购买商品
            guide.enter_exchange(cityname=loc_city)
            trade.test(buylist=[i[0] for i in buy_list], buybook=0)
            travel.citytravel(startcity=loc_city, endcity=aim_city)  # 导航到目标城市
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
            travel.citytravel(startcity=travel_list[(i + offset) % len(travel_list)],
                              endcity=travel_list[(i + 1 + offset) % len(travel_list)])
            loc_city = travel_list[(i + 1 + offset) % len(travel_list)]
        times -= 1


def autorun(citylist, productlist1, productlist2, city1book=0, city2book=0, times=-1):
    """

    :param citylist: 往返城市列表
    :param productlist1: 1号城市商品购买列表
    :param productlist2: 2号城市商品购买列表
    :param city1book: 购买1号城市商品用多少书
    :param city2book: 购买2号城市商品用多少书
    :param times:往返多少次
    :return:
    """
    # 预处理数据
    citydir = {"阿妮塔能源研究所": "anita_energy_research_institute", "7号自由港": "freeport", "七号自由港": "freeport",
               "澄明数据中心": "clarity_data_center_administration_bureau",
               "修格里城": "shoggolith_city", "铁盟哨站": "brcl_outpost",
               "荒原站": "wilderness_station", "曼德矿场": "mander_mine", "淘金乐园": "onederland"}
    toaster = ToastNotifier()

    # 先检查在哪个城市
    guide.enter_city()
    cityname = guide.searchcity()
    guide.backmain()

    # 不在1号城的前往1号城
    if cityname != citydir[citylist[0]]:
        toaster.show_toast("跑商通知", "目前在" + cityname + "准备前往" + citydir[citylist[0]], duration=1)
        travel.citytravel(startcity=cityname, endcity=citydir[citylist[0]])

    time = 0
    while time != times:
        # 这里在1号城
        cityname = citydir[citylist[0]]
        print(cityname)

        toaster.show_toast("跑商通知", "到达" + cityname, duration=1)

        guide.enter_city()
        guide.enter_exchange(cityname=cityname)
        trade.test(productlist2, productlist1, buybook=city1book)

        toaster.show_toast("跑商通知", "前往" + citydir[citylist[1]], duration=1)

        travel.citytravel(startcity=cityname, endcity=citydir[citylist[1]])

        # 这里在2号城
        cityname = citydir[citylist[1]]
        print(cityname)

        toaster.show_toast("跑商通知", "到达" + cityname, duration=1)

        guide.enter_city()
        guide.enter_exchange(cityname=cityname)
        trade.test(productlist1, productlist2, buybook=city2book)

        toaster.show_toast("跑商通知", "前往" + citydir[citylist[0]], duration=1)

        travel.citytravel(startcity=cityname, endcity=citydir[citylist[0]])

        time += 1

        # 显示通知

        toaster.show_toast("跑商通知", "现在已经跑了" + str(time) + "次" + citylist[0] + "-" + citylist[1] + "循环",
                           duration=1)
