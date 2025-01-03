import urllib

from pynput import keyboard
from websocket_server import WebsocketServer

from windhide.thread import hook_utils

hook_utils.sout_null()

# WebSocket 服务端实例
server = WebsocketServer("127.0.0.1", 11452)
# 键盘按键事件处理
def on_press(key):
    try:
        # 仅处理特定的按键
        if key == keyboard.Key.f5:
            print("按键 F5 被触发")
            server.send_message_to_all(urllib.parse.quote("F5"))
        elif key == keyboard.Key.f6:
            print("按键 F6 被触发")
            server.send_message_to_all(urllib.parse.quote("F6"))
        elif key == keyboard.Key.f7:
            print("按键 F7 被触发")
            server.send_message_to_all(urllib.parse.quote("F7"))
        elif key == keyboard.Key.f8:
            print("按键 F8 被触发")
            server.send_message_to_all(urllib.parse.quote("F8"))
        elif key == keyboard.Key.f2:
            print("按键 F2 被触发")
            server.send_message_to_all(urllib.parse.quote("F2"))
    except AttributeError:
        return
    except Exception as e:
        print(f"发生错误: {e}")

# 客户端连接事件处理
def on_client_connect(client, server):
    print(f"客户端 {client['id']} 已连接")

# 客户端断开事件处理
def on_client_disconnect(client, server):
    print(f"客户端 {client['id']} 已断开连接")

# 启动 WebSocket 服务
def startThread():
    try:
        server.set_fn_new_client(on_client_connect)
        server.set_fn_client_left(on_client_disconnect)
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        print("WebSocket 服务正在启动，监听 127.0.0.1:11452...")
        server.run_forever()
    except Exception as e:
        print(f"WebSocket 服务器启动失败: {e}")