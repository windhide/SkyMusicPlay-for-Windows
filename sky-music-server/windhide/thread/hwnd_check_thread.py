import os
import time
import traceback

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
        error_code = e.args[0]  # 获取错误码
        error_message = e.args[1]  # 获取错误消息
        error_details = e.args[2]  # 获取错误详细信息
        if error_code == 2:  # 系统找不到指定文件，忽略
            print(f"[DEBUG] EnumWindows 错误码 2：{error_message}，详细信息：{error_details}")
        else:
            # 打印错误码、消息和详细信息，同时也捕获堆栈跟踪
            print(f"[DEBUG] EnumWindows 异常:")
            print(f"  错误码: {error_code}")
            print(f"  错误消息: {error_message}")
            print(f"  错误详细信息: {error_details}")
            print("[DEBUG] 错误堆栈跟踪:")
            traceback.print_exc()  # 打印堆栈跟踪


def get_exe_name_from_hwnd(hwnd):
    # 获取窗口的 PID
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        # 使用 psutil 获取进程的 exe 路径
        process = psutil.Process(pid)
        exe_path = process.exe()  # 获取 exe 路径
        exe_name = os.path.basename(exe_path)  # 只获取文件名
        return exe_name
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def find_window_by_class(class_name):
    """根据窗口类名查找窗口句柄"""
    hwnd = win32gui.FindWindow(class_name, None)
    return hwnd

def update_window_handle():
    """查找窗口句柄，并更新全局变量"""
    if GlobalVariable.is_custom_hwnd is False:
        class_name = "TgcMainWindow"
        hwnd = find_window_by_class(class_name)
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
            GlobalVariable.hwnd_title = get_exe_name_from_hwnd(hwnd)
            get_key_position(0.60)
        else:
            GlobalVariable.window["hWnd"] = None
    else:
        GlobalVariable.hwnd_title = get_exe_name_from_hwnd(GlobalVariable.window["hWnd"])

def start_thread():
    """后台线程循环更新窗口句柄"""
    while True:
        update_window_handle()
        time.sleep(2)