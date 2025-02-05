import time

import psutil
import pywintypes
import win32gui
import win32process

from windhide.static.global_variable import GlobalVariable
from windhide.utils import hook_util
from windhide.utils.ocr_follow_util import get_key_position

hook_util.sout_null()


def safe_enum_windows(callback):
    """封装 EnumWindows 调用，捕获特定异常，防止异常中断调用链"""
    try:
        win32gui.EnumWindows(callback, None)
    except pywintypes.error as e:
        if e.args[0] == 2:  # 系统找不到指定文件，忽略
            print(f"[DEBUG] EnumWindows 错误码 2：{e}")
        else:
            print(f"[DEBUG] EnumWindows 异常: {e}")


def find_window_by_exe(exe_names):
    """根据 exe 名称列表查找窗口句柄"""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in exe_names:
            pid = proc.info['pid']
            target_hwnd = None

            def enum_callback(hwnd, _):
                nonlocal target_hwnd
                try:
                    _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if window_pid == pid:
                        target_hwnd = hwnd
                        return False  # 停止枚举
                except pywintypes.error as e:
                    print(f"[DEBUG] EnumWindows 回调异常: {e}")
                return True

            safe_enum_windows(enum_callback)
            if target_hwnd:
                return target_hwnd
    return None


def update_window_handle():
    """查找窗口句柄，并更新全局变量"""
    target_exes = ["光·遇.exe", "Sky.exe"]
    hwnd = find_window_by_exe(target_exes)

    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width, height = right - left, bottom - top

        window = GlobalVariable.window
        window["hWnd"], window["width"], window["height"] = hwnd, width, height
        window["position_x"], window["position_y"] = left, top

        # 仅在窗口信息发生变化时设置 is_change
        if any([
            window["width"] != width,
            window["height"] != height,
            window["position_x"] != left,
            window["position_y"] != top,
        ]):
            window["is_change"] = True

        get_key_position(0.45)
    else:
        GlobalVariable.window["hWnd"] = None


def start_thread():
    """后台线程循环更新窗口句柄"""
    while True:
        update_window_handle()
        time.sleep(2)
