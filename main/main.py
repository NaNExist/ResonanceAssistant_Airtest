# -*- encoding=utf8 -*-
from airtest.core.api import *
import dotenv

import resource.function.city_guide as guide
import resource.function.trade_action as trade
import resource.function.game_action as game
import resource.function.battle_action as battle
import resource.function.travel_action as travel
import resource.function.core as core

def usertest():
    dotenv.load_dotenv()
    device_url = os.getenv("DEVICE")
    device_url = None if device_url == None else [device_url]
    game.init(devices=device_url)
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

                citylist = ["修格里城", "阿妮塔能源研究站"]
                #此处为往返城市名称，行驶前建议留足够仓库空间，不在第一个城市的会先开到第一个城市再开始

                city1buylist = "红茶,弹丸加速装置"
                # 这里指在第一个城市购买的商品，会在第二个城市售卖，逗号分隔的字符串
                city2buylist = "阿妮塔小型桦树发电机,石墨烯电池,阿妮塔101民用无人机,家用太阳能电池组,锂电池,充电电池"
                # 这里指在第二个城市购买的商品，会在第一个城市售卖，逗号分隔的字符串

                city1book = 5
                # 买第一个城市商品用多少书
                city2book = 3
                # 买第2个城市商品用多少书

                city1list = list(city1buylist.split(","))
                city2list = list(city2buylist.split(","))
                #将商品处理成列表

                game.sleep(5)
                #图一乐的延迟
                core.autorun(citylist, city1list, city2list,city1book,city2book)



usertest()
