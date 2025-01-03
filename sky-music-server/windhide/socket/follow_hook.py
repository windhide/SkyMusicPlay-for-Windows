import urllib

from pynput import keyboard
from websocket_server import WebsocketServer
from windhide._global import global_state


# 打包放行
import builtins

from windhide.playRobot.robotUtils import send_multiple_key_to_window_task

# 重定向 print 到空函数
builtins.print = lambda *args, **kwargs: None

# WebSocket 服务端实例
server = WebsocketServer("127.0.0.1",11451)

# 键盘按键事件处理
def on_press(key):
    if global_state.follow_music != "":
        try:
            # 仅处理特定的按键
            if key.char in 'yuiophjkl;nm,./-=':
                if global_state.isNowAutoPlaying:
                    if key.char not in "-":
                        global_state.nowRobotKey += key.char
                    if len(global_state.nowRobotKey) == len(global_state.nowClientKey):
                        global_state.isNowAutoPlaying = False
                        global_state.nowRobotKey = ''
                else:
                    if key.char in "-":
                        global_state.isNowAutoPlaying = True
                        send_multiple_key_to_window_task(global_state.nowClientKey)
                    if key.char in "=":
                        send_multiple_key_to_window_task(global_state.nowClientKey)
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

# 客户端断开事件处理
def on_client_disconnect(client, server):
    global_state.follow_music = ""
    global_state.follow_sheet = []
    print(f"客户端 {client['id']} 已断开连接")

# 启动 WebSocket 服务
def startWebsocket():
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
