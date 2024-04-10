from airtest.core.api import *
import resource.function.city_guide as guide
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
            touch((1200, 380))
            flag = False
    return True


def end_battle():
    flag = True
    while flag:
        loc = exists(
            Template(filename="resource/template/guide/quit_battle.png", resolution=(1280, 720), threshold=0.8))
        if loc:
            sleep(5)
            touch(loc)
            flag = False
        sleep(10)


def battle_loop(times = -1):
    while True:
        if start_battle():
            sleep(60)
            end_battle()
        else:
            return False


def changedifficulty(type=0):
    loc = exists(
        Template(filename="resource/template/guide/difficulty.png", resolution=(1280, 720), threshold=0.8))
    if loc:
        touch(loc)

    matchlist = {1: [275, 400], 2: [420, 400], 3: [560, 400], 4: [705, 400], 5: [850, 400], 6: [995, 400]}
    touch(matchlist[type])

    loc = exists(
        Template(filename="resource/template/action/confirm.png", resolution=(1280, 720), threshold=0.8))
    if loc:
        touch(loc)


def chooseenemy(enemy=0):
    if enemy == 0:
        print("无参数运行")
        return False
    matchlist = {1: [620, 660], 2: [890, 660], 3: [1140, 660]}
    touch(matchlist[enemy])
    return True


def test(times=-1,enemy=0, difficult=0):
    guide.entercity()
    guide.enterbattle()
    sleep(2)
    while True:
        guide.choose(0)
        sleep(1)
        chooseenemy(enemy=enemy)
        if ispurple():
            break
        guide.back()
        sleep(0.5)
    sleep(1)
    changedifficulty(type=difficult)
    battle_loop(times=times)


def ispurple():
    print("这里开始匹配箱子")
    touch((920,460))
    loc = exists(Template(filename="resource/template/guide/purple_box.png", resolution=(1280, 720),threshold=0.9,record_pos=(555,220)))
    print(loc)
    if loc:
        touch((470,660))
        return True
    touch((470, 660))
    return False
