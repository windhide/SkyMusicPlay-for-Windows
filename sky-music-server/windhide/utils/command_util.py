import socket
import threading
import time

from windhide.static.global_variable import GlobalVariable
from windhide.thread.follow_process_thread import run_follow_process, stop_follow_process
from windhide.utils.ocr_normal_utils import get_game_position

# 全局变量，存储客户端连接对象
GlobalVariable.follow_client = None



def start_process():
    # 创建并启动线程，传递参数
    thread = threading.Thread(target=run_follow_process)
    thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    thread.start()

def add_window_key(key):
    try:
        width = GlobalVariable.window['key_position'][key]['width']
        height = GlobalVariable.window['key_position'][key]['height']
        position_x = GlobalVariable.window['key_position'][key]['position_x'] - GlobalVariable.window_offset_x
        position_y = GlobalVariable.window['key_position'][key]['position_y'] - GlobalVariable.window_offset_y
        send_command(f"draw {key} {width} {height} {position_x} {position_y} \n")  # 绘制
    except KeyError:
        print("按键识别不完全，重新调用")
        GlobalVariable.window["is_change"] = True
        time.sleep(2)
        resize_and_reload_key()

def del_window_key(key):
    send_command(f"delete {key} \n")  # 绘制

def clear_window_key(keys):
    for key in keys:
        send_command(f"delete {key} \n")

def resize_and_reload_key():
    position = get_game_position()
    position_x, position_y = position[0], position[1]
    width, height = position[2] - position[0], position[3] - position[1]
    send_command(f"resize {width} {height} {position_x} {position_y} \n")
    clear_window_key(GlobalVariable.nowClientKey)
    for key in GlobalVariable.nowClientKey:
        add_window_key(key)

def quit_window():
    send_command(f"exit\n")
    GlobalVariable.follow_client.shutdown(socket.SHUT_RDWR)  # 关闭套接字的读写
    GlobalVariable.follow_client.close()
    GlobalVariable.follow_client = None
    stop_follow_process()

def send_command(command):
    try:
        if GlobalVariable.follow_client is None:
            GlobalVariable.follow_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            GlobalVariable.follow_client.connect(("localhost", 12345))  # 连接到服务器
        GlobalVariable.follow_client.send(command.encode("utf-8"))
        print(f"发送命令: {command}")
    except WindowsError as e:
        GlobalVariable.exit_flag = False
        print("send Command错误", e.__doc__)
    except Exception as e:
        print("send Command错误", e.__doc__)
        # GlobalVariable.follow_client.shutdown(socket.SHUT_RDWR)  # 关闭套接字的读写
        # GlobalVariable.follow_client.close()
        # GlobalVariable.follow_client = None
