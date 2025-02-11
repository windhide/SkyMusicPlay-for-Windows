import time
import psutil
import uiautomation as auto
import win32gui
import win32process

from windhide.static.global_variable import GlobalVariable
from windhide.utils import hook_util
from windhide.utils.ocr_follow_util import get_key_position

hook_util.sout_null()


def find_window_by_uiautomation(exe_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == exe_name.lower():
            pid = proc.info['pid']
            print(f"找到 {exe_name} 进程, PID: {pid}")

            window = auto.WindowControl(searchDepth=1, ProcessId=pid)
            if window.Exists(0):
                print(f"找到窗口: {window.Name}")
                return window
    return None

def find_window_by_win32(exe_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == exe_name.lower():
            pid = proc.info['pid']
            target_hwnd = None

            def enum_callback(hwnd, _):
                nonlocal target_hwnd
                try:
                    _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if window_pid == pid:
                        target_hwnd = hwnd
                        return False  # 停止枚举
                except:
                    pass
                return True
            win32gui.EnumWindows(enum_callback, None)
            return target_hwnd
    return None

def update_window_handle():
    target_exe = "Sky.exe"
    window = find_window_by_uiautomation(target_exe)

    if window:
        hwnd = window.NativeWindowHandle
        left, top, right, bottom = window.BoundingRectangle
        width, height = right - left, bottom - top
    else:
        hwnd = find_window_by_win32(target_exe)
        if hwnd:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width, height = right - left, bottom - top
    if hwnd:
        window = GlobalVariable.window
        window["hWnd"], window["width"], window["height"] = hwnd, width, height
        window["position_x"], window["position_y"] = left, top
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
