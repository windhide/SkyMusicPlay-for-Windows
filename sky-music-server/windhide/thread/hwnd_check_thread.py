import time

import pygetwindow as gw

from windhide._global import global_variable
from windhide.utils import hook_util

hook_util.sout_null()

def is_window_alive(window):
    try:
        return window.title != "" and window._hWnd is not None
    except Exception:
        return False

def startThread():
    while True:
        # 获取窗口
        china = gw.getWindowsWithTitle("光·遇")
        wide = gw.getWindowsWithTitle("Sky")
        if china and len(china) > 0:
            window_china = china[0]
            if is_window_alive(window_china):
                global_variable._hWnd = window_china._hWnd
            else:
                global_variable._hWnd = None
        elif wide and len(wide) > 0:
            window_wide = wide[0]
            if is_window_alive(window_wide):
                global_variable._hWnd = window_wide._hWnd
            else:
                global_variable._hWnd = None
        else:
            global_variable._hWnd = None
        # 每隔一段时间检查一次
        time.sleep(3)