#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visualize_barcode_only.py

功能：
 1. 读取 IMAGE_PATH 指定的图片
 2. 用自训练的条码权重检测 "barcode"
 3. 可视化：在原图上绘制所有 barcode 框和置信度，并展示
"""

import os
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# —— 配置 —— #
IMAGE_PATH    = 'test_data/DJI_20250424162618_0274_V.jpeg'  # 要可视化的那张图
BARCODE_MODEL = 'weights/best.pt'                          # 你训练好的条码模型

def visualize_barcode():
    # 1) 加载 Barcode 模型
    model = YOLO(BARCODE_MODEL)

    # 2) 打开图片
    img = Image.open(IMAGE_PATH).convert('RGB')

    # 3) 运行检测
    results = model(IMAGE_PATH)

    # 4) 在原图上绘制 barcode 框和置信度
    draw = ImageDraw.Draw(img)
    # 如果你想用更清晰的文字，可自行指定系统字体路径：
    try:
        font = ImageFont.truetype("arial.ttf", size=20)
    except:
        font = ImageFont.load_default()
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        # 画框
        draw.rectangle([x1, y1, x2, y2], outline='red', width=3)
        # 标注置信度
        text = f"{conf:.2f}"
        draw.text((x1, y1 - 18), text, fill='red', font=font)

    # 5) 显示结果
    plt.figure(figsize=(12,8))
    plt.imshow(img)
    plt.axis('off')
    plt.title(f"Barcode Detection — {os.path.basename(IMAGE_PATH)}")
    plt.show()

if __name__ == "__main__":
    visualize_barcode()
