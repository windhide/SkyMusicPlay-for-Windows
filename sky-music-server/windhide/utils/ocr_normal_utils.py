import os
import cv2
import numpy as np
import pyautogui
import win32con
import win32gui
from windhide.playRobot.amd_robot import PostMessageW
from windhide.static.global_variable import GlobalVariable
from windhide.utils.play_path_util import getResourcesPath


def resetGameFrame():
    win32gui.ShowWindow(GlobalVariable.hWnd, win32con.SW_RESTORE)  # 先恢复窗口，以防最小化
    rect = win32gui.GetWindowRect(GlobalVariable.hWnd)
    x, y = rect[0], rect[1]  # 保持窗口的左上角位置不变
    win32gui.MoveWindow(GlobalVariable.hWnd, x, y, 1280, 720, True)


def get_window_screenshot_friend():
    png_path = os.path.join(getResourcesPath("systemTools"), 'modelData', 'demoScheenshot', 'demo.png')
    saturation_scale = 2.4  # >1增加饱和度，<1降低饱和度
    PostMessageW(GlobalVariable.hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    client_rect = win32gui.GetClientRect(GlobalVariable.hWnd)
    # 将客户区矩形转换为屏幕坐标
    client_x1, client_y1 = win32gui.ClientToScreen(GlobalVariable.hWnd, (client_rect[0], client_rect[1]))
    client_x2, client_y2 = win32gui.ClientToScreen(GlobalVariable.hWnd, (client_rect[2], client_rect[3]))
    # 截取窗口客户区范围内的图像
    screenshot = pyautogui.screenshot(
        region=(client_x1 + 150, client_y1 + 80, client_x2 - client_x1 - 230, client_y2 - client_y1 - 150))
    _, s_channel, _ = cv2.split(cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2HSV))
    d = np.clip(s_channel * saturation_scale, 0, 255).astype(np.uint8)
    cv2.imwrite(png_path, d)
    image = cv2.imread(png_path)
    return image


def get_window_screenshot():
    """获取指定窗口的截图"""
    # 获取窗口位置和大小
    PostMessageW(GlobalVariable.hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    rect = win32gui.GetWindowRect(GlobalVariable.hWnd)
    x1, y1, x2, y2 = rect
    # 截取窗口范围内的图像
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)