import airtest.core.api as air


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
        air.swipe(start, end, durations=duration, steps=steps)


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
    if template=="":
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


