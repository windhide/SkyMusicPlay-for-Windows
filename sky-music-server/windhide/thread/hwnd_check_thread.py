import time
import psutil
import win32gui
import win32process

from windhide.static.global_variable import GlobalVariable
from windhide.utils import hook_util
from windhide.utils.ocr_follow_util import get_key_position

hook_util.sout_null()


def is_window_alive(hwnd):
    try:
        title = win32gui.GetWindowText(hwnd)
        if hwnd and title:
            return True
        return False
    except Exception:
        return False


def find_window_by_exe(exe_names):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in exe_names:
            pid = proc.info['pid']
            target_hwnd = None

            def enum_callback(hwnd, lParam):
                nonlocal target_hwnd
                if win32gui.IsWindowVisible(hwnd):
                    _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if window_pid == pid:
                        target_hwnd = hwnd
                        return False
                return True

            win32gui.EnumWindows(enum_callback, None)
            if target_hwnd:
                return target_hwnd
    return None

def update_window_handle():
    # 修改目标 exe 列表，根据实际情况填写
    target_exes = ["光·遇.exe", "Sky.exe"]
    hwnd = find_window_by_exe(target_exes)
    if is_window_alive(hwnd):
        # 获取窗口矩形：(left, top, right, bottom)
        rect = win32gui.GetWindowRect(hwnd)
        current_x, current_y, right, bottom = rect
        current_width = right - current_x
        current_height = bottom - current_y

        # 更新全局变量
        GlobalVariable.window["hWnd"] = hwnd
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
        print("未找到窗口")


def start_thread():
    """后台线程循环更新窗口句柄"""
    while True:
        update_window_handle()
        time.sleep(3)
