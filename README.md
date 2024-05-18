# 雷索纳斯跑商脚本

## 项目介绍

雷索纳斯自动跑商脚本，为了解放ph罪恶大手下苦苦赚钱买UR的自己，决定出道解决跑商问题（bushi
现在糊的有点烂，但是能用（

## 使用注意

分辨率1280*720
需要自行输入模拟器adb端口，开发用的mumu，所以默认端口是mumu的，端口设置在game_action的init函数里
运行main.py文件就行

## 开发指南

### 部署环境

使用 [`conda`](https://www.anaconda.com/) 管理环境, 请确保已经安装

```shell
conda env create -f environment.yml --prefix ./.conda
```

根据你的情况使用 `conda activate RAA_env` 或者 `source activate RAA_env` 激活环境, VS Code 可以直接选择环境

### 更新环境

如果你更改了引用, 使用以下指令保存更新后的环境(记得检查是否使用相对路径)

```shell
pip freeze > requirements.txt
conda env export > environment.yml
```

加载更新后的环境

```shell
conda env update -f environment.yml
pip install -r requirements.txt
```

### 设置环境变量

在项目根目录下创建 `.env` 文件, 内容如下

```conf
DEVICE="android://127.0.0.1:5037/127.0.0.1:7555"
PROJECT_ROOT=".../ResonanceAssistant_Airtest"
LOGDIR="log"
```

### IDE 使用

直接写py文件就行

## DOWN

- [x] 开关游戏
- [x] 循环作战（在有开始作战的界面
- [x] 爬取商品数据，自动计算最优跑商方案（爬数据需要索斯学会权限，算法是科伦巴商会那copy的（算出来的东西好像有点不对，虽然路线和科伦巴一样，但是利润和疲劳比差的有点多，啥时候研究一下
- [x] 全自动跑商（会用书了，但是不会讲价（之后想想怎么糊
- [x] 清理日常（指铁案局悬赏和商会的送客送货任务，大概花240澄明度和200疲劳？打不过就会卡住，送客送货有可能空间不够卡住。遇到了再改（感觉得加个喝酒的逻辑

## TODO

- [ ] 加 CI 验证 conda 环境（不会这个，听说有用
- [ ] 修改一下日常的清理逻辑，顺路跑一下商
- [ ] 糊一个调度逻辑方便长时间挂机
- [ ] 增加客运功能（等客运有用了在搞，phnmsl（其实是还没玩明白
- [ ] 改写部分逻辑减少网络波动导致的问题
- [ ] 研究一下看看能不能自动砍树（可以识别到地图的紫树，但是没法从界面找到（还得想想
- [ ] 自动跑商里面加一个自动喝酒
- [ ] 黑月商店自动购买商品（先糊一个买每日桦石的
