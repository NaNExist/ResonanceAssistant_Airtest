# -*- encoding=utf8 -*-
#py库
import json
#airtest库
from airtest.core.api import *
#RAA库
import resource.function.city_guide as guide
import resource.function.trade_action as trade
import resource.function.game_action as game
import resource.function.battle_action as battle
import resource.function.travel_action as travel

#这个应该放在game_action里面
# 设置一些全局参数
ST.THRESHOLD = 0.9
ST.SAVE_IMAGE = False

# 搞了个临时ui
if __name__ == '__main__':

    choose = 0
    game.init()
    while True:

        print("选择操作:")
        print("1：启动游戏")
        print("2：关闭游戏")
        print("3：城市间导航")
        print("4：清理澄明度")
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


