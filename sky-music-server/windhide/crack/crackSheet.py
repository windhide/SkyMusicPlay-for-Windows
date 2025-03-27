import json
import os
import time

import keyboard
import plyer
import pyautogui
import win32api
import win32con
import win32gui
import ctypes

from platformdirs import user_desktop_dir

from windhide.thread.hwnd_check_thread import find_window_by_class
from windhide.utils import hook_util
hook_util.sout_null()
ctypes.windll.shcore.SetProcessDpiAwareness(2)  # 让 Windows 以真实像素处理坐标
resultList = []
falseCount = 0
vk_code = 0x27  # 右方向键
scan_code = win32api.MapVirtualKey(vk_code, 0)
lparam = (scan_code << 16) | 1

key_areas = {
    "key0": (126, 126), "key1": (159, 126), "key2": (191, 126), "key3": (226, 126), "key4": (257, 126),
    "key5": (126, 161), "key6": (159, 161), "key7": (191, 161), "key8": (226, 161), "key9": (257, 161),
    "key10": (126, 193), "key11": (159, 193), "key12": (191, 193), "key13": (226, 193), "key14": (257, 193)
}

def get_now_column_sheet(screenshot):
    return {key: is_active(screenshot.getpixel(pos)) for key, pos in key_areas.items()}

async def crack_skySheet(bpm, interval, songName):
    """查找窗口句柄，并优化窗口大小，使客户区严格为 200x200，避免 DPI 缩放问题"""
    global falseCount
    class_name = "UnityWndClass"
    hwnd = find_window_by_class(class_name)
    resultList = []
    falseCount = 0
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 恢复窗口，以防最小化

        # **获取当前系统的 DPI 缩放系数**
        dpi = ctypes.windll.user32.GetDpiForWindow(hwnd) / 96.0  # 96 是默认 DPI（100%）

        # **计算调整后的窗口大小**
        target_client_width = 400
        target_client_height = 200
        border_width = int(20 * dpi)  # 估算边框宽度（不同 Windows 可能略有差异）
        title_height = int(40 * dpi)  # 估算标题栏高度

        window_width = int(target_client_width + border_width)
        window_height = int(target_client_height + title_height)

        # **调整窗口大小**
        win32gui.MoveWindow(hwnd, 100, 100, window_width, window_height, True)

        # **获取真实客户区的大小（防止 DPI 缩放影响）**
        client_rect = win32gui.GetClientRect(hwnd)
        client_width, client_height = client_rect[2], client_rect[3]

        # **获取客户区的屏幕坐标**
        client_x, client_y = win32gui.ClientToScreen(hwnd, (0, 0))
        while True:
            # **截图（确保 200x200）**
            screenshot = pyautogui.screenshot(region=(client_x, client_y, client_width, client_height))
            result = get_now_column_sheet(screenshot)
            falseCount = 0 if any(result.values()) else falseCount + 15
            resultList.append(result)
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 还原
            win32gui.SetForegroundWindow(hwnd)  # 置前
            keyboard.press_and_release("right")  # 模拟按下并释放右箭头键
            time.sleep(interval)
            if falseCount >= 280:
                break
            print(result)
        tran_to_time_key_formate_and_save(resultList, bpm, songName)

    else:
        plyer.notification.notify(
            title='⚠️⚠️⚠️⚠️⚠️',
            message='未检测到 Sky Studio，请启动后重试！',
            timeout=2
        )


def tran_to_time_key_formate_and_save(data_list, bpm, songName):
    bitTime = int(60.0 / float(bpm) * 1000.0)  # 计算时间间隔
    nowTimeSum = 0
    result_list = []  # 存储最终结果
    for data in data_list:
        pressed_keys = [key for key, value in data.items() if value]  # 获取所有 True 的 key
        key_count = len(pressed_keys)  # 计算当前出现的 True 数量
        if key_count > 0:  # 发现按键按下
            for key in pressed_keys:
                result_list.append({"time": nowTimeSum, "key": f"{key_count}Key{key[3:]}"})
        nowTimeSum += bitTime
    output_file = os.path.join(user_desktop_dir(), f"{songName}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([{"name": songName, "author": "crack for WindHide", "transcribedBy": "WindHide crack",
                    "bpm": int(bpm), "bitsPerPage": 15, "pitchLevel": 0, "isComposed": True,
                    "songNotes": result_list, "isEncrypted": False}], f, ensure_ascii=False,
                  indent=4)
    plyer.notification.notify(
        title='OK',
        message='破解好了',
        timeout=2
    )

    # 颜色判断（简单亮度判定）
def is_active(color):
    r, g, b = color
    return (r + g + b) > 300  # 低于 300 认为是暗色