import pyautogui
import pygetwindow as gw
import time
from utils import global_state
from utils.musicFileTranselate import convert_notes_to_delayed_format
from utils.playThread import ControlledThread
import keyboard

def is_window_exist():
    # 优化窗体检测：只在启动时检查并缓存结果
    window_titles = ["Sky", "光·遇", "Sky光·遇", "光遇"]
    for title in window_titles:
        if gw.getWindowsWithTitle(title):
            global_state.windows_name = title
            break
    return global_state.windows_name != ''

isActive = True  # 全局控制标志

def send_single_key_to_window(key, press_duration):
    """发送单个按键，减少延迟"""
    keyboard.press_and_release(key)
    print("keyDown ->", key)

def send_multiple_key_to_window(keys, press_duration):
    """批量按键发送优化"""
    print('keyDown ->', end='')
    for key in keys:
        keyboard.press(key)
        print(key, end=' ')
    print('')
    # 尽可能快速释放按键
    for key in keys:
        keyboard.release(key)

def playMusic(fileName, type):
    """优化音乐播放逻辑"""
    # 加载乐谱数据一次，避免重复转换
    convert_notes_to_delayed_format(fileName, type)
    global_state.thread = ControlledThread()
    global_state.thread.start()

def resume():
        global_state.thread.resume()

def pause():
        global_state.thread.pause()

def stop():
        global_state.thread.stop()

# 优化1：减少 `is_window_exist` 的频率调用
if is_window_exist():
    print(f"Window '{global_state.windows_name}' detected, ready to proceed.")
