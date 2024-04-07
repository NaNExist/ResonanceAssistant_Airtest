from airtest.core.api import *


def startupapp(appname="com.hermes.goda"):
    start_app(appname)
    # 循环检测启程图标，检测到就结束，没有就疯狂点击左下角（(*^_^*)
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/map_ui.png", resolution=(1280, 720)))
        if loc:
            return True
            print("success startup")
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
