# -*- encoding=utf8 -*-
from pathlib import Path
import re

from airtest.core.api import *
import json
import resource.function.city_guide as guide
import resource.function.trade_action as trade
import resource.function.game_action as game
import resource.function.battle_action as battle

import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

# 项目根目录
project_root = os.getenv("PROJECT_ROOT")
"""项目根目录"""
if project_root is None:
    project_root = Path(__file__).parent.resolve()

# 端口设置
dev_url = os.getenv("DEVICE")
"""设备地址"""
if dev_url is None:
    raise Exception("No devices found in .env file")

logdir = os.getenv("LOGDIR")
"""log保存位置"""
if logdir is not None:
    logdir = os.path.join(project_root, logdir)

# 图像压缩比[1-100]
compress = 90

# 初始化airtest设置
auto_setup(__file__, devices=[dev_url], logdir=logdir,
           project_root=project_root, compress=compress)

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
