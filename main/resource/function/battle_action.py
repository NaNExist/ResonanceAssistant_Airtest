from airtest.core.api import *
import json








def start_battle():
    touch(Template(filename="resource/template/guide/battle_ready.png", resolution=(1280, 720)))

    loc = exists(Template(filename="resource/template/guide/cancel.png", resolution=(1280, 720)))
    if loc:
        touch(loc)
        return False
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/battle_check.png", resolution=(1280, 720)))
        if loc:
            touch((1200,380))
            flag = False
    return True

def end_battle():
    flag = True
    while flag:
        loc = exists(Template(filename="resource/template/guide/quit_battle.png", resolution=(1280, 720),threshold=0.8))
        if loc:
            touch(loc)
            flag = False
        sleep(10)

def battle_loop():
    while True:

        if start_battle():
            sleep(60)
            end_battle()
        else:
            return
