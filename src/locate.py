import pyautogui
import time
import logging

def get_mouse_position_as_ratio():
    """
    获取当前鼠标位置的屏幕比例坐标 (x_ratio, y_ratio)。
    :return: (x_ratio, y_ratio)
    """
    x, y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    x_ratio = x / screen_width
    y_ratio = y / screen_height
    return x_ratio, y_ratio

time.sleep(2)  # 等待2秒以便用户将鼠标移动到目标位置
ratio = get_mouse_position_as_ratio()
logging.info(ratio)  # 输出 (x_ratio, y_ratio)