import urllib

from pynput import keyboard
from websocket_server import WebsocketServer

from windhide.utils import hook_util

hook_util.sout_null()

server = WebsocketServer("127.0.0.1", 11452)

# 按键映射
key_mappings = {
    keyboard.Key.f2: "F2",
    keyboard.Key.f5: "F5",
    keyboard.Key.f6: "F6",
    keyboard.Key.f7: "F7",
    keyboard.Key.f8: "F8"
}

# 键盘按键事件处理
def on_press(key):
    if key in key_mappings:
        key_name = key_mappings[key]
        print(f"按键 {key_name} 被触发")
        try:
            server.send_message_to_all(urllib.parse.quote(key_name))
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
