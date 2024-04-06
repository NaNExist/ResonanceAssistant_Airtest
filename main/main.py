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


# 实现一些基本操作，待拆分(X
# 这里是初始化，开游戏，关游戏的部分
game.init()
game.startupapp()
game.closeapp()

# 这是循环清理澄明度
# battle.battle_loop()

