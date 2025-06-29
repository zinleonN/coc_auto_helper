import cv2
import numpy as np
import pyautogui
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime
import os
import time

MODEL_PATH = "src/best.pt"  # 模型路径
OUTPUT_DIR = "detection_results"  # 输出目录

def capture_screenshot():
    """
    捕获屏幕截图
    :return: 截图 (BGR格式的numpy数组)
    """
    # 捕获屏幕
    screenshot = pyautogui.screenshot()
    
    # 转换为OpenCV格式 (BGR)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    return screenshot

def plot_detections(screenshot, result, conf_threshold=0.4):
    """
    在图像上绘制检测结果
    :param screenshot: 原始图像
    :param result: YOLO检测结果
    :param conf_threshold: 置信度阈值
    :return: 标注后的图像
    """
    # 创建原始图像的副本
    annotated_img = screenshot.copy()
    
    # 定义绘图参数
    box_thickness = max(round(sum(annotated_img.shape) / 2 * 0.002), 1)  # 更细的边界框
    font_scale = 0.5  # 更小的字体
    font_thickness = max(box_thickness - 1, 1)  # 更细的字体笔画
    
    # 定义颜色 (BGR格式)
    color_map = {
        0: (0, 165, 255),    # 橙色 - dark elixir drill
        1: (50, 205, 50),    # 绿色 - elixir collector
        2: (255, 50, 50),    # 蓝色 - gold mine
    }
    
    # 绘制每个检测框
    for box in result.boxes:
        if box.conf < conf_threshold:
            continue
            
        class_id = int(box.cls)
        class_name = result.names[class_id]
        confidence = box.conf.item()
        
        # 获取边界框坐标
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        
        # 选择颜色
        color = color_map.get(class_id, (0, 255, 255))  # 默认黄色
        
        # 绘制边界框
        cv2.rectangle(
            annotated_img,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            color,
            box_thickness
        )
        
        # 创建标签文本 - 更简洁的格式
        label = f"{class_name} {confidence:.2f}"
        
        # 计算文本大小
        (text_width, text_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
        )
        
        # 计算文本背景位置 (放在框内顶部)
        text_bg_x1 = int(x1)
        text_bg_y1 = max(int(y1) - text_height - 4, 0)  # 确保不超出图像顶部
        text_bg_x2 = int(x1) + text_width
        text_bg_y2 = int(y1)
        
        # 绘制文本背景
        cv2.rectangle(
            annotated_img,
            (text_bg_x1, text_bg_y1),
            (text_bg_x2, text_bg_y2),
            color,
            -1  # 填充矩形
        )
        
        # 绘制文本 (放在框内)
        cv2.putText(
            annotated_img,
            label,
            (int(x1), int(y1) - 2),  # 文本位置 (框内顶部)
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (255, 255, 255),  # 白色文本
            font_thickness,
            lineType=cv2.LINE_AA
        )
    
    return annotated_img

def record_and_detect_video(record_seconds=5, conf_threshold=0.4, fps=10):
    """
    录制屏幕视频并在视频中实时进行目标检测
    :param record_seconds: 录制时长(秒)
    :param conf_threshold: 置信度阈值
    :param fps: 视频帧率
    :return: 视频文件路径
    """
    # 确保输出目录存在
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # 生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_video_path = os.path.join(OUTPUT_DIR, f"detection_{timestamp}.mp4")
    
    # 获取屏幕尺寸
    screen_size = pyautogui.size()
    width, height = screen_size
    
    # 创建视频编码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    # 加载模型
    model = YOLO(MODEL_PATH)
    
    print(f"开始录制 {record_seconds} 秒视频 (FPS: {fps})...")
    start_time = time.time()
    
    # 创建显示窗口
    cv2.namedWindow("实时检测", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("实时检测", width // 2, height // 2)
    
    frame_count = 0
    while time.time() - start_time < record_seconds:
        # 捕获屏幕
        frame = capture_screenshot()
        
        # 进行推理
        results = model.predict(
            source=frame,
            conf=conf_threshold,
            verbose=False,  # 不输出详细信息
            imgsz=640  # 固定输入尺寸以提高速度
        )
        
        # 处理结果
        if results:
            result = results[0]
            # 绘制检测结果
            frame = plot_detections(frame, result, conf_threshold)
            
            # 显示检测到的目标数量
            cv2.putText(frame, f"目标数量: {len(result.boxes)}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 写入视频帧
        video_writer.write(frame)
        frame_count += 1
        
        # 显示实时画面
        display_frame = cv2.resize(frame, (width // 2, height // 2))
        cv2.imshow("实时检测", display_frame)
        
        # 按ESC键可提前退出
        if cv2.waitKey(1) == 27:
            break
    
    # 释放资源
    video_writer.release()
    cv2.destroyAllWindows()
    
    # 计算实际帧率
    actual_fps = frame_count / record_seconds
    print(f"录制完成！保存至: {output_video_path}")
    print(f"总帧数: {frame_count}, 实际帧率: {actual_fps:.1f} FPS")
    
    return output_video_path

# 使用示例
if __name__ == "__main__":
    # 检查模型是否存在
    if not Path(MODEL_PATH).exists():
        print(f"错误: 找不到模型文件 {MODEL_PATH}")
        print("请先训练模型或提供正确的模型路径")
    else:
        # 调用视频录制和检测函数
        video_path = record_and_detect_video(
            record_seconds=10,  # 录制5秒
            conf_threshold=0.36,
            fps=10  # 目标帧率
        )
        
        if video_path:
            print("检测完成！")
            # 在文件管理器中打开结果目录（Windows系统）
            if os.name == 'nt':  # Windows
                os.startfile(OUTPUT_DIR)