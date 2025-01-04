import threading
import time
from windhide._global import globalVariable
from windhide.utils.musicFileTranselate import convert_notes_to_delayed_format
from windhide.utils.playThread import ControlledThread
from pynput.keyboard import Controller

keyboard = Controller()

def send_single_key_to_window_task(key):
    """发送单个按键，减少延迟"""
    keyboard.press(key)
    time.sleep(globalVariable.sustain_time)
    keyboard.release(key)

def send_multiple_key_to_window_task(keys):
    """发送组合按键，减少延迟"""
    for key in keys:
        keyboard.press(key)
    time.sleep(globalVariable.sustain_time)
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
# 键盘映射
KEYS_MAP = {
    'A': 0x41, 'a': 0x41,
    'B': 0x42, 'b': 0x42,
    'C': 0x43, 'c': 0x43,
    'D': 0x44, 'd': 0x44,
    'E': 0x45, 'e': 0x45,
    'F': 0x46, 'f': 0x46,
    'G': 0x47, 'g': 0x47,
    'H': 0x48, 'h': 0x48,
    'I': 0x49, 'i': 0x49,
    'J': 0x4A, 'j': 0x4A,
    'K': 0x4B, 'k': 0x4B,
    'L': 0x4C, 'l': 0x4C,
    'M': 0x4D, 'm': 0x4D,
    'N': 0x4E, 'n': 0x4E,
    'O': 0x4F, 'o': 0x4F,
    'P': 0x50, 'p': 0x50,
    'Q': 0x51, 'q': 0x51,
    'R': 0x52, 'r': 0x52,
    'S': 0x53, 's': 0x53,
    'T': 0x54, 't': 0x54,
    'U': 0x55, 'u': 0x55,
    'V': 0x56, 'v': 0x56,
    'W': 0x57, 'w': 0x57,
    'X': 0x58, 'x': 0x58,
    'Y': 0x59, 'y': 0x59,
    'Z': 0x5A, 'z': 0x5A,
    '0': 0x30, ')': 0x30,
    '1': 0x31, '!': 0x31,
    '2': 0x32, '@': 0x32,
    '3': 0x33, '#': 0x33,
    '4': 0x34, '$': 0x34,
    '5': 0x35, '%': 0x35,
    '6': 0x36, '^': 0x36,
    '7': 0x37, '&': 0x37,
    '8': 0x38, '*': 0x38,
    '9': 0x39, '(': 0x39,
    '-': 0x2D, '_': 0x2D,
    '=': 0x3D, '+': 0x3D,
    '[': 0x5B, '{': 0x5B,
    ']': 0x5D, '}': 0x5D,
    '\\': 0x5C, '|': 0x5C,
    ';': 0x3B, ':': 0x3B,
    "'": 0x27, '"': 0x27,
    ',': 0x2C, '<': 0x2C,
    '.': 0x2E, '>': 0x2E,
    '/': 0x2F, '?': 0x2F
}
