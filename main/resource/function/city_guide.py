from airtest.core.api import *
import json


def replacecity(element="", facility=""):
    with open("resource/argument/loaction.json") as f:
        data = json.load(f)
    return data["city"][element][facility]


def entercity():
    touch(Template(filename="resource/template/guide/city_ui.png", resolution=(1280, 720)))
    sleep(3)


def enterexchange(type="sell"):
    cityname = searchcity()

    touch(replacecity(cityname, facility="exchange"))

    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/exchange_" + type + ".png", resolution=(1280, 720)))
        if loc:
            flag = False
            touch(loc)
    print("end")


def searchcity():
    flag = True
    while flag:
        for i in os.listdir("C:\\Users\\356\Desktop\MRA\pythonProject\main\\resource\\template\\city\\"):
            print(i)
            if exists(Template(filename="resource/template/city/" + i, resolution=(1280, 720))):
                return i.rsplit('.', 1)[0]


def backmain():
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/home.png", resolution=(1280, 720), threshold=0.9))
        if loc:
            touch(loc)
            flag = False
