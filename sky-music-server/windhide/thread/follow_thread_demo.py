from pynput import keyboard

from windhide.playRobot.amd_robot import send_single_key_to_window_follow, send_multiple_key_to_window_follow
from windhide.static.global_variable import GlobalVariable
from windhide.thread.follow_process_thread import stop_follow_process
from windhide.utils import hook_util
from windhide.utils.command_util import send_command, resize_and_reload_key

hook_util.sout_null()

GlobalVariable.exit_flag = False  # 添加全局退出标志


def on_press(key):
    global pressedKeys, originalKeys

    if GlobalVariable.exit_flag:
        return False  # 终止监听

    if GlobalVariable.follow_music != "":
        print(f"按键来自代码 -> {key}")
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
                        send_single_key_to_window_follow(GlobalVariable.nowClientKey)
                    if key.char in "=":
                        send_multiple_key_to_window_follow(GlobalVariable.nowClientKey)
                    if key.char in "q":
                        resize_and_reload_key()
                    else:
                        if key.char in originalKeys:
                            pressedKeys.add(key.char)
                        if len(pressedKeys) == len(originalKeys):
                            originalKeys = set(get_next_sheet_demo("ok"))
                            pressedKeys.clear()

        except AttributeError:
            return
        except Exception as e:
            print(f"发生错误: {e}")

    # 处理 Esc 退出监听
    if key == keyboard.Key.esc:
        print("检测到 Esc 键，退出监听...")
        GlobalVariable.exit_flag = True  # 设置全局标志
        stop_follow_process()
        return False  # 停止监听


box_ids = []


def get_next_sheet_demo(operator):
    if len(GlobalVariable.follow_sheet) == 0:
        return ""
    try:
        if operator == "ok":
            sheet = GlobalVariable.follow_sheet[0]
            GlobalVariable.nowClientKey = sheet
            GlobalVariable.follow_sheet = GlobalVariable.follow_sheet[1:]
            for key in sheet.keys():
                send_command("draw box1 100 50 200 200")  # 绘制
            return sheet
        else:
            GlobalVariable.nowClientKey = GlobalVariable.follow_sheet[0]
            return GlobalVariable.follow_sheet[0]
    except IndexError:
        print("空数组")
        return ""


# 初始化
originalKeys = set(get_next_sheet_demo("不OK"))
pressedKeys = set()


def startThread():
    GlobalVariable.exit_flag = False  # 确保每次启动时标志位重置
    # 用 with 语句确保退出后线程释放
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
