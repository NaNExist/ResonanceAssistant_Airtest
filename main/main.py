# -*- encoding=utf8 -*-
import json

import resource.function.battle_action as battle
import resource.function.core as core
import resource.function.game_action as game
import resource.function.base_action as base
import resource.function.trade_action as trade
import resource.function.city_guide as guide
import resource.function.count_price as count

def usertest():
    game.init()



    while True:

        print("选择操作:")
        print("1：启动游戏")
        print("2：关闭游戏")
        print("3：城市间导航(暂时用不了)")
        print("4：清理澄明度")
        print("5：半自动跑商（要求车库里面留足够空间，最好是空的")
        print("6：测试部分")

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
                battle.test(times=-1, enemy=2, difficult=3)
            #   times是作战次数，enemy是选择敌人，difficult是难度选择 均从1开始
            case 5:
                pass
            case 6:
                core.program_plan()


                # game.update_user_inf()
                # game.update_mission_inf()
                # game.clean_battle_mission(city_name=None)
                # count.temp()
                # core.count_business_proposal()





usertest()

