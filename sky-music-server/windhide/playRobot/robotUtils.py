import threading

import keyboard

from windhide._global import globalVariable
from windhide.utils.musicFileTranselate import convert_notes_to_delayed_format
from windhide.utils.playThread import ControlledThread
import ctypes
import time
from ctypes import windll
import pygetwindow as gw
import win32con
import win32gui


PostMessageW = windll.user32.PostMessageW
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA
user32 = ctypes.windll.user32

WM_KEYDOWN = 0x100
WM_KEYUP = 0x101


def send_single_key_to_window_task(key):
    """发送单个按键，减少延迟"""
    key_down(key)
    time.sleep(globalVariable.sustain_time)
    key_up(key)

def send_multiple_key_to_window_task(keys):
    """发送组合按键，减少延迟"""
    for key in keys:
        key_down(key)
    time.sleep(globalVariable.sustain_time)
    for key in keys:
        key_up(key)
def send_single_key_to_window_follow(key):
    """发送单个按键，减少延迟"""
    keyboard.press(key)
    time.sleep(0.01)
    keyboard.release(key)

def send_multiple_key_to_window_follow(keys):
    """发送组合按键，减少延迟"""
    for key in keys:
        keyboard.press(key)
    time.sleep(0.01)
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
    execute_in_thread(send_single_key_to_window_task, key)

def send_multiple_key_to_window(keys):
    """发送组合按键（新线程中执行）"""
    execute_in_thread(send_multiple_key_to_window_task, keys)

def playMusic(fileName, type):
    """优化音乐播放逻辑，只加载乐谱数据一次"""
    convert_notes_to_delayed_format(fileName, type)
    globalVariable.thread = ControlledThread()
    globalVariable.thread.start()

def resume():
    """恢复播放"""
    if globalVariable.thread:
        globalVariable.thread.resume()

def pause():
    """暂停播放"""
    if globalVariable.thread:
        globalVariable.thread.pause()

def stop():
    """停止播放"""
    if globalVariable.thread:
        globalVariable.thread.stop()

#  核心
def key_down(key: str):
    vk_code = VkKeyScanA(ord(key)) & 0xff
    scan_code = MapVirtualKeyW(vk_code, 0)
    lparam = (scan_code << 16) | 1
    win32gui.PostMessage(globalVariable._hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    PostMessageW(globalVariable._hWnd, WM_KEYDOWN, vk_code, lparam)


def key_up(key: str):
    vk_code = VkKeyScanA(ord(key)) & 0xff
    scan_code = MapVirtualKeyW(vk_code, 0)
    wparam = vk_code
    lparam = (scan_code << 16) | 0XC0000001
    PostMessageW(globalVariable._hWnd, WM_KEYUP, wparam, lparam)

