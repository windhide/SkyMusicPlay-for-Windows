import psutil
import win32gui
import win32process
import os
from windhide.static.global_variable import GlobalVariable


def get_running_apps():
    apps = []
    # 获取当前系统运行的所有进程
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            exe_path = proc.exe()
            if 'System' in name or 'svchost' in name:
                continue
            def enum_windows(hwnd, lParam):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if window_title:
                        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                        if window_pid == pid:
                            apps.append({
                                'title': window_title,
                                'exe_name': os.path.basename(exe_path),
                                'pid': pid,
                                'hwnd': hwnd
                            })
            win32gui.EnumWindows(enum_windows, None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return apps

def get_running_apps_by_struct(check_struct):
    if any(item == check_struct for item in get_running_apps()) is True:
        GlobalVariable.hwnd_select_struct = check_struct
        GlobalVariable.window["hWnd"] = check_struct["hwnd"]
        GlobalVariable.is_custom_hwnd = True
    else:
        GlobalVariable.is_custom_hwnd = False
