import ctypes
import threading
import time
from ctypes import windll

import keyboard
import pyautogui
import win32con
import win32gui

from windhide._global import global_variable
from windhide._global.global_variable import is_post_w
from windhide.thread.amd_play_thread import ControlledThread
from windhide.utils.music_file_transelate import convert_notes_to_delayed_format

PostMessageW = windll.user32.PostMessageW # ok 消息队列
SendMessageW = windll.user32.SendMessageW # ok 立即处理
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanW = windll.user32.VkKeyScanW
user32 = ctypes.windll.user32

WM_KEYDOWN = 0x100
WM_KEYUP = 0x101
pyautogui.FAILSAFE = False

def send_single_key_to_window_task(key):
    """发送单个按键，减少延迟"""
    key_down(key)
    time.sleep(global_variable.sustain_time)
    key_up(key)

def send_multiple_key_to_window_task(keys):
    """发送组合按键，减少延迟"""
    for key in keys:
        key_down(key)
    time.sleep(global_variable.sustain_time)
    for key in keys:
        key_up(key)


# 现在给模拟器和跟弹在用了
def send_single_key_to_window_follow(key):
    """发送单个按键，减少延迟"""
    keyboard.press(key)
    time.sleep(global_variable.sustain_time)
    keyboard.release(key)

 # 现在给模拟器和跟弹在用了
def send_multiple_key_to_window_follow(keys):
    """发送组合按键，减少延迟"""
    for key in keys:
        keyboard.press(key)
    time.sleep(global_variable.sustain_time)
    for key in keys:
        keyboard.release(key)

def execute_in_thread(target, *args, **kwargs):
    """通用线程执行器，采用线程池管理"""
    thread = threading.Thread(target=target, args=args, kwargs=kwargs)
    thread.daemon = True  # 将线程设置为守护线程，程序退出时自动结束线程
    thread.start()
    return thread

def send_single_key_to_window(key):
    """发送单个按键（新线程中执行）"""
    if global_variable.compatibility_mode:
        execute_in_thread(send_single_key_to_window_follow, key)
    else:
        execute_in_thread(send_single_key_to_window_task, key)

def send_multiple_key_to_window(keys):
    """发送组合按键（新线程中执行）"""
    if global_variable.compatibility_mode:
        execute_in_thread(send_multiple_key_to_window_follow, keys)
    else:
        execute_in_thread(send_multiple_key_to_window_task, keys)

def playMusic(fileName, type):
    """优化音乐播放逻辑，只加载乐谱数据一次"""
    convert_notes_to_delayed_format(fileName, type)
    if global_variable.thread != None:
        stop()
    global_variable.thread = ControlledThread()
    global_variable.thread.start()

def resume():
    """恢复播放"""
    if global_variable.thread:
        global_variable.thread.resume()

def pause():
    """暂停播放"""
    if global_variable.thread:
        global_variable.thread.pause()

def stop():
    """停止播放"""
    if global_variable.thread:
        global_variable.thread.stop()
        global_variable.set_progress = 0
        global_variable.thread = None


#  点击，按下

def click_window_position(x: int, y: int):
    # 获取窗口的屏幕位置
    window_rect = win32gui.GetWindowRect(global_variable._hWnd)  # 返回 (left, top, right, bottom)
    window_x, window_y = window_rect[0], window_rect[1]
    client_x = window_x + x
    client_y = window_y + y
    win32gui.SendMessage(global_variable._hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    pyautogui.moveTo(client_x, client_y, duration=0)
    pyautogui.click()

#  核心
def key_press(key: str):
    key = key.lower()
    if key in special_keys:
        vk_code, scan_code = special_keys[key]
    else:
        # 普通按键的处理
        vk_code = VkKeyScanW(ctypes.c_wchar(key))
        scan_code = keyboard.key_to_scan_codes(key)[0] if key != '/' else keyboard.key_to_scan_codes(key)[1]
    lparam = (scan_code << 16) | 1
    if is_post_w:
        PostMessageW(global_variable._hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        PostMessageW(global_variable._hWnd, WM_KEYDOWN, vk_code, lparam)
        time.sleep(0.01)
        PostMessageW(global_variable._hWnd, WM_KEYUP, vk_code, lparam)
    else:
        SendMessageW(global_variable._hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        SendMessageW(global_variable._hWnd, WM_KEYDOWN, vk_code, lparam)
        time.sleep(0.01)
        SendMessageW(global_variable._hWnd, WM_KEYUP, vk_code, lparam)

def key_down(key: str):
    set_us_keyboard_layout()
    key = key.lower()
    if key in special_keys:
        vk_code, scan_code = special_keys[key]
    else:
        # 普通按键的处理
        vk_code = VkKeyScanW(ctypes.c_wchar(key))
        scan_code = keyboard.key_to_scan_codes(key)[0] if key != '/' else keyboard.key_to_scan_codes(key)[1]
    lparam = (scan_code << 16) | 1
    if is_post_w:
        PostMessageW(global_variable._hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        PostMessageW(global_variable._hWnd, WM_KEYDOWN, vk_code, lparam)
    else:
        SendMessageW(global_variable._hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        SendMessageW(global_variable._hWnd, WM_KEYDOWN, vk_code, lparam)

def key_up(key: str):
    key = key.lower()
    if key in special_keys:
        vk_code, scan_code = special_keys[key]
    else:
        # 普通按键的处理
        vk_code = VkKeyScanW(ctypes.c_wchar(key))
        scan_code = keyboard.key_to_scan_codes(key)[0] if key != '/' else keyboard.key_to_scan_codes(key)[1]
    lparam = (scan_code << 16) | 0XC0000001
    if is_post_w:
        PostMessageW(global_variable._hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        PostMessageW(global_variable._hWnd, WM_KEYUP, vk_code, lparam)
    else:
        SendMessageW(global_variable._hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        SendMessageW(global_variable._hWnd, WM_KEYUP, vk_code, lparam)

def mouse_wheel_scroll(operator):
    match operator:
        case 'up':
            delta =  3000
        case 'down':
            delta = -3000
    window_rect = win32gui.GetWindowRect(global_variable._hWnd)  # 返回 (left, top, right, bottom)
    # 窗口中心
    window_x, window_y = window_rect[0] + window_rect[0] / 2, window_rect[1] + window_rect[1] / 2
    # 激活窗口
    if is_post_w:
        PostMessageW(global_variable._hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    else:
        SendMessageW(global_variable._hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    pyautogui.moveTo(window_x, window_y)
    pyautogui.scroll(delta)


def set_us_keyboard_layout():
    # LoadKeyboardLayoutW 函数的定义
    user32.LoadKeyboardLayoutW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint]
    user32.LoadKeyboardLayoutW.restype = ctypes.c_void_p
    user32.LoadKeyboardLayoutW("00000409", 1)  # 0409 是美国键盘布局标识符，1 表示激活

special_keys = {
    'space': (0x20, 0x39),  # 虚拟键码和扫描码
    'tab': (0x09, 0x0F),
    'esc': (0x1B, 0x01),
    'shift': (0x10, 0x2A)  # 左 Shift 键
}
