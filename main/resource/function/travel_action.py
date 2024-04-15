from airtest.core.api import *
import resource.function.city_guide as guide
import json


def entermap():
    for i in range(5):
        loc = exists(
            Template(filename="resource/template/guide/map_ui.png", resolution=(1280, 720)))
        if loc:
            touch(loc)
            return True
    return False


def searchcity(end_city_name=""):
    direction = 0
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/city/map/" + end_city_name + ".png", resolution=(1280, 720),
                              threshold=0.8))
        if loc:
            print("找到目标", end_city_name, "坐标", loc)
            touch(loc)
            return True
        match direction // 3:
            case 0:
                swipe((640, 140), (640, 620), duration=1)
                direction += 1
            case 1:
                swipe((1000, 360), (340, 360), duration=1)
                direction += 1
            case 2:
                swipe((640, 620), (640, 140), duration=1)
                direction += 1
            case 3:
                swipe((340, 360), (1000, 360), duration=1)
                direction += 1
        direction %= 12


def guidecity(start_city_name="", end_city_name=""):
    startcityloc = guide.get_city_inf(city=start_city_name, information="maploc")
    endcityloc = guide.get_city_inf(city=end_city_name, information="maploc")
    directionvector = [endcityloc[0] - startcityloc[0], endcityloc[1] - startcityloc[1]]
    k = 300 / max(directionvector, key=abs).__abs__()
    direction = (int(directionvector[0] * k), int(-directionvector[1] * k))
    print(direction)
    swipe((640 + direction[0] // 2, 360 - direction[1] // 2), (640 - direction[0] // 2, 360 + direction[1] // 2),
          duration=1)

    times = 8
    flag = True
    while flag and times > 0:
        loc = exists(Template(filename="resource/template/city/map/" + end_city_name + ".png", resolution=(1280, 720),
                              threshold=0.8))
        if loc:
            print("找到目标", end_city_name, "坐标", loc)
            touch(loc)
            return True
        swipe((640 + direction[0] // 2, 360 - direction[0] // 2), (640 - direction[0] // 2, 360 + direction[0] // 2),
              duration=1)
        times -= 1
    return False


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
def citytravel(startcity="", endcity=""):
    entermap()
    if startcity != "":
        if not guidecity(start_city_name=startcity, end_city_name=endcity):
            searchcity(end_city_name=endcity)
    else:
        searchcity(end_city_name=endcity)
    travel()
