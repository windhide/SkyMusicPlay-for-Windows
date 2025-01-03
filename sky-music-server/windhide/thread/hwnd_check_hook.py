import pygetwindow as gw
import time
from windhide._global import globalVariable
from windhide.thread import hook_utils
from threading import Thread

hook_utils.sout_null()

def startThread():
    while True:
        # 获取窗口
        china = gw.getWindowsWithTitle("光·遇")
        wide = gw.getWindowsWithTitle("Sky: Children of Light")
        if china and len(china) > 0:
            window_china = china[0]
            if window_china.isAlive() and not window_china.isMinimized():
                globalVariable._hWnd = window_china
            else:
                globalVariable._hWnd = None
        elif wide and len(wide) > 0:
            window_wide = wide[0]
            if window_wide.isAlive() and not window_wide.isMinimized():
                globalVariable._hWnd = window_wide
            else:
                globalVariable._hWnd = None
        else:
            globalVariable._hWnd = None
        # 每隔一段时间检查一次
        time.sleep(3)