import time

import pygetwindow as gw

from windhide.static.global_variable import GlobalVariable
from windhide.utils import hook_util
from windhide.utils.ocr_follow_util import get_key_position

hook_util.sout_null()


def is_window_alive(window):
    """检查窗口是否有效"""
    try:
        return window and window.title and window._hWnd
    except Exception:
        return False


def find_window_by_title(titles):
    """根据窗口标题列表查找窗口"""
    for title in titles:
        windows = gw.getWindowsWithTitle(title)
        for window in windows:
            if window.title == title:
                return window
    return None


def update_window_handle():
    """更新全局窗口句柄，并检测窗口宽高和位置变化"""
    target_titles = ["光·遇", "Sky"]
    window = find_window_by_title(target_titles)
    if is_window_alive(window):
        current_hwnd = window._hWnd
        current_width, current_height = window.size
        current_x, current_y = window.left, window.top
        # 更新全局变量
        GlobalVariable.window["hWnd"] = current_hwnd
        GlobalVariable.window["width"] = current_width
        GlobalVariable.window["height"] = current_height
        GlobalVariable.window["position_x"] = current_x
        GlobalVariable.window["position_y"] = current_y
        GlobalVariable.window["is_change"] = True
        try:
            get_key_position(0.5)
        except KeyError:
            print("未知原因")
        # 输出变化信息
        print(f"窗口位置：({current_x}, {current_y})，宽度：{current_width}，高度：{current_height}")
    else:
        GlobalVariable.window["hWnd"] = None
        print(f"未找到窗口")

def start_thread():
    """后台线程循环更新窗口句柄"""
    while True:
        update_window_handle()
        time.sleep(3)
