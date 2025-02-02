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
    """
    封装 EnumWindows 调用，捕获特定异常，防止异常中断调用链。
    """
    try:
        win32gui.EnumWindows(callback, None)
    except pywintypes.error as e:
        # 错误码 2: 系统找不到指定的文件，此处直接忽略
        if e.args[0] == 2:
            print(f"[DEBUG] EnumWindows 错误码 2：{e}")
        else:
            print(f"[DEBUG] EnumWindows 异常: {e}")


def find_window_by_exe(exe_names):
    """
    根据 exe 文件名列表查找窗口句柄：
    遍历所有进程，匹配 exe 名称；对匹配进程，枚举所有窗口，
    当窗口所属进程 id 与目标进程 id 匹配时，即返回该窗口句柄。
    """
    found_hwnd = None
    # 遍历所有进程
    for proc in psutil.process_iter(['pid', 'name']):
        proc_name = proc.info.get('name', '')
        if proc_name in exe_names:
            pid = proc.info['pid']
            # print(f"[DEBUG] 找到目标进程: {proc_name} (PID: {pid})")
            target_hwnd = None

            def enum_callback(hwnd, lParam):
                nonlocal target_hwnd
                try:
                    _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                    # 判断窗口所属进程 id 是否匹配
                    if window_pid == pid:
                        target_hwnd = hwnd
                        # print(f"[DEBUG] 匹配到窗口句柄: {hwnd} (属于 PID: {window_pid})")
                        return False  # 找到后停止枚举
                except pywintypes.error as e:
                    print(f"[DEBUG] EnumWindows 回调异常: {e}")
                return True

            safe_enum_windows(enum_callback)
            if target_hwnd:
                found_hwnd = target_hwnd
                break  # 找到一个符合条件的窗口后退出循环
            else:
                print(f"[DEBUG] 进程 {proc_name} (PID: {pid}) 未找到对应窗口。")
    # if found_hwnd:
    #     print(f"[DEBUG] 返回窗口句柄: {found_hwnd}")
    # else:
    #     print("[DEBUG] 未找到符合条件的窗口句柄。")
    return found_hwnd


def update_window_handle():
    """
    根据目标 exe 列表查找窗口句柄，并更新全局变量：
    当目标 exe 正在运行时，通过窗口句柄获取窗口位置、宽高等信息，
    并调用 get_key_position 进行键位检测。否则，清空句柄信息。
    """
    target_exes = ["光·遇.exe", "Sky.exe"]
    hwnd = find_window_by_exe(target_exes)
    if hwnd is not None:
        rect = win32gui.GetWindowRect(hwnd)
        current_x, current_y, right, bottom = rect
        current_width = right - current_x
        current_height = bottom - current_y

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

        # print(f"窗口位置：({current_x}, {current_y})，宽度：{current_width}，高度：{current_height}")
    else:
        GlobalVariable.window["hWnd"] = None
        # print("未找到窗口")


def start_thread():
    """后台线程循环更新窗口句柄"""
    while True:
        update_window_handle()
        time.sleep(3)
