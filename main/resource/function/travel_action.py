from airtest.core.api import *
import json


def entermap():
    for i in range(3):
        loc = exists(
            Template(filename="resource/template/guide/map_ui.png", resolution=(1280, 720)))
        if loc:
            touch(loc)
            return True
    return False

def searchcity(city_name=""):
    direction = 0
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/" + city_name + ".png", resolution=(1280, 720),threshold=0.8))
        if loc:
            touch(loc)
            return True
        match direction // 3:
            case 0:
                swipe((1000, 360), (340, 360), duration=1)
                direction += 1
            case 1:
                swipe((640, 620), (640, 140), duration=1)
                direction += 1
            case 2:
                swipe((340, 360), (1000, 360), duration=1)
                direction += 1
            case 3:
                swipe((640, 140), (640, 620), duration=1)
                direction += 1
        direction %= 12

def travel():
    starttravel()
    endtravel()
def starttravel():
    touch(Template(filename="resource/template/guide/start_travel.png", resolution=(1280, 720)))


def endtravel():
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/end_travel.png", resolution=(1280, 720)))
        if loc:
            touch(loc)
            flag = False
        sleep(10)


# 这个是完整的测试逻辑
def test(temp):
    entermap()
    searchcity(temp)
    starttravel()
    endtravel()
