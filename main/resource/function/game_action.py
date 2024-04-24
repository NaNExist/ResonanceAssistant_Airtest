from airtest.core.api import *
import resource.function.base_action as base
import resource.function.city_guide as guide
import logging
import json
from paddleocr import PaddleOCR
import re


def startupapp(appname="com.hermes.goda"):
    start_app(appname)
    # 循环检测启程图标，检测到就结束，没有就疯狂点击左下角（(*^_^*)
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/map_ui.png", resolution=(1280, 720)))
        if loc:
            print("success startup")
            return True
        loc = exists(Template(filename="resource/template/guide/confirm.png", resolution=(1280, 720)))
        if loc:
            touch(loc)
        touch(v=(20, 700))


def closeapp(appname="com.hermes.goda"):
    stop_app(appname)


def init(devices=None, logdir=True, project_root="log/log.txt", compress=90):
    loggera = logging.getLogger("airtest")
    loggera.setLevel(logging.CRITICAL)
    loggerb = logging.getLogger("ppocr")
    loggerb.setLevel(logging.CRITICAL)

    ST.THRESHOLD = 0.9
    ST.SAVE_IMAGE = False

    if devices is None:
        devices = ["android://127.0.0.1:5037/127.0.0.1:7555"]
    auto_setup(__file__, devices=devices, logdir=logdir, project_root=project_root, compress=compress)
    __author__ = "Airtest"

    ocr = PaddleOCR(use_angle_cls=True, lang="ch")


def eatphysicalmedicine(small=0, medium=0, large=0, money=0):
    eatdir = {"small": small, "medium": medium, "large": large}
    for i in eatdir:
        if eatdir[i] <= 0:
            continue
        while True:
            loc = exists(
                Template(filename="resource/template/guide/physical.png", resolution=(1280, 720), threshold=0.8))
            if loc:
                touch((loc[0] + 500, loc[1]))
                break
            touch((150, 666))
            sleep(1)
        sleep(1)
        loc = exists(Template(
            filename="resource/template/guide/" + i + "physical.png",
            resolution=(1280, 720), threshold=0.8))
        if loc:
            touch(loc)
        if eatdir[i] > 1:
            touch((830, 480), times=eatdir[i] - 1)
        loc = exists(Template(filename="resource/template/guide/confirm.png", resolution=(1280, 720)))
        if loc:
            touch(loc)
        eatdir[i] = 0
    touch((840, 360))


def eatfatiguemedicine(small=0, medium=0, large=0, money=0):
    # todo 吃药
    pass


def update_user_inf():
    with open("resource/setting/setting.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    loc_city_loc = [1127, 498, 110, 16]
    lv_loc = [250, 100, 40, 20]
    san_loc = [570, 260, 70, 20]
    fatigue_loc = [570, 305, 70, 20]
    cargo_loc = [580, 350, 90, 20]
    money_loc = [195, 200, 120, 25]
    small_san_medicine_loc = [65, 630, 30, 16]
    middle_san_medicine_loc = [365, 625, 30, 16]
    large_san_medicine_loc = [665, 630, 30, 16]
    fatigue_medicine_loc = [850, 235, 30, 18]

    loc_city = base.recognition_text_ocr(rect=loc_city_loc)

    touch((160, 660))
    sleep(2)

    result = base.recognition_textlist_ocr([lv_loc, san_loc, fatigue_loc, cargo_loc, money_loc])
    lv = result[0]
    san_relate = result[1].split("/")
    fatigue_relate = result[2].split("/")
    cargo_relate = result[3].split("/")
    money = result[4]

    san = san_relate[0]
    san_limit = san_relate[1]
    fatigue = fatigue_relate[0]
    fatigue_limit = fatigue_relate[1]
    cargo = cargo_relate[0]
    cargo_limit = cargo_relate[1]

    touch((650, 270))
    sleep(1)
    result = base.recognition_textlist_ocr([small_san_medicine_loc, middle_san_medicine_loc, large_san_medicine_loc])
    san_medicine = [int(result[0]), int(result[1]), int(result[2])]
    guide.back()

    sleep(1)

    result = []

    touch((650, 315))
    sleep(1)
    touch((665, 240))
    sleep(1)
    result.append(int(base.recognition_text_ocr(fatigue_medicine_loc)))
    touch((295, 585))

    touch((900, 240))
    sleep(1)
    result.append(int(base.recognition_text_ocr(fatigue_medicine_loc)))
    touch((295, 585))

    touch((660, 500))
    sleep(1)
    result.append(int(base.recognition_text_ocr(fatigue_medicine_loc)))
    touch((295, 585))

    fatigue_medicine = result

    guide.back()

    touch((840, 360))

    data["user_inf"]["loc_city"] = loc_city
    data["user_inf"]["lv"] = int(lv)
    data["user_inf"]["san"] = int(san)
    data["user_inf"]["san_limit"] = int(san_limit)
    data["user_inf"]["fatigue"] = int(fatigue)
    data["user_inf"]["fatigue_limit"] = int(fatigue_limit)
    data["user_inf"]["cargo"] = int(cargo)
    data["user_inf"]["cargo_limit"] = int(cargo_limit)
    data["user_inf"]["money"] = int(money)
    data["user_inf"]["san_medicine"] = san_medicine
    data["user_inf"]["fatigue_medicine"] = fatigue_medicine

    print(loc_city, lv, san, san_limit, san_medicine, fatigue, fatigue_limit, san_medicine, cargo, cargo_limit, money)

    with open("resource/setting/setting.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def update_goods_inf():
    # todo 写一个识别货舱有哪些货物的
    pass


def update_mission_inf():
    with open("resource/setting/setting.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    recognition = [[48, 105, 50, 32], [70, 170, 600, 30], [108, 105, 250, 30]]
    sleep(2)
    touch((1060, 160))
    sleep(1)
    while True:
        loc = base.find_text_ocr(text="商会任务")
        if loc:
            touch(loc)
            sleep(1)
            break

    human_transport = []
    freight_transport = []
    purchase_transport = []

    def match_mission(mission_describe):
        result = []
        match mission_describe[0]:
            case "客运":
                result.append(mission_describe[2])
                result.append(re.findall(r'至(.*?)。', mission_describe[1])[0])
                result.append(int(re.findall(r'\d+', mission_describe[1])[0]))

                if result[0] not in [temp[0] for temp in human_transport]:
                    human_transport.append(result)
                    print("增加客运项目", result)
                    return True
                print("重复项目,不增加客运项目", result[0])
                return False
            case "货运":
                result.append(mission_describe[2])
                result.append(re.findall(r'箱(.*?)至', mission_describe[1])[0])
                result.append(re.findall(r'至(.*?)。', mission_describe[1])[0])
                result.append(int(re.findall(r'\d+', mission_describe[1])[0]))

                if result[0] not in [temp[0] for temp in freight_transport]:
                    freight_transport.append(result)
                    print("增加货运项目", result)
                    return True
                print("重复项目,不增加货运项目", result[0])
                return False
            case "采购":
                result.append(mission_describe[2])
                result.append(re.findall(r'箱(.*?)至', mission_describe[1])[0])
                result.append(re.findall(r'至(.*?)售', mission_describe[1])[0])
                result.append(int(re.findall(r'\d+', mission_describe[1])[0]))

                if result[0] not in [temp[0] for temp in purchase_transport]:
                    purchase_transport.append(result)
                    print("增加采购项目", result)
                    return True
                print("重复项目,不增加采购项目", result[0])
                return False
            case _:
                print("识别到未知，失败处理")
                return False

    mission_describe = base.recognition_textlist_ocr(recognition)
    match_mission(mission_describe=mission_describe)

    while True:

        loc_list = find_all(
            Template(filename="resource/template/guide/mission.png", resolution=(1280, 720), threshold=0.8, rgb=False))
        if not loc_list:
            break

        flag = 0
        for i in loc_list:
            touch(i["result"])
            sleep(0.5)
            mission_describe = base.recognition_textlist_ocr(recognition)
            if match_mission(mission_describe=mission_describe):
                flag += 1

        if flag < 1:
            print("本次识别存在新项目，滑动")
            swipe((1000, 600), (1000, 360), duration=1)
        else:
            print("本次识别不存在新项目，完成")
            break

    data["mission"]["human_transport"] = human_transport
    data["mission"]["freight_transport"] = freight_transport
    data["mission"]["purchase_transport"] = purchase_transport

    with open("resource/setting/setting.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    guide.backmain()


def read_setting():
    with open("resource/setting/setting.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
