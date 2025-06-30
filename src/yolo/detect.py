import cv2
import numpy as np
import pyautogui
from ultralytics import YOLO

model = YOLO("src/yolo/best.pt")


def detect_objects_from_screenshot(screenshot, conf_threshold=0.4):
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    
    # 加载YOLO模型
    
    # 进行目标检测
    results = model.predict(
        source=screenshot_bgr,
        conf=conf_threshold,
        verbose=False,
        imgsz=640
    )
    
    # 解析检测结果
    detected_objects = []
    if results:
        result = results[0]
        for box in result.boxes:
            # 获取检测信息
            class_id = int(box.cls)
            class_name = result.names[class_id]
            confidence = box.conf.item()
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            # 添加到结果列表
            detected_objects.append({
                "class_name": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2],
                "center": [(x1 + x2) / 2, (y1 + y2) / 2]
            })
    
    return detected_objects

def calculate_avg_distance_to_line(k, x0, y0):
    """计算所有检测点到直线的平均距离
    
    Args:
        k: 直线斜率
        x0, y0: 直线经过的点坐标
    
    Returns:
        float: 所有检测点到直线的平均距离
    """
    import pyautogui
    import numpy as np

    # 计算直线截距 (y = kx + b)
    b = y0 - k * x0
    
    # 获取屏幕截图
    screenshot = pyautogui.screenshot()
    
    # 检测对象
    detected_objects = detect_objects_from_screenshot(screenshot)  # 假设该函数已实现
    total_distance = 0
    count = 0

    # 处理每个检测到的对象
    for obj in detected_objects:
        cx, cy = obj['center']
        count += 1
        
        # 计算点到直线的距离: |kx - y + b|/√(k²+1)
        numerator = abs(k * cx - cy + b)
        denominator = np.sqrt(k**2 + 1)
        distance = numerator / denominator
        
        # 特定类别距离减半
        if obj['class_name'] == 'elixir collector':
            distance *= 0.5
            
        total_distance += distance

    # 返回平均距离
    return total_distance / count if count > 0 else float('inf')