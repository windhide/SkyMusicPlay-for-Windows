import time

from utils._global import global_state
from utils.musicFileTranselate import convert_notes_to_delayed_format
from utils.playThread import ControlledThread
import keyboard

def send_single_key_to_window(key):
    """发送单个按键，减少延迟"""
    keyboard.press(key)
    time.sleep(global_state.sustain_time)
    keyboard.release(key)
    time.sleep(global_state.delay_interval)
    print("keyDown ->", key)

def send_multiple_key_to_window(keys):
    for key in keys:
            if key in keys:
                send_single_key_to_window(key)

def playMusic(fileName, type):
    """优化音乐播放逻辑"""
    # 加载乐谱数据一次，避免重复转换ih
    convert_notes_to_delayed_format(fileName, type)
    global_state.thread = ControlledThread()
    global_state.thread.start()

def resume():
        global_state.thread.resume()

def pause():
        global_state.thread.pause()

def stop():
        global_state.thread.stop()



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
    '0': 0x30, ')': 0x30,  # 右括号在某些键盘布局上可能是Shift+0
    '1': 0x31, '!': 0x31,
    '2': 0x32, '@': 0x32,
    '3': 0x33, '#': 0x33,
    '4': 0x34, '$': 0x34,
    '5': 0x35, '%': 0x35,
    '6': 0x36, '^': 0x36,
    '7': 0x37, '&': 0x37,
    '8': 0x38, '*': 0x38,
    '9': 0x39, '(': 0x39,  # 左括号在某些键盘布局上可能是Shift+9
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