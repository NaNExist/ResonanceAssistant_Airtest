from airtest.core.api import *
import resource.function.base_action as base
import resource.function.city_guide as guide
import resource.function.travel_action as travel
import resource.function.battle_action as battle
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


def eat_physical_medicine(small=0, medium=0, large=0, money=0):
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


def eat_fatigue_medicine(small=0, medium=0, large=0, money=0):
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
    small_san_medicine_loc = [65, 630, 30, 20]
    middle_san_medicine_loc = [365, 625, 30, 20]
    large_san_medicine_loc = [665, 630, 30, 20]
    fatigue_medicine_loc = [850, 235, 30, 18]

    loc_city = base.city_name_transition(base.recognition_text_ocr(rect=loc_city_loc))
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
    while True:
        result = base.recognition_textlist_ocr(
            [small_san_medicine_loc, middle_san_medicine_loc, large_san_medicine_loc])
        if len(result) == 3:
            break
        print("识别到仙人掌数量不对，重来")
    san_medicine = [int(result[0].replace("O", "0")), int(result[1].replace("O", "0")),
                    int(result[2].replace("O", "0"))]
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

    user_inf = {"lv": int(lv),
                "san": int(san),
                "san_limit": int(san_limit),
                "fatigue": int(fatigue),
                "fatigue_limit": int(fatigue_limit),
                "cargo": int(cargo),
                "cargo_limit": int(cargo_limit),
                "money": int(money),
                "fatigue_medicine": fatigue_medicine,
                "san_medicine": san_medicine,
                "loc_city": loc_city}
    data["user_inf"] = user_inf
    print(user_inf)

    with open("resource/setting/setting.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    return user_inf


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
                result.append(re.sub(r'[^\u4e00-\u9fa5^a-zA-Z^0-9]', '', mission_describe[2]))
                result.append(
                    re.findall(r'至(.*?)。', mission_describe[1])[0] if re.findall(r'至(.*?)。', mission_describe[1])[
                                                                           0] != "七号自由港" else "7号自由港")
                result.append(int(re.findall(r'\d+', mission_describe[1])[0]))

                if result[0] not in [temp[0] for temp in freight_transport]:
                    human_transport.append(result)
                    print("增加客运项目", result)
                    return True

                print("重复项目,不增加客运项目", result[0])
                return False
            case "货运":
                result.append(re.sub(r'[^\u4e00-\u9fa5^a-zA-Z0-9]', '', mission_describe[2]))
                result.append(re.findall(r'箱(.*?)至', mission_describe[1])[0])
                result.append(
                    re.findall(r'至(.*?)。', mission_describe[1])[0] if re.findall(r'至(.*?)。', mission_describe[1])[
                                                                           0] != "七号自由港" else "7号自由港")
                result.append(int(re.findall(r'\d+', mission_describe[1])[0]))
                if result[0] not in [temp[0] for temp in freight_transport]:
                    freight_transport.append(result)
                    print("增加货运项目", result)
                    return True
                print("重复项目,不增加货运项目", result[0])
                return False
            case "采购":
                result.append(re.sub(r'[^\u4e00-\u9fa5^a-zA-Z^0-9]', '', mission_describe[2]))
                result.append(re.findall(r'箱(.*?)至', mission_describe[1])[0])
                result.append(
                    re.findall(r'至(.*?)售', mission_describe[1])[0] if re.findall(r'至(.*?)。', mission_describe[1])[
                                                                            0] != "七号自由港" else "7号自由港")
                result.append(int(re.findall(r'\d+', mission_describe[1])[0]))

                if result[0] not in [temp[0] for temp in freight_transport]:
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

    for _ in range(5):

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

        if flag > 0:
            print("本次识别存在新项目，滑动")
            swipe((1000, 600), (1000, 400), duration=0.5)
        else:
            print("本次识别不存在新项目，完成")
            break

    # data["mission"]["human_transport"] = human_transport
    # data["mission"]["freight_transport"] = freight_transport
    # data["mission"]["purchase_transport"] = purchase_transport

    mission = {"human_transport": human_transport, "freight_transport": freight_transport,
               "purchase_transport": purchase_transport}
    print(mission)
    with open("resource/setting/setting.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    guide.backmain()

    return mission




def read_setting():
    with open("resource/setting/setting.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def drink_fatigue(loc_city=None):
    # todo 没写完的喝酒逻辑
    guide.enter_city()
    guide.enter_place(place_name="rest",cityname=loc_city,type = 0)
    guide.choose(1)
    touch((1200,35))
    sleep(5)
    guide.backmain()
    sleep(0.5)

def clean_trade_mission(loc_city, human_transport, freight_transport, purchase_transport):
    travel_map = []
    print("客运任务列表：", human_transport)
    print("货运任务列表：", freight_transport)

    for i in human_transport:
        temp = base.city_name_transition(i[1])
        if temp not in travel_map:
            travel_map.append(temp)

    for i in freight_transport:
        temp = base.city_name_transition(i[2])
        if temp not in travel_map:
            travel_map.append(temp)

    # 打印排序后的列表
    print("需要到达城市列表：", travel_map)

    cost, plan = base.route_planning(start_city = loc_city,city_list = travel_map)
    print("执行路径:", "->".join(plan),"消耗疲劳",cost)
    for i in plan[1:]:
        print("当前目标",i)
        travel.city_travel(startcity=loc_city, endcity=i)
        loc_city = i

    # while travel_map:
    #     travel_map = set(travel_map) - {loc_city}
    #     aim_city = base.count_nearest_city(city=loc_city, citylist=travel_map)
    #     print("当前目标", base.city_name_transition(loc_city), "->", base.city_name_transition(aim_city))
    #     travel.city_travel(startcity=loc_city, endcity=aim_city)
    #     loc_city = aim_city


def clean_battle_mission(city_name=None):
    print("开始清理悬赏")
    guide.enter_city()
    guide.enter_battle(cityname=city_name)
    sleep(2)
    guide.choose(1)
    sleep(1)
    print("悬赏作战开始")
    battle.reward_battle_loop()
    print("悬赏作战结束")
    guide.backmain()
    return True


def access_mission():
    guide.enter_city()
    guide.enter_place(place_name="commerce", cityname=None, type=0)
    sleep(1)
    for _ in range(10):
        loc = base.find_text_ocr(text="接取订单", rect=[1070, 100, 160, 600])
        if loc:
            touch(loc)
            sleep(0.5)
            result = base.recognition_text_ocr(rect=[810, 110, 290, 30]).split("·")[0]
            print(result)
            if "客运" in result or "货运" in result:
                touch((900, 590))
        else:
            swipe((1000, 500), (1000, 400))
            sleep(1.5)
    sleep(2)
    guide.backmain()
