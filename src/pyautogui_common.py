import pyautogui as pa
import cv2
import numpy as np

from src.tools import sleep
from src.tools import image_path
from src.tools import fluctuate_number

scrren_width, screen_height = pa.size()


def moveToLeftUp():
    sleep(2)
    moveFromTo((1/4, 1/4), (3/4, 3/4))

def moveToLeftDown():
    sleep(2)
    moveFromTo((1/4, 3/4), (3/4, 1/4))

def moveToRightUp():
    sleep(2)
    moveFromTo((3/4, 1/4), (1/4, 3/4))

def moveToRightDown():
    sleep(2)
    moveFromTo((3/4, 3/4), (1/4, 1/4))

def locateImages(*image_names, confidence=0.8, color_sensitive=False, min_saturation=40):
    """
    支持颜色敏感的图片定位。color_sensitive=True 时用OpenCV彩色（HSV）模板匹配，并排除灰色区域。
    :param image_names: 图片文件名
    :param confidence: 匹配置信度
    :param color_sensitive: 是否颜色敏感
    :param min_saturation: 最小饱和度，低于此值视为灰色不算匹配
    :return: (left, top, width, height) 或 None
    """
    import cv2
    import numpy as np
    sleep(2.5)
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

def moveFromTo(start_ratio, end_ratio, duration=2):
    """
    根据屏幕比例坐标移动鼠标，可重复多次。
    :param start_ratio: (x_ratio, y_ratio) 起始点比例
    :param end_ratio: (x_ratio, y_ratio) 结束点比例
    :param duration: 移动持续时间（秒）
    :param repeat: 重复次数
    """
    screen_width, screen_height = pa.size()

    d = fluctuate_number(duration)
    start_x = int(start_ratio[0] * screen_width)
    start_y = int(start_ratio[1] * screen_height)
    end_x = int(end_ratio[0] * screen_width)
    end_y = int(end_ratio[1] * screen_height)
    pa.moveTo(start_x, start_y, d)
    pa.mouseDown()
    sleep(1)

    pa.moveTo(end_x, end_y, d)
    pa.mouseUp()
    sleep(0.5)



