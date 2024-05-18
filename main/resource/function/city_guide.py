from airtest.core.api import *
import resource.function.base_action as base


# 这里是从主界面进入城市界面
def enter_city():
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
def enter_exchange(cityname=None):
    """

    :param cityname: 进那个地方
    :return:
    """
    if not cityname:
        touch(base.get_city_inf(searchcity(), "exchange"))
    else:
        touch(base.get_city_inf(cityname, "exchange"))


def enter_battle(cityname=None):
    """

    :param cityname: 进那个地方
    :return:
    """
    if not cityname:
        touch(base.get_city_inf(searchcity(), "battle"))
    else:
        touch(base.get_city_inf(cityname, "battle"))







def enter_place(place_name=None,cityname=None,type = 0):
    if not cityname:
        touch(base.get_city_inf(searchcity(), place_name))
    else:
        touch(base.get_city_inf(cityname, place_name))
    sleep(3)
    choose(type)

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


# 这里是在城市界面中识别城市，返回值是识别到的城市名称(英文
def searchcity():
    """
    注意，只能在城市界面运行
    :return:
    """
    rect = [140, 545, 350, 40]
    while True:
        result = base.recognition_text_ocr(rect=rect)
        if base.city_name_transition(name=result):
            return base.city_name_transition(name=result)


def is_main():
    return True if exists(
        Template(filename="resource/template/guide/city_ui.png", resolution=(1280, 720), threshold=0.9)) else False


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
            sleep(3)


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
    enter_city()
    enter_exchange(test)
