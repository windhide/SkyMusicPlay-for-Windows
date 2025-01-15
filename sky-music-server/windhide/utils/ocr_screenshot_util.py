import os
import time

import cv2
import numpy as np
import pyautogui
import win32con
import win32gui
from ultralytics import YOLO

from windhide._global import global_variable
from windhide.utils.path_util import getResourcesPath

# 全局变量，保存模型
global_model = None
global_button_model = None

def load_model():
    """加载模型并保存在全局变量中"""
    global global_model
    if global_model is None:
        model_path = os.path.join(getResourcesPath("systemTools"), "modelData", "heart_model.pt")
        global_model = YOLO(model_path)  # 加载模型并保存在 global_model 中
    print("模型加载完成")
    return global_model


def load_key_model():
    """加载模型并保存在全局变量中"""
    global global_button_model
    if global_button_model is None:
        button_model_path = os.path.join(getResourcesPath("systemTools"), "modelData", "check_key_model.pt")
        global_button_model = YOLO(button_model_path)  # 加载模型并保存在 global_model 中
    print("模型加载完成")
    return global_button_model


def get_model_position(conf):
    # 加载已经训练好的模型
    image = get_window_screenshot()
    model = load_model()
    results = model(image, conf=conf)  # 替换为你的图片路径
    boxes = results[0].boxes  # 这是检测到的所有框
    xyxy = boxes.xyxy.cpu().numpy()  # 获取每个框的绝对坐标 (x1, y1, x2, y2)
    classes = boxes.cls.cpu().numpy()  # 获取每个框对应的分类号
    class_names = ["button", "get_fire", "send_fire"]  # 获取所有类别的名称
    result_dict = {
        "button": [],
        "get_fire": [],
        "send_fire": [],
    }
    # 打印绝对坐标和分类号
    for i, box in enumerate(xyxy):
        x1, y1, x2, y2 = box
        class_id = int(classes[i])  # 获取类别ID
        label = class_names[class_id]  # 获取类别名称
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        result_dict[label].append({"x": int(center_x), "y": int(center_y)})
    # results[0].show()
    return result_dict


def get_key_position(conf):
    image = get_window_screenshot()
    model = load_key_model()
    results = model(image, conf=conf)  # 替换为你的图片路径
    boxes = results[0].boxes  # 这是检测到的所有框
    xyxy = boxes.xyxy.cpu().numpy()  # 获取每个框的绝对坐标 (x1, y1, x2, y2)
    classes = boxes.cls.cpu().numpy()  # 获取每个框对应的分类号
    class_names = ["key"]  # 获取所有类别的名称
    result_dict = {
        "key": []
    }
    # 打印绝对坐标和分类号
    for i, box in enumerate(xyxy):
        x1, y1, x2, y2 = box
        class_id = int(classes[i])  # 获取类别ID
        label = class_names[class_id]  # 获取类别名称
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        result_dict[label].append({"x": int(center_x), "y": int(center_y)})
    # results[0].show()
    return result_dict

def test_model_position(conf):
    resetGameFrame()
    time.sleep(1)
    image = get_window_screenshot()
    model = load_model()
    results = model(image, conf=conf)  # 替换为你的图片路径
    results[0].show()


def test_key_model_position(conf):
    time.sleep(1)
    image = get_window_screenshot()
    model = load_key_model()
    results = model(image, conf=conf)  # 替换为你的图片路径
    results[0].show()

def resetGameFrame():
    win32gui.ShowWindow(global_variable._hWnd, win32con.SW_RESTORE)  # 先恢复窗口，以防最小化
    rect = win32gui.GetWindowRect(global_variable._hWnd)
    x, y = rect[0], rect[1]  # 保持窗口的左上角位置不变
    win32gui.MoveWindow(global_variable._hWnd, x, y, 1280, 720, True)

def get_window_screenshot():
    """获取指定窗口的截图"""
    # 获取窗口位置和大小
    rect = win32gui.GetWindowRect(global_variable._hWnd)
    x1, y1, x2, y2 = rect
    # 截取窗口范围内的图像
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
