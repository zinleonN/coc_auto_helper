import pyautogui as pa
import cv2
import numpy as np
import logging

from src.tools import sleep
from src.tools import image_path
from src.tools import fluctuate_number
from src.yolo.detect import calculate_avg_distance_to_line


screen_width, screen_height = pa.size()

def radio_to_actural(radio_x, radio_y):
    return int(radio_x * screen_width), int(radio_y * screen_height)

def moveToLeftUp():
    moveFromTo((1/4, 1/4), (3/4, 3/4))

def moveToLeftDown():
    moveFromTo((1/4, 3/4), (3/4, 1/4))

def moveToRightUp():
    moveFromTo((3/4, 1/4), (1/4, 3/4))

def moveToRightDown():
    moveFromTo((3/4, 3/4), (1/4, 1/4))


def locateImages(*image_names, confidence=0.8, color_sensitive=False, min_saturation=40):
    import cv2
    import numpy as np
    sleep(0.5)
    for name in image_names:
        path = image_path(name)
        try:
            if not path:
                continue
            if not color_sensitive:
                location = pa.locateOnScreen(path, confidence=confidence)
                if location:
                    return location
            else:
                # 彩色敏感（HSV）匹配
                screen = pa.screenshot()
                screen = np.array(screen)
                screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
                template = cv2.imread(path)
                if template is None:
                    continue
                # 转为HSV
                screen_hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
                template_hsv = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)
                res = cv2.matchTemplate(screen_hsv, template_hsv, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val >= confidence:
                    h, w = template.shape[:2]
                    left, top = max_loc
                    # 取出匹配区域，判断饱和度
                    matched = screen_hsv[top:top+h, left:left+w]
                    if matched.shape[:2] == (h, w):
                        mean_s = matched[...,1].mean()
                        if mean_s >= min_saturation:
                            return (left, top, w, h)
        except Exception as e:
            pass
    return None

def clickImage(*image_names, color_sensitive=False):
    # 限制输出图片名数量，避免日志过长
    max_names = 5
    names_display = image_names[:max_names]
    names_str = ', '.join(str(n) for n in names_display)
    if len(image_names) > max_names:
        names_str += ', ...'
    logging.info(f"Attempting to click on images: [{names_str}]")
    location = locateImages(*image_names, color_sensitive=color_sensitive)
    if location:
        pa.moveTo(location, duration=0.2)
        pa.click()
        return 0
    else:
        logging.warning(f"Failed to find images: [{names_str}]")
        return -1

def moveFromTo(start_point, end_point, duration=0.8, holding=0.01):
    d = fluctuate_number(duration)
    start_x, start_y = radio_to_actural(start_point[0], start_point[1])
    end_x, end_y = radio_to_actural(end_point[0], end_point[1])
    

    pa.moveTo(start_x, start_y, fluctuate_number(0.2))
    pa.mouseDown()
    sleep(holding)    

    pa.moveTo(end_x, end_y, d)
    pa.mouseUp()
    sleep(0.1)


import asyncio
import concurrent.futures
import logging
import pyautogui
from functools import partial

async def detect_best_direction():
    """检测最佳方向，返回最佳方向的移动函数及其对应的映射点坐标"""
    directions_config = [
        ("left_up", moveToLeftUp, (0.153, 0.575), -0.75),
        ("left_down", moveToLeftDown, (0.338, 0.65), 0.74),
        ("right_up", moveToRightUp, (0.657, 0.328), 0.74),
        ("right_down", moveToRightDown, (0.699, 0.509), -0.75)
    ]
    
    MAX_DISTANCE = screen_height * 0.265
    results = {}  # 存储结果: {方向名称: (距离, 映射点列表, 移动函数)}
    
    # 使用线程池执行CPU密集型任务
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        tasks = []
        
        for name, move_func, coords, slope in directions_config:
            await asyncio.sleep(0.5)  # 等待一小段时间
            
            # 1. 执行方向移动
            move_func()
            
            # 2. 截图
            screenshot = pyautogui.screenshot()
            
            # 3. 计算坐标
            x, y = radio_to_actural(*coords)
            
            # 4. 创建异步任务计算距离和映射点
            task = loop.run_in_executor(
                executor, 
                partial(calculate_avg_distance_to_line, slope, x, y, screenshot)
            )
            tasks.append((name, move_func, task))  # 同时存储名称和移动函数
        
        # 等待所有任务完成并收集结果
        for name, move_func, task in tasks:
            distance, projected_points = await task
            logging.info(f"{name.title().replace('_', ' ')}: {distance}")
            results[name] = (distance, projected_points, move_func)
    
    # 寻找最小距离方向
    if not results:
        logging.info("No valid results found")
        return None, []
    
    # 找出最佳方向和最小距离
    best_direction_name, (min_distance, min_projected_points, best_move_func) = min(
        results.items(), 
        key=lambda item: item[1][0]
    )
    
    if min_distance < MAX_DISTANCE:
        logging.info(f"Best direction: {best_direction_name} with distance {min_distance}")
        return best_move_func, min_projected_points  # 返回移动函数而不是名称
    else:
        logging.info(f"No valid direction (min distance {min_distance} >= {MAX_DISTANCE})")
        return None, []

def place_army(location, direction, need_locate):
    if not location:
        logging.error("No location provided for placing army.")
        return
    if direction == "left_up":
        if need_locate: moveToLeftUp()
        pa.click(location)
        moveFromTo((0.526,0.104), (0.151,0.584), duration=2, holding=1)
    elif direction == "left_down":
        if need_locate: moveToLeftDown()
        pa.click(location)
        moveFromTo((0.128,0.281), (0.453,0.759), duration=2, holding=1)
    elif direction == "right_up":
        if need_locate: moveToRightUp()
        pa.click(location)
        moveFromTo((0.475,0.082), (0.843,0.572), duration=2, holding=1)
    elif direction == "right_down":
        if need_locate: moveToRightDown()
        pa.click(location)
        moveFromTo((0.863,0.294), (0.509,0.797), duration=2, holding=1)
    else:
        logging.error(f"Unknown direction: {direction}. Cannot place army.")
        return
