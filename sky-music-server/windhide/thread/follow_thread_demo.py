from pynput import keyboard
from windhide.playRobot.amd_robot import send_single_key_to_window_follow, send_multiple_key_to_window_follow
from windhide.static.global_variable import GlobalVariable
from windhide.utils import hook_util
from windhide.utils.ocr_follow_util import get_next_sheet_demo

hook_util.sout_null()

# 初始化
originalKeys = set(get_next_sheet_demo("不OK"))
pressedKeys = set()

# 键盘按键事件处理
def on_press(key):
    global pressedKeys
    global originalKeys

    if GlobalVariable.follow_music != "":
        print(key)
        try:
            # 仅处理特定的按键
            if key.char in 'yuiophjkl;nm,./-=':
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
                    else:
                        if key.char in originalKeys:
                            pressedKeys.add(key.char)

                        if len(pressedKeys) == len(pressedKeys):
                            originalKeys = set(get_next_sheet_demo("ok"))
                            pressedKeys.clear()

        except AttributeError:
            return
        except Exception as e:
            print(f"发生错误: {e}")


# 客户端连接事件处理
def on_client_connect(client):
    print(f"客户端 {client['id']} 已连接")

# 客户端断开事件处理
def on_client_disconnect(client):
    GlobalVariable.follow_music = ""
    GlobalVariable.follow_sheet = []
    print(f"客户端 {client['id']} 已断开连接")

# 启动 WebSocket 服务
def startThread():
     # 启动键盘监听
     listener = keyboard.Listener(on_press=on_press)
     listener.start()
