import time
from os import path

import plyer
from pynput import keyboard

from windhide.playRobot.amd_robot import send_multiple_key_press, send_multiple_key_release
from windhide.static.global_variable import GlobalVariable
from windhide.utils import hook_util
from windhide.utils.command_util import resize_and_reload_key, clear_window_key, add_window_key, \
    quit_window, update_key
from windhide.utils.path_util import getResourcesPath

hook_util.sout_null()

GlobalVariable.exit_flag = False  # 添加全局退出标志
originalKeys = "None"
pressedKeys = set()

def get_key_string(key):
    if hasattr(key, "char") and key.char is not None:  # 处理普通字符按键
        return key.char
    elif hasattr(key, "name"):  # 处理特殊按键
        return key.name
    else:
        return str(key)  # 兜底方案，转换为字符串

def on_press(key):
    global pressedKeys, originalKeys
    if GlobalVariable.exit_flag:
        return False  # 终止监听
    if GlobalVariable.follow_music != "":
        try:
            key = get_key_string(key)
            if key in GlobalVariable.shortcutStruct["follow_key"]["string"] or key in GlobalVariable.shortcutStruct["follow_key"]["tap_key"]:
                if GlobalVariable.isNowAutoPlaying:
                    if key not in GlobalVariable.shortcutStruct["follow_key"]["repeat"]:
                        GlobalVariable.nowRobotKey += key
                    if len(GlobalVariable.nowRobotKey) == len(GlobalVariable.nowClientKey):
                        GlobalVariable.isNowAutoPlaying = False
                        GlobalVariable.nowRobotKey = ''
                else:
                    if key in GlobalVariable.shortcutStruct["follow_key"]["repeat"]:
                        GlobalVariable.isNowAutoPlaying = True
                        send_multiple_key_press(GlobalVariable.nowClientKey)
                    if key in GlobalVariable.shortcutStruct["follow_key"]["repeat_next"]:
                        send_multiple_key_press(GlobalVariable.nowClientKey)
        except Exception as e:
            print(f"发生错误: {e.__doc__} , 开始重新加载")

    # 处理 Esc 退出监听
    if key == GlobalVariable.shortcutStruct["follow_key"]["exit"] or  key == "alt_l":
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
            key = get_key_string(key)
            if key in GlobalVariable.shortcutStruct["follow_key"]["string"] or key in GlobalVariable.shortcutStruct["follow_key"]["tap_key"]:
                if GlobalVariable.isNowAutoPlaying:
                    if key not in GlobalVariable.shortcutStruct["follow_key"]["repeat"]:
                        GlobalVariable.nowRobotKey += key
                    if len(GlobalVariable.nowRobotKey) == len(GlobalVariable.nowClientKey):
                        GlobalVariable.isNowAutoPlaying = False
                        GlobalVariable.nowRobotKey = ''
                else:
                    if key in GlobalVariable.shortcutStruct["follow_key"]["repeat"]:
                        GlobalVariable.isNowAutoPlaying = True
                        send_multiple_key_release(GlobalVariable.nowClientKey)
                    if key in GlobalVariable.shortcutStruct["follow_key"]["repeat_next"]:
                        send_multiple_key_release(GlobalVariable.nowClientKey)
                    if key in GlobalVariable.shortcutStruct["follow_key"]["resize"]:
                        resize_and_reload_key()
                    else:
                        if key in originalKeys:
                            pressedKeys.add(key)
                        if len(pressedKeys) == len(originalKeys):
                            pressedKeys.clear()
                            maybe_next_key = get_next_sheet_demo("ok")
                            if not maybe_next_key:
                                return
                            else:
                                originalKeys = set(maybe_next_key)
        except Exception as e:
            print(f"发生错误: {e.__doc__} , 开始重新加载")

    # 处理 Esc 退出监听
    if key == GlobalVariable.shortcutStruct["follow_key"]["exit"] or  key == "alt_l":
        print("检测到 Esc 键，退出监听...")
        GlobalVariable.exit_flag = True  # 设置全局标志
        try:
            quit_window()
        except Exception as e:
            return False
        return False  # 停止监听

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
            if len(GlobalVariable.follow_sheet) == 0:
                GlobalVariable.exit_flag = True  # 设置全局标志
                quit_window()
                plyer.notification.notify(
                    app_name='小星弹琴软件',
                    app_icon=path.join(getResourcesPath("systemTools"), "icon.ico"),
                    title='已经结束啦',
                    message='这首歌已经弹完了哦',
                    timeout=1
                )
                send_multiple_key_press("z")
                send_multiple_key_release("z")
                return False
            for key in sheet:
                add_window_key(key)
            update_key()
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
