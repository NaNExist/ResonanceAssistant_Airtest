# -*- encoding=utf8 -*-
import re

from airtest.core.api import *
import json
import resource.function.city_guide as guide
import resource.function.trade_action as trade
import resource.function.game_action as game
import resource.function.battle_action as battle

# 端口设置
devices = ["android://127.0.0.1:5037/127.0.0.1:7555"]
# 保存log
logdir = True
# log保存位置
project_root = "C:\\Users\\356\\Desktop\\logs"
# 图像压缩比[1-100]
compress = 90
# 初始化airtest设置
auto_setup(__file__, devices=devices, logdir=logdir, project_root=project_root, compress=compress)
# 设置一些全局参数
ST.THRESHOLD = 0.9
ST.SAVE_IMAGE = False

















# 实现一些基本操作，待拆分
game.startupapp()
# game.closeapp()
# guide.entercity()
# enterexchange()
# buyproduct(product=["placer_gold.png", "lasurite.png", "silica_sand.png"])
# sellproduct(product=["石墨烯电池"])
