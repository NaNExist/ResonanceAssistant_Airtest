import json

import resource.function.city_guide as guide
import resource.function.trade_action as trade
import resource.function.game_action as game
import resource.function.battle_action as battle
import resource.function.travel_action as travel
import resource.function.base_action as base

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

    game.update_user_inf()
    # game.update_goods_inf()
    game.update_mission_inf()

    setting = game.read_setting()
    # game.ui()

    loc_city = setting["user_inf"]["loc_city"]
    lv = setting["user_inf"]["lv"]
    san = setting["user_inf"]["san"]
    san_limit = setting["user_inf"]["san_limit"]
    fatigue = setting["user_inf"]["fatigue"]
    fatigue_limit = setting["user_inf"]["fatigue_limit"]
    cargo = setting["user_inf"]["cargo"]
    cargo_limit = setting["user_inf"]["cargo_limit"]
    money = setting["user_inf"]["money"]
    san_medicine = setting["user_inf"]["san_medicine"]
    fatigue_medicine = setting["user_inf"]["fatigue_medicine"]

    human_transport = setting["mission"]["human_transport"]
    freight_transport = setting["mission"]["freight_transport"]
    purchase_transport = setting["mission"]["purchase_transport"]

    print(loc_city, lv, san, san_limit, fatigue, fatigue_limit, cargo, cargo_limit, money, san_medicine,
          fatigue_medicine)

    while True:
        if setting["user_inf"]["san_limit"] - setting["user_inf"]["san"] < 10:
            print("发现澄明要满了,临时清理一下")
            if base.get_city_inf(city=base.city_name_transition(name=loc_city), information="is_main"):
                battle.test(times=1, enemy=1, difficult=1)
            else:
                aim_city = base.city_name_transition(base.count_nearest_city(base.city_name_transition(name=loc_city)))
                print(aim_city, loc_city)
                travel.citytravel(startcity=base.city_name_transition(name=loc_city),
                                  endcity=base.city_name_transition(aim_city))
                battle.test(times=1, enemy=1, difficult=1)
    #     # if setting["user_inf"]["fatigue"] < 20:
    #     #     print("发现疲劳要满了,临时清理一下")
    #
    #     #     todo 加一个清理跑商和送客任务的部分
    #     base.sleep(1)
    #
    #     print("!")


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
    guide.entercity()
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

        guide.entercity()
        guide.enterexchange(cityname=cityname)
        trade.test(productlist2, productlist1, buybook=city1book)

        toaster.show_toast("跑商通知", "前往" + citydir[citylist[1]], duration=1)

        travel.citytravel(startcity=cityname, endcity=citydir[citylist[1]])

        # 这里在2号城
        cityname = citydir[citylist[1]]
        print(cityname)

        toaster.show_toast("跑商通知", "到达" + cityname, duration=1)

        guide.entercity()
        guide.enterexchange(cityname=cityname)
        trade.test(productlist1, productlist2, buybook=city2book)

        toaster.show_toast("跑商通知", "前往" + citydir[citylist[0]], duration=1)

        travel.citytravel(startcity=cityname, endcity=citydir[citylist[0]])

        time += 1

        # 显示通知

        toaster.show_toast("跑商通知", "现在已经跑了" + str(time) + "次" + citylist[0] + "-" + citylist[1] + "循环",
                           duration=1)


def clean_mission(loc_city=None, human_transport=None, freight_transport=None, purchase_transport=None):
    if not loc_city:
        loc_city = guide.searchcity()
