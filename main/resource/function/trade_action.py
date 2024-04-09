from airtest.core.api import *
import resource.function.city_guide as guide


def test(selllist, buylist, buybook):
    sellproduct(product=selllist)
    buyproduct(book=buybook, product=buylist)
    guide.backmain()
    return True



def buyproduct(talk = 0,book=0, product=None):
    """
    初步购买逻辑，启动界面在交易所选择买还是卖的界面
    :param book: 吃多少书
    :param product: 列表，目前只支持中文商品列表，后期会改成商品代号
    :return: True表示正常完成
    """
    # 检查商品列表是否为空
    if product is None:
        product = []
        print("购买空参数")
        return False
    print("购买列表：", product)

    sleep(3)
    guide.choose(0)
    sleep(2)

    # 这里负责吃书,book大于10的没写，应该没人这么无聊吧
    eatbook(book)

    # 识别列表中所有商品，找到的点一下，
    newproduct = product.copy()
    times = 5
    while newproduct and times > 0:
        for i in product:
            loc = exists(
                Template(filename="resource/template/product/" + i + ".png", resolution=(1280, 720)))
            if loc:
                touch((loc[0] + 120, loc[1]))
                newproduct.remove(i)
        product = newproduct.copy()
        print("待购货物", product)
        swipe((670, 450), (670, 200), duration=1)
        times -= 1

    makedeal()

    sleep(2)
    # 有时候会出问题，加个sleep看看

    #     搜索回到主界面按键，没有说明报表还在，点击左下角，循环处理
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/home.png", resolution=(1280, 720)))
        if loc:
            flag = False
        else:
            touch((20, 700))
    return True


def sellproduct(talk = 0,product=None):
    """
    初步购买逻辑，启动界面在商品界面
    :param product: 列表，目前只支持中文商品列表，后期会改成商品代号
    :return: True表示正常完成
    """
    # 检查商品列表是否为空
    if product is None:
        product = []
        print("售出空参数")
        return False

    sleep(3)
    guide.choose(1)
    sleep(2)

    if not iswarehouseempty():
        return False

    # 识别列表中所有商品，找到的点一下，
    newproduct = product.copy()
    times = 5
    while newproduct and times > 0:
        for i in product:
            loc = exists(Template(filename="resource/template/product/" + i + ".png", resolution=(1280, 720)))
            if loc:
                touch((loc[0] + 120, loc[1]))
                newproduct.remove(i)
                sleep(1)
        product = newproduct.copy()
        print("待卖货物", product)
        swipe((670, 650), (470, 200), duration=1)
        times -= 1

    if not makedeal():
        guide.back()
        return False

    sleep(2)
    # 有时候会出问题，加个sleep看看

    #     搜索回到主界面按键，没有说明报表还在，点击左下角，循环处理
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/home.png", resolution=(1280, 720)))
        if loc:
            flag = False
        else:
            touch((20, 700))
    return True


def makedeal(type=0, pause=0):
    """
    该函数用于点击购买/售出按键，注意，不会做行为前检查
    :param type: 没想好
    :param pause: 为0识别到价格变更就会继续购买，为1就不会，（应该会退出购买逻辑，但是我没想好
    :return:
    """
    #  固定位置点击
    flag = 3
    while flag > 0:
        loc = exists(Template(filename="resource/template/guide/deal_about.png", resolution=(1280, 720)))
        if loc:
            touch((20, 700))
            return True
        else:
            touch((1000, 650))
            flag -= 1
    return False


def eatbook(times):
    if times<=0:
        return False
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
    return True


def talk(times):
    loc = exists(Template(filename="resource/template/action/discuss.png", resolution=(1280, 720)))
    if loc:
        for i in range(times):
            touch(loc)
            sleep(5)

def iswarehouseempty():
    if exists(Template(filename="resource/template/guide/empty_warehouse.png", resolution=(1280, 720))):
        return False
    return True

