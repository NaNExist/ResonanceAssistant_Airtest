from airtest.core.api import *
import json


# 这里是从json中读取city的数据，目前只有各个城市交易所的坐标，其他的待补充
def get_city_inf(city="", information=""):
    """

    :param city:城市名称
    :param information: 需要坐标的店面类型
    :return: 店面坐标
    """
    with open("resource/setting/location.json") as f:
        data = json.load(f)
    return data["city"][city][information]


# 这里是从主界面进入城市界面
def entercity():
    """
    从主界面到城市界面
    :return:
    """
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/city_ui.png", resolution=(1280, 720)))
        if loc:
            touch(loc)
            sleep(3)
            return True


# 进交易所
def enterexchange(cityname=""):
    """

    :param cityname: 进那个地方
    :return:
    """
    if not bool(cityname):
        touch(get_city_inf(searchcity(), "exchange"))
    else:
        touch(get_city_inf(cityname, "exchange"))


def enterbattle(cityname=""):
    """

    :param cityname: 进那个地方
    :return:
    """
    if not bool(cityname):
        touch(get_city_inf(searchcity(), "battle"))
    else:
        touch(get_city_inf(cityname, "battle"))


#  这里是用于铁安居，商会，交易所一类的进入不同的部分用的，无确认运行，目前最高5层
def choose(type=0):
    """

    :param type:用来点击 铁安居，商会，交易所进入后的分支，不进行确认运行
    :return:
    """
    match type:
        case 0:
            touch((940, 320))
        case 1:
            touch((940, 400))
        case 2:
            touch((940, 480))
        case 3:
            touch((940, 560))
        case 4:
            touch((940, 640))


# 进商会，目前没啥用
def entershop(type=0):
    """

    :param type:数字表示进第几个项目，0开始
    :return:
    """
    touch(get_city_inf(searchcity(), "commerce"))
    sleep(3)
    choose(type)


# 这里是在城市界面中识别城市，返回值是识别到的城市名称(英文
def searchcity():
    """
    注意，只能在城市界面运行
    :return:
    """
    flag = True
    while flag:
        for i in os.listdir("resource\\template\\city\\logo"):
            print(i)
            if exists(Template(filename="resource/template/city/logo/" + i, resolution=(1280, 720))):
                return i.rsplit('.', 1)[0]


# 用来回到主界面
def backmain():
    """
    回到主界面
    :return:
    """
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/home.png", resolution=(1280, 720), threshold=0.9))
        if loc:
            touch(loc)
            flag = False


def back():
    """
    回退
    :return:
    """
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/return.png", resolution=(1280, 720), threshold=0.9))
        if loc:
            touch(loc)
            flag = False
            sleep(1)
        sleep(1)


# 测试用函数
def test(test):
    entercity()
    enterexchange(test)
