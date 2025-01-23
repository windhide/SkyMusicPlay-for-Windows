import socket
import threading
from windhide.static.global_variable import GlobalVariable
from windhide.thread.follow_process_thread import run_follow_process
# 全局变量，存储客户端连接对象
GlobalVariable.follow_client = None



def start_process():
    # 创建并启动线程，传递参数
    thread = threading.Thread(target=run_follow_process)
    thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    thread.start()

def add_window_key(key):
    width = GlobalVariable.window['key_position'][key]['width']
    height = GlobalVariable.window['key_position'][key]['height']
    position_x = GlobalVariable.window['key_position'][key]['position_x']
    position_y = GlobalVariable.window['key_position'][key]['position_y']
    send_command(f"draw {key} {width} {height} {position_x} {position_y}")  # 绘制

def del_window_key(key):
    send_command(f"delete {key}")  # 绘制

def clear_window_key(keys):
    for key in keys:
        send_command(f"delete {key}")

def resize_and_reload_key():
    width = GlobalVariable.window["width"]
    height = GlobalVariable.window["height"]
    position_x = GlobalVariable.window["position_x"]
    position_y = GlobalVariable.window["position_y"]
    send_command(f"resize {width} {height} {position_x} {position_y}")
    clear_window_key(GlobalVariable.nowClientKey)
    for key in GlobalVariable.nowClientKey:
        add_window_key(key)

def quit_window():
    send_command("exit")  # 发送退出指令到服务器
    GlobalVariable.follow_client.close()
    GlobalVariable.follow_client = None

def send_command(command):
    global follow_client
    try:
        if not GlobalVariable.follow_client:
            GlobalVariable.follow_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            GlobalVariable.follow_client.connect(("localhost", 12345))  # 连接到服务器
        GlobalVariable.follow_client.sendall(command.encode("utf-8"))  # 发送命令
        print(f"发送命令: {command}")
    except ConnectionRefusedError:
        print("无法连接到服务器，请确保服务端已启动。")