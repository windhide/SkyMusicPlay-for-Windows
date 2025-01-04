import pygetwindow as gw
import time
from windhide._global import globalVariable
from windhide.thread import hook_utils
from threading import Thread

hook_utils.sout_null()

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
                globalVariable._hWnd = window_china._hWnd
            else:
                globalVariable._hWnd = None
        elif wide and len(wide) > 0:
            window_wide = wide[0]
            if is_window_alive(window_wide):
                globalVariable._hWnd = window_wide._hWnd
            else:
                globalVariable._hWnd = None
        else:
            globalVariable._hWnd = None
        # 每隔一段时间检查一次
        print("当前状态",globalVariable._hWnd)
        time.sleep(3)