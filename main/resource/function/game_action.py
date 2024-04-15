from airtest.core.api import *


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
    ST.THRESHOLD = 0.9
    ST.SAVE_IMAGE = False

    if devices is None:
        devices = ["android://127.0.0.1:5037/127.0.0.1:7555"]
    auto_setup(__file__, devices=devices, logdir=logdir, project_root=project_root, compress=compress)


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


def eatfatiguemedicine(small=0, medium=0, large=0, money=0):
    pass
