import time

from pynput import keyboard

from windhide.playRobot.amd_robot import send_multiple_key_press, send_multiple_key_release
from windhide.static.global_variable import GlobalVariable
from windhide.utils import hook_util
from windhide.utils.command_util import resize_and_reload_key, clear_window_key, add_window_key, \
    quit_window

hook_util.sout_null()

GlobalVariable.exit_flag = False  # 添加全局退出标志
originalKeys = "None"
pressedKeys = set()

def on_press(key):
    global pressedKeys, originalKeys
    if GlobalVariable.exit_flag:
        return False  # 终止监听
    if GlobalVariable.follow_music != "":
        try:
            if hasattr(key, 'char') and key.char in 'yuiophjkl;nm,./-=q':
                if GlobalVariable.isNowAutoPlaying:
                    if key.char not in "-":
                        GlobalVariable.nowRobotKey += key.char
                    if len(GlobalVariable.nowRobotKey) == len(GlobalVariable.nowClientKey):
                        GlobalVariable.isNowAutoPlaying = False
                        GlobalVariable.nowRobotKey = ''
                else:
                    if key.char in "-":
                        GlobalVariable.isNowAutoPlaying = True
                        send_multiple_key_press(GlobalVariable.nowClientKey)
                    if key.char in "=":
                        send_multiple_key_press(GlobalVariable.nowClientKey)
        except Exception as e:
            print(f"发生错误: {e.__doc__} , 开始重新加载")

    # 处理 Esc 退出监听
    if key == keyboard.Key.esc:
        print("检测到 Esc 键，退出监听...")
        GlobalVariable.exit_flag = True  # 设置全局标志
        try:
            quit_window()
        except Exception as e:
            return False
        return False  # 停止监听


def key_release(key):
    global pressedKeys, originalKeys
    if GlobalVariable.exit_flag:
        return False  # 终止监听
    if GlobalVariable.follow_music != "":
        try:
            if hasattr(key, 'char') and key.char in 'yuiophjkl;nm,./-=q':
                if GlobalVariable.isNowAutoPlaying:
                    if key.char not in "-":
                        GlobalVariable.nowRobotKey += key.char
                    if len(GlobalVariable.nowRobotKey) == len(GlobalVariable.nowClientKey):
                        GlobalVariable.isNowAutoPlaying = False
                        GlobalVariable.nowRobotKey = ''
                else:
                    if key.char in "-":
                        GlobalVariable.isNowAutoPlaying = True
                        send_multiple_key_release(GlobalVariable.nowClientKey)
                    if key.char in "=":
                        send_multiple_key_release(GlobalVariable.nowClientKey)
                    if key.char in "q":
                        resize_and_reload_key()
                    else:
                        if key.char in originalKeys:
                            pressedKeys.add(key.char)
                        if len(pressedKeys) == len(originalKeys):
                            pressedKeys.clear()
                            originalKeys = set(get_next_sheet_demo("ok"))
        except Exception as e:
            print(f"发生错误: {e.__doc__} , 开始重新加载")

    # 处理 Esc 退出监听
    if key == keyboard.Key.esc:
        print("检测到 Esc 键，退出监听...")
        GlobalVariable.exit_flag = True  # 设置全局标志
        try:
            quit_window()
        except Exception as e:
            return False
        return False  # 停止监听
box_ids = []


def get_next_sheet_demo(operator):
    if len(GlobalVariable.follow_sheet) == 0:
        return ""
    try:
        if operator != "load":
            global originalKeys
            clear_window_key(originalKeys)

        if operator == "ok" or operator == "load":
            sheet = GlobalVariable.follow_sheet[0]
            GlobalVariable.nowClientKey = sheet
            GlobalVariable.follow_sheet = GlobalVariable.follow_sheet[1:]
            for key in sheet:
                add_window_key(key)
            return sheet
        else:
            GlobalVariable.nowClientKey = GlobalVariable.follow_sheet[0]
            return GlobalVariable.follow_sheet[0]
    except IndexError:
        print("空数组")
        return ""


def startThread():
    global originalKeys, pressedKeys
    time.sleep(2)
    originalKeys = set(get_next_sheet_demo("load"))
    pressedKeys = set()
    GlobalVariable.exit_flag = False  # 确保每次启动时标志位重置
    with keyboard.Listener(on_press=on_press, on_release=key_release) as listener:
        listener.join()
