from airtest.core.api import *
import resource.function.city_guide as guide
import resource.function.base_action as base


def test(selllist, buylist, buybook):
    sellproduct(product=selllist)
    buyproduct(book=buybook, product=buylist)
    guide.backmain()
    return True


def buyproduct(talktimes=0, book=0, product=None):
    """
    初步购买逻辑，启动界面在交易所选择买还是卖的界面
    :param book: 吃多少书
    :param product: 列表，目前只支持中文商品列表，后期会改成商品代号
    :return: True表示正常完成
    """
    # 检查商品列表是否为空
    if product is None:
        print("空参数购买")
        return False
    print("购买列表：", product)

    sleep(1)
    print("进入买")
    guide.choose(0)
    sleep(1)

    # 这里负责吃书,book大于10的没写，应该没人这么无聊吧
    print("使用", book, "本书")
    eatbook(book)
    # 识别列表中所有商品，找到的点一下，
    times = 5
    while times > 0:
        loc = base.find_textlist_ocr(text=product, rect=[620, 130, 210, 520])
        print("识别到商品及坐标：", loc)
        if loc :
            for i in loc:
                touch(i[1])
                sleep(0.5)
            product = list(set(product) - set([name[0] for name in loc]))
            if not product:
                print("购买结束")
                break
            print("待购货物:", product)
        swipe((670, 450), (670, 200), duration=0.5)
        times -= 1
        # 旧逻辑
        # for i in product:
        #     loc = base.find_text_ocr(i,rect = [])
        #
        #     print(loc)
        #     # loc = exists(
        #     #     Template(filename="resource/template/product/" + i + ".png", resolution=(1280, 720)))
        #     print(loc)
        #     if loc:
        #         print("识别到商品：", i)
        #         # touch((loc[0] + 120, loc[1]))
        #         touch(loc)
        #         newproduct.remove(i)
        # product = newproduct.copy()
        # print("待购货物", product)
        # swipe((670, 450), (670, 200), duration=1)
        # times -= 1

    talk(talktimes)

    if not makedeal():
        guide.back()
        return False

    sleep(2)
    # 有时候会出问题，加个sleep看看


def sellproduct(talktimes=0, product=None):
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
        print("无可售商品,无需后续")
        guide.back()
        return False
    print("有待售商品")
    # 识别列表中所有商品，找到的点一下，
    newproduct = product.copy()
    times = 5
    print("重复尝试次数", times)
    while newproduct and times > 0:
        loc = base.find_textlist_ocr(text=product, rect=[620, 130, 210, 520])
        print("识别到商品及坐标：", loc)
        if loc :
            skew = 0
            for i in loc:
                touch((i[1][0],i[1][1]-skew))
                skew+=120
                sleep(0.5)

            product = list(set(product) - set([name[0] for name in loc]))
            if not product:
                print("售卖结束")
                break
            print("待卖货物:", product)
        swipe((670, 450), (670, 200), duration=0.5)
        times -= 1

        # for i in product:
        #     loc = exists(Template(filename="resource/template/product/" + i + ".png", resolution=(1280, 720)))
        #     if loc:
        #         print("识别到商品：", i)
        #         touch((loc[0] + 120, loc[1]))
        #         newproduct.remove(i)
        #         sleep(1)
        # product = newproduct.copy()
        # print("待卖货物列表：", product)
        # swipe((670, 650), (470, 200), duration=1)
        # times -= 1

    talk(talktimes)

    if not makedeal():
        guide.back()
        return False

    sleep(2)
    # 有时候会出问题，加个sleep看看


def sellall(talktimes=0):
    sleep(3)
    print("进入卖")
    guide.choose(0)
    sleep(2)

    if not iswarehouseempty():
        print("无可售商品,无需后续")
        guide.back()
        return False

    while True:
        loc = exists(Template(filename="resource/template/action/cancelall.png", resolution=(1280, 720)))
        if loc:
            break
        touch((1200, 100))

    talk(talktimes)

    if not makedeal():
        guide.back()
        return False


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
            print("交易完成")
            touch((20, 700))
            return True
        else:
            touch((1000, 650))
            flag -= 1
    return False


def eatbook(times):
    if times <= 0:
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
    # todo 判断是否砍满，满了就退出
    if times == 0:
        print("不计划砍价")
        return False
    print("计划砍价", times, "次")
    loc = exists(Template(filename="resource/template/action/discuss.png", resolution=(1280, 720)))
    if loc:
        for i in range(times):
            touch(loc)
            sleep(5)
    print("砍完了")
    return True


def iswarehouseempty():
    if exists(Template(filename="resource/template/guide/empty_warehouse.png", resolution=(1280, 720))):
        return False
    return True
