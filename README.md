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

### 设置环境变量

在项目根目录下创建 `.env` 文件, 内容如下

```conf
DEVICE="android://127.0.0.1:5037/127.0.0.1:7555"
PROJECT_ROOT=".../ResonanceAssistant_Airtest"
LOGDIR="log"
```

### IDE 使用

如果要用 IDE, 把文件都放到仓库文件夹里, 这样会保存一个 `xxx.air` 文件夹

## TODO

- [ ] 加 CI 验证 conda 环境
