from airtest.core.api import *
import json


def replacecity(element="", facility=""):
    with open("resource/setting/loaction.json") as f:
        data = json.load(f)
    return data["city"][element][facility]


def entercity():
    touch(Template(filename="resource/template/guide/city_ui.png", resolution=(1280, 720)))
    sleep(3)


def enterexchange(type="sell"):
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/exchange_" + type + ".png", resolution=(1280, 720)))
        if loc:
            flag = False
            touch(loc)
    print("end")

def entershop(cityname = "",shopname=""):
    touch(replacecity(element=cityname, facility=shopname))

def searchcity():
    flag = True
    while flag:
        for i in os.listdir("resource\\template\\city\\"):
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
