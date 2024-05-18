import json
import math
import pandas as pd

import airtest.core.api as air
import numpy as np
from airtest.core.api import *
from paddleocr import PaddleOCR


def touch(loc, times=1):
    """
    这个函数会点击times次loc位置
    :param loc：这个参数要求传入点击坐标
    :param times:这个是滑动次数，默认为1次
    """
    air.touch(loc, times=times)


def swipe(start, end, times=1, duration=1, steps=1):
    """
    这个函数会从start滑动到end，滑动times次，滑动完成会返回True
    :param steps: 滑动几次完成，2就是分两段滑动
    :param duration: 滑动消耗时间
    :param start:这个参数要求传入滑动起点，列表元组都行
    :param end：这个参数要求传入滑动终点，列表元组都行
    :param times:这个是滑动次数，默认为1次
    """
    for i in range(times):
        air.swipe(start, end, duration=duration, steps=steps)


def exists(template="", threshold=air.ST.THRESHOLD):
    """
    :param template:模板路径
    :param threshold: 识别阈值
    :return: 识别到返回坐标，失败返回False
    """
    loc = air.exists(template, threshold=threshold)
    if loc:
        return loc
    return False


def wait(template="", timeout=air.ST.FIND_TIMEOUT, interval=1):
    """

    :param template: 要等待出现的目标Template实例
    :param timeout:等待匹配的最大超时时长，默认为None即默认取 ST.FIND_TIMEOUT 的值
    :param interval:尝试查找匹配项的时间间隔（以秒为单位）
    :return:成功返回匹配到的坐标，失败返回False
    """
    if template == "":
        print("无识别模板")
        return False

    try:
        return air.wait(template=template, timeout=timeout, interval=interval)
    except air.TargetNotFoundError:
        return False


def sleep(times=1):
    """
    :param times: sleep的时长
    :return:无返回
    """

    air.sleep(times)


def cyclic_search(template="", threshold=air.ST.THRESHOLD):
    """
    这个函数会死循环搜索template，搜索到会返回坐标
    :param template:这个参数要求传入文件路径，默认为空，保证报错
    :param threshold：这个参数为识别阈值，默认为0.8
    """
    while True:
        loc = air.exists(air.Template(template, resolution=(1280, 720), threshold=threshold))
        if loc:
            return loc


def cyclic_search_times(template="", times=10, threshold=air.ST.THRESHOLD):
    """
    这个函数会循环times次搜索template，搜索到会返回坐标,搜不到会返回False
    :param template:这个参数要求传入文件路径，默认为空，保证报错
    :param threshold：这个参数为识别阈值，默认为0.8
    :param times:这个是识别次数，默认为10
    """

    for i in range(times):
        loc = air.exists(air.Template(template, resolution=(1280, 720), threshold=threshold))
        if loc:
            return loc
    return False


def search_and_touch_cyclic(template="", threshold=air.ST.THRESHOLD, cyclic_times=1, times=1):
    """
    这个函数会循环cyclic_times次搜索并点击模板times次,成功返回True，失败返回False
    :param template:这个参数要求传入模板路径
    :param threshold:这个参数为匹配阈值
    :param cyclic_times:这个参数为识别循环次数
    :param times:这个是点击次数，默认为1次
    """

    loc = cyclic_search_times(template, cyclic_times, threshold)
    if loc:
        touch(loc, times)
        return True
    else:
        print("识别失败")
        return False


def search_and_swipe_cyclic(template="", threshold=air.ST.THRESHOLD, cyclic_times=1, times=1):
    """
    这个函数会循环cyclic_times次搜索并滑动times次,成功返回True，失败返回False
    :param template:这个参数要求传入模板路径
    :param threshold:这个参数为匹配阈值
    :param cyclic_times:这个参数为识别循环次数
    :param times:这个是点击次数，默认为1次
    """

    loc = cyclic_search_times(template, cyclic_times, threshold)
    if loc:
        swipe(loc, times)
        return True
    else:
        print("识别失败")
        return False


def find_text_ocr(text="", rect=None):
    screen = G.DEVICE.snapshot()
    if rect:
        screen = screen[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
    else:
        rect = [0, 0, 1280, 720]

    print("搜索文本：", text, "搜索范围", rect)

    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    result = ocr.ocr(screen, cls=True)
    if not result:
        return False
    for idx in range(len(result)):
        res = result[idx]
        print(res)
        if not res:
            continue
        if not result:
            return False
        for line in res:
            if line[1][0] == text:
                loc = [(line[0][0][0] + line[0][1][0]) // 2, (line[0][1][1] + line[0][2][1]) // 2]
                return [loc[0] + rect[0], loc[1] + rect[1]]
    return False


def find_text_include_ocr(text="", rect=None):
    screen = G.DEVICE.snapshot()
    if rect:
        screen = screen[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
    else:
        rect = [0, 0, 1280, 720]

    print("搜索文本：", text, "搜索范围", rect)

    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    result = ocr.ocr(screen, cls=True)
    if not result:
        return False
    for idx in range(len(result)):
        res = result[idx]
        print(res)
        if not res:
            continue
        if not result:
            return False
        for line in res:
            if text in line[1][0]:
                loc = [(line[0][0][0] + line[0][1][0]) // 2, (line[0][1][1] + line[0][2][1]) // 2]
                return [loc[0] + rect[0], loc[1] + rect[1]]
    return False


def find_textlist_ocr(text=None, rect=None):
    if not text:
        print("空参数")
        return False
    print("搜索文本")
    screen = G.DEVICE.snapshot()
    if rect:
        screen = screen[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
    else:
        rect = [0, 0, 1280, 720]

    print("搜索文本列表：", text, "搜索范围", rect)

    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    result = ocr.ocr(screen, cls=True)
    resultloc = []
    for idx in range(len(result)):
        res = result[idx]
        if not rect:
            continue
        for line in res:
            if line[1][0] in text:
                loc = [(line[0][0][0] + line[0][1][0]) // 2, (line[0][1][1] + line[0][2][1]) // 2]
                resultloc.append([line[1][0], [loc[0] + rect[0], loc[1] + rect[1]]])
    return resultloc if resultloc != [] else False


def city_name_transition(name=""):
    if name == "":
        print("空参数")
        return False

    print("转换名称：", name)

    citylist = [["阿妮塔能源研究所", "anita_energy_research_institute"],
                ["7号自由港", "freeport"],
                ["七号自由港", "freeport"],
                ["澄明数据中心", "clarity_data_center_administration_bureau"],
                ["修格里城", "shoggolith_city"], ["铁盟哨站", "brcl_outpost"],
                ["荒原站", "wilderness_station"], ["曼德矿场", "mander_mine"],
                ["淘金乐园", "onederland"], ["阿妮塔战备工厂", "anita_weapon_research_institute"],
                ["阿妮塔发射中心", "anita_rocket_base"]]
    for i in citylist:
        if name == i[0]:
            return i[1]
        if name == i[1]:
            return i[0]
    print("错误输入")
    return False


def recognition_text_ocr(rect=None):
    if rect is None:
        rect = [0, 0, 1280, 720]
    screen = G.DEVICE.snapshot()
    newscreen = screen[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]

    print("识别文本范围", rect)

    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    resultlist = ocr.ocr(newscreen, cls=True, det=False)
    max = 0
    result = ""
    for idx in resultlist:
        for i in idx:
            if i[1] > max:
                max = i[1]
                result = i[0]
    return result


def recognition_textlist_ocr(rect=None):
    if rect is None:
        print("空参数运行")
        return False
    screen = G.DEVICE.snapshot()
    result = []
    print("识别文本范围列表", rect)
    for i in range(len(rect)):
        newscreen = screen[rect[i][1]:rect[i][1] + rect[i][3], rect[i][0]:rect[i][0] + rect[i][2]]
        # pil_img = cv2_2_pil(newscreen)
        # pil_img.show()

        ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        resultlist = ocr.ocr(newscreen, cls=True, det=False)
        max = 0
        for idx in resultlist:
            for j in idx:
                if j[1] > max:
                    max = j[1]
                    result.append(j[0])
    print("识别到：", result)
    return result


def count_nearest_city(city="", citylist=None):
    if city == "":
        print("空参数")
        return False
    all_city_list = [
        "shoggolith_city", "onederland", "brcl_outpost", "wilderness_station", "mander_mine",
        "clarity_data_center_administration_bureau", "freeport",
        "anita_weapon_research_institute", "anita_energy_research_institute", "anita_rocket_base"
    ]
    if not citylist:
        citylist = all_city_list

    temp = np.array(pd.read_csv("resource/setting/城市路程疲劳表.csv", header=None).values.tolist())[1:, 1:]
    print(temp)
    # todo 读疲劳表找最短城市
    print("正在寻找:", "`".join([city_name_transition(i) for i in citylist]), "中距", city_name_transition(city),
          "最近的城市")
    # print(np.array_equal(temp,temp.T)) 这里是检查疲劳矩阵是不是对称的
    distance = 114514
    aim = ""
    for i in citylist:
        if i == city:
            continue
        print(i, int(temp[all_city_list.index(city)][all_city_list.index(i)]), aim)
        dis = int(temp[all_city_list.index(city)][all_city_list.index(i)])
        if dis < distance:
            distance = dis
            aim = i

    if aim != "":
        print("目标为", aim)
        return aim
    else:
        print("未知错误")
        return False


# todo 这里需要一个计算最佳路径的算法，用于得到商会任务的最短路径，目前暂时留存gpt版本
def tsp_dp(cost_matrix, start_city):
    num_cities = len(cost_matrix)
    all_sets = 2 ** num_cities
    dp = [[float('inf')] * num_cities for _ in range(all_sets)]
    dp[1][start_city] = 0

    for mask in range(1, all_sets):
        for current_city in range(num_cities):
            if mask & (1 << current_city) == 0:
                continue
            for next_city in range(num_cities):
                if mask & (1 << next_city) != 0:
                    continue
                new_mask = mask | (1 << next_city)
                dp[new_mask][next_city] = min(dp[new_mask][next_city],
                                              dp[mask][current_city] + cost_matrix[current_city][next_city])

    # Find the minimum cost path
    min_cost = float('inf')
    final_city = -1
    for city in range(num_cities):
        if city != start_city:
            min_cost = min(min_cost, dp[all_sets - 1][city] + cost_matrix[city][start_city])
            if min_cost == dp[all_sets - 1][city] + cost_matrix[city][start_city]:
                final_city = city

    # Backtrack to find the path
    path = [final_city]
    mask = all_sets - 1
    while mask > 1:
        for prev_city in range(num_cities):
            if mask & (1 << prev_city) != 0 and dp[mask][final_city] == dp[mask ^ (1 << final_city)][prev_city] + \
                    cost_matrix[prev_city][final_city]:
                path.append(prev_city)
                mask ^= (1 << final_city)
                final_city = prev_city
                break

    path.reverse()
    return path, min_cost


def route_planning(start_city = None, city_list: list = None):
    if not start_city:
        print("无起始城市")
        return False
    city_tired_map = np.array(pd.read_csv("resource/setting/城市路程疲劳表.csv", header=None).values.tolist())
    city_tired_list = city_tired_map[1:, 1:].astype(float).astype(int)
    all_city_list = [city_name_transition(i) for i in city_tired_map[1:, 0]]
    if not city_list:
        city_list = all_city_list
    if start_city not in city_list:
        city_list.insert(0, start_city)
    else:
        city_list.remove(start_city)
        city_list.insert(0, start_city)
    cost_matrix = np.zeros((len(city_list), len(city_list)), int)
    for i in range(len(city_list)):
        for j in range(len(city_list)):
            cost_matrix[i][j] = city_tired_list[all_city_list.index(city_list[i]), all_city_list.index(city_list[j])]
    start_city = 0
    shortest_path, total_cost = tsp_dp(cost_matrix, start_city)
    # print("Shortest path:", [city_list[i] for i in shortest_path])
    # print("Total cost:", total_cost)
    return total_cost,[city_list[i] for i in shortest_path]




# [["阿妮塔能源研究所", "anita_energy_research_institute"],
#                 ["7号自由港", "freeport"],
#                 ["七号自由港", "freeport"],
#                 ["澄明数据中心", "clarity_data_center_administration_bureau"],
#                 ["修格里城", "shoggolith_city"], ["铁盟哨站", "brcl_outpost"],
#                 ["荒原站", "wilderness_station"], ["曼德矿场", "mander_mine"],
#                 ["淘金乐园", "onederland"], ["阿妮塔战备工厂", "anita_weapon_research_institute"],
#                 ["阿妮塔发射中心", "anita_rocket_base"]]

def get_city_inf(city="", information=""):
    """

    :param city:城市名称
    :param information: 需要坐标的店面类型
    :return: 店面坐标
    """
    print("搜索城市：", city, "信息为：", information)
    with open("resource/setting/location.json") as f:
        data = json.load(f)
    return data["city"][city][information]
