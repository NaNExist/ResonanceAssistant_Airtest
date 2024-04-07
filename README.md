# ResonanceAssistant_Airtest

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

### IDE 使用

如果要用 IDE, 把文件都放到仓库文件夹里, 这样会保存一个 `xxx.air` 文件夹（建议不用AIRTEST IDE，直接写py文件

## TODO

- [x] 城市间导航（要求有自动出击，后面糊一个输了继续跑的补丁
- [x] 自动清理澄明度（需要手动到关卡（还没写吃药的行为
- [x] 初版半自动买卖商品
- [ ] 加 CI 验证 conda 环境
- [ ] 封装airtest操作作为操作层（高
- [ ] 拆分现有行动到行为层（高
- [ ] 编写完整买卖商品的调度层（高
- [ ] 改为class类
- [ ] 增加全商品匹配模板（目前争取先把能买到的搞了（要是有大佬能搞ocr出来就可以摆了（先糊着
- [ ] 糊一个能用的ui先（命令行也不是不能用
- [ ] 增加本地数据库功能（还没思路
- [ ] 爬取商品数据，自动计算最优跑商方案（haha
- [ ] 增加客运功能（
- [ ] 提高鲁棒性
