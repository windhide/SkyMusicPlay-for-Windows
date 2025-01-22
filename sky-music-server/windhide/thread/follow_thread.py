import urllib

from pynput import keyboard
from websocket_server import WebsocketServer

from windhide.playRobot.amd_robot import send_single_key_to_window_follow, send_multiple_key_to_window_follow
from windhide.static.global_variable import GlobalVariable
from windhide.utils import hook_util

hook_util.sout_null()

# WebSocket 服务端实例
server = WebsocketServer("127.0.0.1",11451)

# 键盘按键事件处理
def on_press(key):
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
                        # 向所有客户端发送按键信息
                        server.send_message_to_all(urllib.parse.quote(key.char))
        except AttributeError:
            return
        except Exception as e:
            print(f"发生错误: {e}")


# 客户端连接事件处理
def on_client_connect(client, server):
    print(f"客户端 {client['id']} 已连接")
    print(f"{server}")

# 客户端断开事件处理
def on_client_disconnect(client, server):
    GlobalVariable.follow_music = ""
    GlobalVariable.follow_sheet = []
    print(f"客户端 {client['id']} 已断开连接")
    print(f"{server}")

# 启动 WebSocket 服务
def startThread():
    try:
        # 设置 WebSocket 事件回调
        server.set_fn_new_client(on_client_connect)
        server.set_fn_client_left(on_client_disconnect)

        # 启动键盘监听
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        # 输出启动日志
        print("WebSocket 服务正在启动，监听 127.0.0.1:11451...")

        # 启动 WebSocket 服务
        server.run_forever()
    except Exception as e:
        print(f"WebSocket 服务器启动失败: {e}")

    # 确保 WebSocket 服务如果没有正常启动，可以进行进一步的调试
    print("WebSocket 服务正在运行...")
