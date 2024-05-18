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
        print("3：清理日常")
        print("4：循环作战")
        print("5：自动跑商（默认疲劳跑到500停，不会用书")
        print("6：计算当前跑商方案")
        print("7：监控方案")
        print("8：测试部分（不用")

        print("")
        choose = int(input())
        match choose:
            case 1:
                game.startupapp()
            case 2:
                game.closeapp()
            case 3:
                core.daily_work(parm=3)
            case 4:
                battle.expel_battle_loop()
            case 5:
                print("疲劳跑到多少,输入0就是默认到500")
                fatigue_limit = int(input())
                book = int(input("book_num="))
                core.business_traffic(book= book,fatigue_limit=fatigue_limit if fatigue_limit != 0 else 500)
            case 6:
                book = int(input("book_num="))
                core.monitor_data(book=book)
            case 7:
                # print("花几本书")
                # income_limit_set = int(input())
                # print("花几本书")
                # income_each_fatigue_set =  int(input())
                book = int(input("book_num="))
                core.monitor_data_notice(book=book, income_set=0, income_each_fatigue_set=1)

            case 8:
                # core.program_plan()
                # core.program_plan_test()
                book = int(input("book_num="))
                core.business_traffic(book= book)
                # base.count_nearest_city(city="anita_weapon_research_institute")
                # print(count.calculation_scheme(book=4))

                # battle.expel_battle_loop(times=-1)
                # game.update_user_inf()
                # game.update_mission_inf()
                # game.clean_battle_mission(city_name=None)
                # count.temp()
                # core.count_business_proposal()

if __name__ =="__main__":
    usertest()
