import ctypes

import cv2
import numpy as np
import pyautogui
import win32con
import win32gui

from windhide.static.global_variable import GlobalVariable


def resetGameFrame():
    win32gui.ShowWindow(GlobalVariable.window["hWnd"], win32con.SW_RESTORE)  # 先恢复窗口，以防最小化
    rect = win32gui.GetWindowRect(GlobalVariable.window["hWnd"])
    x, y = rect[0], rect[1]  # 保持窗口的左上角位置不变
    win32gui.MoveWindow(GlobalVariable.window["hWnd"], x, y, 1280, 720, True)

def get_window_screenshot():
    """获取指定窗口的截图"""
    # 获取窗口位置和大小
    # PostMessageW(GlobalVariable.window["hWnd"], win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    rect = win32gui.GetWindowRect(GlobalVariable.window["hWnd"])
    x1, y1, x2, y2 = rect
    # 截取窗口范围内的图像
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def get_system_dpi():
    hdc = ctypes.windll.user32.GetDC(0)  # 获取屏幕设备上下文
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX = 88
    ctypes.windll.user32.ReleaseDC(0, hdc)  # 释放设备上下文
    return dpi

def get_game_position():
    hwnd = GlobalVariable.window["hWnd"]
    # 获取窗口物理坐标
    rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    # 获取窗口 DPI 缩放比例
    scale_factor = get_system_dpi() / 96.0  # DPI 标准比例为 96
    # 计算边框和标题栏的逻辑偏移
    border_x = (rect[2] - rect[0] - client_rect[2]) // 2
    border_y = (rect[3] - rect[1] - client_rect[3] - border_x)
    # 转换物理坐标为逻辑坐标，去掉边框和标题栏
    x1 = int((rect[0] + border_x) / scale_factor)
    y1 = int((rect[1] + border_y) / scale_factor)
    x2 = int((rect[2] - border_x) / scale_factor)
    y2 = int((rect[3] - border_y) / scale_factor)
    return x1, y1, x2, y2