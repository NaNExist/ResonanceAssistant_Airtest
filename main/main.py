# -*- encoding=utf8 -*-
import re

from airtest.core.api import *
import json




# 端口设置
devices = ["android://127.0.0.1:5037/127.0.0.1:7555"]
# 保存log
logdir = True
# log保存位置
project_root = "C:\\Users\\356\\Desktop\\logs"
# 图像压缩比[1-100]
compress = 90
# 初始化airtest设置
auto_setup(__file__, devices=devices, logdir=logdir, project_root=project_root, compress=compress)

ST.THRESHOLD = 0.9
ST.SAVE_IMAGE = False

def startupapp(device="android://127.0.0.1:5037/127.0.0.1:7555",
               appname="com.hermes.goda/com.hermes.goda.MainActivity"):
    dev = connect_device(device)
    dev.shell("am start " + appname)
    # 循环检测启程图标，检测到就结束，没有就疯狂点击左下角（(*^_^*)
    flag = True
    while flag:
        try:
            if wait(Template(filename="resource/template/guide/main_ui.png", resolution=(1280, 720)), timeout=1):
                flag = False
                print("success startup")
        except TargetNotFoundError:
            touch(v=(20, 700))

def replacecity(element="", facility=""):
    with open("resource/argument/loaction.json") as f:
        data = json.load(f)
    return data["city"][element][facility]


def replaceproduct(facility=""):
    with open("resource/argument/loaction.json") as f:
        data = json.load(f)
    print(data["product"][facility])
    return data["product"][facility]

def entercity():
    touch(Template(filename="resource/template/guide/city_ui.png", resolution=(1280, 720)))
    sleep(3)

def backmain():
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/home.png", resolution=(1280, 720),threshold=0.9))
        if loc:
            touch(loc)
            flag = False

def searchcity():
    flag = True
    while flag:
        for i in os.listdir("C:\\Users\\356\Desktop\MRA\pythonProject\main\\resource\\template\\city\\"):
            print(i)
            if exists(Template(filename="resource/template/city/" + i, resolution=(1280, 720))):
                return i.rsplit('.', 1)[0]



def enterexchange(type="sell"):
    cityname = searchcity()

    touch(replacecity(cityname, facility="exchange"))

    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/exchange_"+type+".png", resolution=(1280, 720)))
        if loc:
            flag = False
            touch(loc)
    print("end")


def buyproduct(product=None):
    print("?")
    if product is None:
        product = []
        print("空参数")
    newproduct = product.copy()
    while newproduct:
        for i in product:
            loc = exists(Template(filename="resource/template/product/" + replaceproduct(i) + ".png", resolution=(1280, 720)))
            if loc:
                print(loc)
                touch((loc[0] + 120, loc[1]))
                newproduct.remove(i)
                print(product)
        product = newproduct
        print("do")
        swipe((670, 650), (670, 200), duration=1)
    loc = exists(Template(filename="resource/template/action/buy_product.png", resolution=(1280, 720)))
    if loc:
        print(loc)
        touch(loc)
    flag = True
    while flag:
        try:
            if wait(Template(filename="resource/template/guide/main_ui.png", resolution=(1280, 720)), timeout=1):
                flag = False
        except TargetNotFoundError:
            touch(v=(20, 700))

def sellproduct(product=None):
    print("?")
    if product is None:
        product = []
        print("空参数")
    newproduct = product.copy()
    while newproduct:
        for i in product:
            loc = exists(
                Template(filename="resource/template/product/" + replaceproduct(i) + ".png", resolution=(1280, 720)))
            if loc:
                touch((loc[0] + 120, loc[1]))
                print(i,loc)
                newproduct.remove(i)
        product = newproduct
        print(product)
        swipe((670, 650), (670, 200), duration=1)
    loc = exists(Template(filename="resource/template/action/sell_product.png", resolution=(1280, 720)))
    if loc:
        touch(loc)


    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/home.png", resolution=(1280, 720)))
        if loc:
            touch(loc)
            flag = False
        else:
            touch((20, 700))
    print("end")



# 实现一些基本操作，待拆分
startupapp()
entercity()
enterexchange()
# buyproduct(product=["placer_gold.png", "lasurite.png", "silica_sand.png"])
# sellproduct(product=["石墨烯电池"])

