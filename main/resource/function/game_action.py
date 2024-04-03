from airtest.core.api import *



def startupapp(device="android://127.0.0.1:5037/127.0.0.1:7555",
               appname="com.hermes.goda/com.hermes.goda.MainActivity"):
    start_app("com.hermes.goda")
    # 循环检测启程图标，检测到就结束，没有就疯狂点击左下角（(*^_^*)
    flag = True
    while flag:
        try:
            if wait(Template(filename="resource/template/guide/main_ui.png", resolution=(1280, 720)), timeout=1):
                flag = False
                print("success startup")
        except TargetNotFoundError:
            touch(v=(20, 700))


def closeapp(device="android://127.0.0.1:5037/127.0.0.1:7555",
               appname="com.hermes.goda/com.hermes.goda.MainActivity"):
    stop_app("com.hermes.goda")
