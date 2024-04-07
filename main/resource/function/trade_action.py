from airtest.core.api import *
import json


def test(type, list):
    buyproduct(type, list)


#
def buyproduct(book=0, product=None):
    """
    初步购买逻辑，启动界面在商品界面
    :param book: 吃多少书
    :param product: 列表，目前只支持中文商品列表，后期会改成商品代号
    :return: True表示正常完成
    """
    # 检查商品列表是否为空
    if product is None:
        product = []
        print("空参数")
        return False

    #这里负责吃书
    if book > 0:
        eatbook(book)

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

    makedeal()

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

def sellproduct(type=0, product=None):
    """
    初步购买逻辑，启动界面在商品界面
    :param type: 行动类别 0是买 1是卖
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
        print("待卖货物", product)
        swipe((670, 650), (670, 200), duration=1)

    makedeal()

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

def dealdealproduct_all(type=0, local=False):
    """

    :param type:
    :param local: 是否买卖本地商品 False为否，True为真
    :return:完成返回True
    """
    pass


def makedeal(type=0, pause=0):
    """
    该函数用于点击购买/售出按键，注意，不会做行为前检查
    :param type: 没想好
    :param pause: 为0识别到价格变更就会继续购买，为1就不会，（应该会退出购买逻辑，但是我没想好
    :return:
    """
    #  固定位置点击
    while True:
        loc = exists(Template(filename="resource/template/guide/deal_about.png", resolution=(1280, 720)))
        if loc:
            touch((20, 700))
            return True
        else:
            touch((1000, 650))

def eatbook(times):
    loc = exists(Template(filename="resource/template/guide/use_porp.png", resolution=(1280, 720)))
    if loc:
        touch(loc)
    loc = exists(Template(filename="resource/template/guide/buy_book.png", resolution=(1280, 720)))
    if loc:
        touch((loc[0] + 280, loc[1]))
    sleep(1)
    touch((830, 390), times=times - 1)
    loc = exists(Template(filename="resource/template/guide/confirm.png", resolution=(1280, 720)))
    if loc:
        touch(loc)
