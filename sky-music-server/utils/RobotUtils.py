import pyautogui
import pygetwindow as gw
import time
from utils import global_state

keyMap = {
    '1Key0':'Y', '1Key1':'U', '1Key2':'I', '1Key3':'O', '1Key4':'P',
    '1Key5':'H', '1Key6':'J', '1Key7':'K', '1Key8':'L', '1Key9':':',
    '1Key10':'N', '1Key11':'M', '1Key12':',', '1Key13':'.', '1Key14':'/'
}

def is_window_exist():
    # 获取所有活动窗体列表
    if len(gw.getWindowsWithTitle("Sky")) != 0:
        global_state.windows_name = "Sky"
    elif len(gw.getWindowsWithTitle("光·遇")) != 0:
        global_state.windows_name = "光·遇"
    elif len(gw.getWindowsWithTitle("Sky光·遇")) != 0:
        global_state.windows_name = "Sky光·遇"
    elif len(gw.getWindowsWithTitle("光遇")) != 0:
        global_state.windows_name = "光遇"
    return global_state.windows_name != ''


def is_active_ok():
    if is_window_exist():
            # 获取窗体对象并激活窗体
            global_state.target_window = gw.getWindowsWithTitle(global_state.windows_name)[0]
            global_state.global_window_activated = True
            print(f"Window '{global_state.windows_name}' activated.")
            return True
    return False


def send_single_key_to_window(window_name, key, press_duration):
        # 检查窗体是否存在
        if is_active_ok(): global_state.target_window.activate()
        else: return False
        # 发送按键
        pyautogui.keyDown(keyMap.get(key))  # 模拟按下按键
        time.sleep(press_duration)  # 持续按下指定的时间
        pyautogui.keyUp(keyMap.get(key))  # 松开按键
        print(f"Sent '{key}' to window '{window_name}'")
        return True

def send_multiple_key_to_window(window_name, keys, press_duration):
        if is_active_ok(): global_state.target_window.activate()
        else: return False

        for key in keys:
            pyautogui.keyDown(keyMap.get(key))  # 模拟按下每个键
        time.sleep(press_duration)  # 持续按下指定的时间
        pyautogui.keyUp(keyMap.get(key))  # 松开按键
        print(f"Sent '{key}' to window '{window_name}'")
        return True
