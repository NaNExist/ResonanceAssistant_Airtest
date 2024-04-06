from airtest.core.api import *
import json


def test(type,list):
    dealproduct(type, list)

#
def dealproduct(type=0, product=None):
    """

    :param type: 0是买 1是卖商品
    :param product: 列表，目前只支持中文商品列表，后期会改成商品代号
    :return: True表示正常完成
    """
    # 检查商品列表是否为空
    if product is None:
        product = []
        print("空参数")
        return False

    # 识别列表中所有商品，找到的点一下，
    newproduct = product.copy()
    while newproduct:
        for i in product:
            loc = exists(
                Template(filename="resource/template/product/" + i + ".png", resolution=(1280, 720)))
            if loc:
                touch((loc[0] + 120, loc[1]))
                newproduct.remove(i)
        product = newproduct
        print("待购货物", product)
        swipe((670, 650), (670, 200), duration=1)

    #     点击购买或售出按键
    loc = exists(Template(
        filename="resource/template/action/buy_product.png" if type == 0 else "resource/template/action/sell_product.png",
        resolution=(1280, 720)))
    if loc:
        touch(loc)

    sleep(2)
    # 有时候会出问题，加个sleep看看

    #     搜索回到主界面按键，没有说明报表还在，点击左下角，循环处理
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/home.png", resolution=(1280, 720)))
        if loc:
            touch(loc)
            flag = False
        else:
            touch((20, 700))
    return True
