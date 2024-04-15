# -*- encoding=utf8 -*-


import resource.function.city_guide as guide
import resource.function.trade_action as trade
import resource.function.game_action as game
import resource.function.battle_action as battle
import resource.function.travel_action as travel
import resource.function.core as core
from win10toast import ToastNotifier



def usertest():
    game.init()


    # 可以塞测试函数
    # # price.get_price_table()
    # a = test.TestPriceDatabase()
    # a.test_calc_profit_to_and_fro()
    #



    while True:

        print("选择操作:")
        print("1：启动游戏")
        print("2：关闭游戏")
        print("3：城市间导航(暂时用不了)")
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
            case 4:
                # print("输入作战次数（数字1-inf（只会打到没澄明或者到次数，第几类敌人（数字1-3，什么难度（数字1-6（默认打紫箱子的。空格间隔输入")
                # inputlist = list(map(int,input().split(" ")))
                # times =  inputlist[0]
                # enemy = inputlist[1]
                # difficult = inputlist[2]
                battle.test(times=2,enemy=2,difficult=4)
            #   times是作战次数，enemy是选择敌人，difficult是难度选择 均从1开始
            case 5:
                # print("需要输入循环地点,中文输入,空格分开,默认跑3次")
                # citylist = input("").split(" ")
                # print("输入"+citylist[0]+"城市购买商品,中文输入,空格分开")
                # city1buylist= input("").split(" ")
                # print("输入" + citylist[1] + "城市购买商品,中文输入,空格分开")
                # city2buylist = input("").split(" ")

                # 这里用预设列表了，输入太慢，

                citylist = ["曼德矿场", "阿妮塔能源研究所"]
                #此处为往返城市名称，行驶前建议留足够仓库空间，不在第一个城市的会先开到第一个城市再开始

                city1buylist = "图形加速卡, 钛矿石, 曼德工具箱, 铁轨用特种钢材, 钢筋混凝土轨枕"
                # 这里指在第一个城市购买的商品，会在第二个城市售卖，逗号分隔的字符串
                city2buylist = "阿妮塔101民用无人机, 家用太阳能电池组, 充电电池, 锂电池"
                # 这里指在第二个城市购买的商品，会在第一个城市售卖，逗号分隔的字符串

                city1book = 2
                # 买第一个城市商品用多少书
                city2book = 0
                # 买第2个城市商品用多少书

                city1list = list(city1buylist.split(", "))
                city2list = list(city2buylist.split(", "))
                # 将商品处理成列表
                print(city1list,city2list)
                game.sleep(5)
                #图一乐的延迟
                core.autorun(citylist, productlist1=city1list, productlist2=city2list,city1book=city1book,city2book=city2book)


usertest()
