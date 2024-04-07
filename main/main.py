# -*- encoding=utf8 -*-
from airtest.core.api import *

import resource.function.city_guide as guide
import resource.function.trade_action as trade
import resource.function.game_action as game
import resource.function.battle_action as battle
import resource.function.travel_action as travel





def usertest():
    game.init()
    while True:

        print("选择操作:")
        print("1：启动游戏")
        print("2：关闭游戏")
        print("3：城市间导航")
        print("4：清理澄明度")
        print("5：半自动跑商（要求车库里面留足够空间，最好是空的")
        print("")
        choose = int(input())
        match choose:
            case 1:
                game.startupapp()
            case 2:
                game.closeapp()
            case 3:
                print("去哪个城市")
                print("1：阿妮塔能源研究站")
                print("2：7号自由港")
                print("3：澄明数据中心")
                print("4：修格里城")
                print("5：铁盟哨站")
                print("6：荒原站")
                print("7：曼德矿场")
                print("8：淘金乐园")
                choose = int(input())
                match choose:
                    case 1:
                        travel.test("a")
                    case 2:
                        travel.test("7")
                    case 3:
                        travel.test("c")
                    case 4:
                        travel.test("x")
                    case 5:
                        travel.test("tie")
                    case 6:
                        travel.test("h")
                    case 7:
                        travel.test("m")
                    case 8:
                        travel.test("t")
            case 4:
                battle.battle_loop()
            case 5:
                # print("需要输入循环地点,中文输入,空格分开")
                # citylist = input("").split(" ")
                # print("输入"+citylist[0]+"城市购买商品,中文输入,空格分开")
                # city1buylist= input("").split(" ")
                # print("输入" + citylist[1] + "城市购买商品,中文输入,空格分开")
                # city2buylist = input("").split(" ")
                
                # 这里用预设列表了，输入太慢，

                citylist = ["修格里城", "淘金乐园"]
                city1buylist = ["发动机", "弹丸加速装置", "红茶", "沃德烤鸡", "高档餐具", "罐头", "沃德山泉"]
                city2buylist = ["沙金", "青金石", "漆黑矿渣","玛瑙","铁矿石", "石英砂"]

                autorun(citylist, city1buylist, city2buylist)






def autorun(citylist, productlist1, productlist2):
    #预处理数据
    citydir = {"阿妮塔能源研究站": "a", "7号自由港": "7", "澄明数据中心": "c", "修格里城": "x", "铁盟哨站": "tie",
               "荒原站": "h", "曼德矿场": "m", "淘金乐园": "t", "阿妮塔战备工厂": "an"}
    citydir2 = {"阿妮塔能源研究站": "anita_energy_research_institute", "7号自由港": "freeport",
                "澄明数据中心": "clarity_data_center_administration_bureau",
                "修格里城": "shoggolith_city", "铁盟哨站": "brcl_outpost",
                "荒原站": "wilderness_station", "曼德矿场": "mander_mine", "淘金乐园": "onederland"}

    # 先检查在哪个城市
    guide.entercity()
    cityname = guide.searchcity()
    guide.backmain()

    # 前往1号城
    if cityname != citydir2[citylist[0]]:
        travel.test(citydir[citylist[0]])

    guide.entercity()
    guide.enterexchange(0)
    trade.buyproduct(product=productlist1)

    travel.test(citydir[citylist[1]])

    while True:
        # 这里在2号城
        guide.entercity()
        guide.enterexchange(1)
        trade.sellproduct(product=productlist1)

        guide.entercity()
        guide.enterexchange(0)
        trade.buyproduct(product=productlist2)

        travel.test(citydir[citylist[0]])

        # 这里在1号城
        guide.entercity()
        guide.enterexchange(1)
        trade.sellproduct(product=productlist2)

        guide.entercity()
        guide.enterexchange(0)
        trade.buyproduct(product=productlist1)

        travel.test(citydir[citylist[1]])


usertest()
