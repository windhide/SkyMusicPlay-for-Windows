import cv2
import numpy as np
import pyautogui
import win32con
import win32gui

from windhide._global import global_variable


def match_template_and_return_coordinates(source_image, template_image_path, match_threshold=0.8):
    # 读取模板图像
    template_image = cv2.imread(template_image_path, cv2.IMREAD_COLOR)
    if source_image is None or template_image is None:
        raise FileNotFoundError("无法加载原始图像或模板图像，请检查路径或截图是否成功！")

    # 转为灰度图
    gray_source_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
    gray_template_image = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    # 使用Canny边缘检测提取边缘
    edges_source = cv2.Canny(gray_source_image, 50, 150)
    edges_template = cv2.Canny(gray_template_image, 50, 150)

    # 进行模板匹配
    result = cv2.matchTemplate(edges_source, edges_template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= match_threshold)

    center_coordinates = []
    for point in zip(*locations[::-1]):  # 转换坐标顺序为 (x, y)
        top_left = point
        # 计算中心点坐标
        center_x = top_left[0] + edges_template.shape[1] // 2
        center_y = top_left[1] + edges_template.shape[0] // 2
        center_coordinates.append({"x": int(center_x), "y": int(center_y)})  # 返回中心点坐标 (x, y)
    filtered_points = []
    for point in center_coordinates:
        # 假设当前点是有效的
        is_valid = True
        # 检查当前点与已过滤点之间的差异
        for filtered_point in filtered_points:
            if abs(point['x'] - filtered_point['x']) < 10 or abs(point['y'] - filtered_point['y']) < 10:
                is_valid = False
                break
        # 如果当前点是有效的，则将其添加到结果数组中
        if is_valid:
            filtered_points.append(point)

    return filtered_points


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
