import resource.function.city_guide as guide
import resource.function.trade_action as trade
import resource.function.game_action as game
import resource.function.battle_action as battle
import resource.function.travel_action as travel

from win10toast import ToastNotifier


def program_plan():
    pass


# 占位使用

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
        toaster.show_toast("跑商通知", "目前在" + cityname+"准备前往"+citydir[citylist[0]], duration=1)
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
