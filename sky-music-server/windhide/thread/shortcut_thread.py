import urllib

from pynput import keyboard
from websocket_server import WebsocketServer

from windhide.static.global_variable import GlobalVariable
from windhide.utils import hook_util

hook_util.sout_null()

server = WebsocketServer("127.0.0.1", 11452)


def get_key_string(key):
    if hasattr(key, "char") and key.char is not None:  # 处理普通字符按键
        return key.char
    elif hasattr(key, "name"):  # 处理特殊按键
        return key.name
    else:
        return str(key)  # 兜底方案，转换为字符串


# 键盘按键事件处理
def on_press(key):
    key = get_key_string(key)
    if key in GlobalVariable.shortcutStruct["music_key"]["string"]:
        try:
            server.send_message_to_all(urllib.parse.quote(key))
        except Exception as e:
            print(f"发送消息时发生错误: {e}")
# 客户端事件处理
def on_client_connect(client, server):
    print(f"客户端 {client['id']} 已连接")

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
