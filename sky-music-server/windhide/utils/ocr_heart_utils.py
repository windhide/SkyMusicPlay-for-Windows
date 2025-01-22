import os

import cv2
import numpy as np
import pyautogui
import win32con
import win32gui
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
from ultralytics import YOLO
from windhide.static.global_variable import GlobalVariable
from windhide.utils.path_util import getResourcesPath

if GlobalVariable.cpu_type == 'AMD':
    from windhide.playRobot.amd_robot import PostMessageW
else:
    from windhide.playRobot.intel_robot import PostMessageW

# 全局变量，保存模型
global_friend_model = None

def load_model():
    """加载模型并保存在全局变量中"""
    global global_friend_model
    if global_friend_model is None:
        model_path = os.path.join(getResourcesPath("systemTools"), "modelData", "friend_model.pt")
        global_friend_model = YOLO(model_path)  # 加载模型并保存在 global_friend_model 中
    print("模型加载完成")
    return global_friend_model

def merge_boxes(boxes, confs, max_distance=50):
    """
    合并距离相近的识别框，合并后的框为置信度高的框。

    :param boxes: 识别框的坐标 [x1, y1, x2, y2] (形状为 [num_boxes, 4])
    :param confs: 每个框的置信度 (形状为 [num_boxes, ])
    :param max_distance: 合并框时的最大距离，单位为像素
    :return: 合并后的框的坐标和置信度
    """
    # 使用 DBSCAN 聚类算法来找出距离相近的框
    clustering = DBSCAN(eps=max_distance, min_samples=1, metric='euclidean').fit(boxes[:, :2])  # 只考虑框的中心点进行聚类

    # 聚类标签
    labels = clustering.labels_

    # 合并结果
    merged_boxes = []
    merged_confs = []

    for label in np.unique(labels):
        # 获取同一类框的索引
        indices = np.where(labels == label)[0]

        # 获取该组框的坐标和置信度
        group_boxes = boxes[indices]
        group_confs = confs[indices]

        # 选择置信度最高的框作为合并后的框
        max_conf_index = np.argmax(group_confs)
        # best_box = group_boxes[max_conf_index]

        # 计算合并后的框，使用最小外接矩形
        x1 = np.min(group_boxes[:, 0])
        y1 = np.min(group_boxes[:, 1])
        x2 = np.max(group_boxes[:, 2])
        y2 = np.max(group_boxes[:, 3])

        # 将合并后的框添加到结果列表
        merged_boxes.append([x1, y1, x2, y2])
        merged_confs.append(group_confs[max_conf_index])  # 置信度为该类中的最大置信度

    return np.array(merged_boxes), np.array(merged_confs)


def get_friend_model_position(conf, isTest=False, max_distance=50):
    # 加载已经训练好的模型
    image = get_window_screenshot_friend()
    model = load_model()
    results = model(image, conf=conf)  # 替换为你的图片路径
    boxes = results[0].boxes  # 这是检测到的所有框
    xyxy = boxes.xyxy.cpu().numpy()  # 获取每个框的绝对坐标 (x1, y1, x2, y2)
    classes = boxes.cls.cpu().numpy()  # 获取每个框对应的分类号
    confs = boxes.conf.cpu().numpy()  # 获取每个框的置信度
    class_names = ["button", "friend"]  # 获取所有类别的名称
    merged_boxes, merged_confs = merge_boxes(xyxy, confs, max_distance)

    # 获取截图的偏移量
    screenshot_offset_x = 150
    screenshot_offset_y = 110

    # 创建结果字典，专门存储合并框的中心点坐标
    result_dict = {
        "button": [],
        "friend": [],
    }

    # 填充结果字典：仅保存修正后的中心点坐标
    for i, box in enumerate(merged_boxes):
        class_id = int(classes[i])  # 获取当前合并框的类别ID
        label = class_names[class_id]  # 获取类别名称
        x1, y1, x2, y2 = box

        # 修正坐标：加上截图的偏移量
        x1 += screenshot_offset_x
        y1 += screenshot_offset_y
        x2 += screenshot_offset_x
        y2 += screenshot_offset_y

        # 计算修正后的中心点坐标
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        result_dict[label].append((center_x, center_y))

    # 如果需要可视化
    image_with_boxes = image.copy()
    for i, box in enumerate(merged_boxes):
        x1, y1, x2, y2 = box

        # 同样修正坐标
        x1 += screenshot_offset_x
        y1 += screenshot_offset_y
        x2 += screenshot_offset_x
        y2 += screenshot_offset_y

        cv2.rectangle(image_with_boxes, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(image_with_boxes, f"{merged_confs[i]:.2f}", (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    if isTest:
        plt.imshow(cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB))
        plt.axis('off')  # 不显示坐标轴
        plt.show()

    return result_dict

def get_window_screenshot_friend():
    png_path = os.path.join(getResourcesPath("systemTools"), 'modelData', 'demoScheenshot', 'demo.png')
    saturation_scale = 2.4  # >1增加饱和度，<1降低饱和度
    PostMessageW(GlobalVariable.window["hWnd"], win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    client_rect = win32gui.GetClientRect(GlobalVariable.window["hWnd"])
    # 将客户区矩形转换为屏幕坐标
    client_x1, client_y1 = win32gui.ClientToScreen(GlobalVariable.window["hWnd"], (client_rect[0], client_rect[1]))
    client_x2, client_y2 = win32gui.ClientToScreen(GlobalVariable.window["hWnd"], (client_rect[2], client_rect[3]))
    # 截取窗口客户区范围内的图像
    screenshot = pyautogui.screenshot(
        region=(client_x1 + 150, client_y1 + 80, client_x2 - client_x1 - 230, client_y2 - client_y1 - 150))
    _, s_channel, _ = cv2.split(cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2HSV))
    d = np.clip(s_channel * saturation_scale, 0, 255).astype(np.uint8)
    cv2.imwrite(png_path, d)
    image = cv2.imread(png_path)
    return image
