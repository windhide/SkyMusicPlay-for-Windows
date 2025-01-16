import time
import pygetwindow as gw
from windhide._global import global_variable
from windhide.utils import hook_util

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
    """更新全局窗口句柄"""
    target_titles = ["光·遇", "Sky"]
    window = find_window_by_title(target_titles)
    global_variable._hWnd = window._hWnd if is_window_alive(window) else None

def start_thread():
    """后台线程循环更新窗口句柄"""
    while True:
        update_window_handle()
        time.sleep(3)
