from airtest.core.api import *
import json

def replaceproduct(facility=""):
    with open("resource/argument/loaction.json") as f:
        data = json.load(f)
    print(data["product"][facility])
    return data["product"][facility]


def buyproduct(product=None):
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
                newproduct.remove(i)
        product = newproduct
        print("待购货物", product)
        swipe((670, 650), (670, 200), duration=1)
    loc = exists(Template(filename="resource/template/action/buy_product.png", resolution=(1280, 720)))
    if loc:
        touch(loc)
    flag = True
    while flag:
        try:
            if wait(Template(filename="resource/template/guide/map_ui.png", resolution=(1280, 720)), timeout=1):
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
                print(i, loc)
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