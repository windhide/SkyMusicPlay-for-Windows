import socket
import threading
import time
from os import path
from time import sleep

import plyer

from windhide.static.global_variable import GlobalVariable
from windhide.thread.follow_process_thread import run_follow_process, stop_follow_process
from windhide.utils.ocr_normal_utils import get_game_position
from windhide.utils.path_util import getResourcesPath

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
    except KeyError as e:
        print("按键识别不完全，重新调用 => ", e, e.__doc__)
        GlobalVariable.window["is_change"] = True
        time.sleep(2)
        resize_and_reload_key()

def del_window_key(key):
    send_command(f"delete {key} \n")  # 绘制

def clear_window_key(keys):
    for key in keys:
        send_command(f"delete {key} \n")

def update_key():
    send_command(f"update \n")

def resize_and_reload_key():
    if GlobalVariable.window["wait"] is not True:
        GlobalVariable.window["is_change"] = True
        GlobalVariable.window["wait"] = True
    plyer.notification.notify(
        app_name='小星弹琴软件',
        app_icon=path.join(getResourcesPath("systemTools"), "icon.ico"),
        title='已经在很努力的检测了',
        message='如果长时间未检测完成请换个位置打开琴键',
        timeout=0.3
    )
    while True:
        sleep(1)
        if len(GlobalVariable.window['key_position']) == 15 and GlobalVariable.window["wait"] == False:
            GlobalVariable.window["wait"] = False
            position = get_game_position()
            position_x, position_y = position[0], position[1]
            width, height = position[2] - position[0], position[3] - position[1]
            # 检查窗口大小是否发生变化
            if width != GlobalVariable.window.get('width', 0) or height != GlobalVariable.window.get('height', 0):
                GlobalVariable.window['width'] = width
                GlobalVariable.window['height'] = height
                # 重新计算按键位置
                from windhide.utils.ocr_follow_util import get_key_position
                get_key_position(None)  # 重新获取按键位置
            send_command(f"resize {width} {height} {position_x} {position_y} \n")
            clear_window_key(GlobalVariable.nowClientKey)
            # 重新获取新的15个按键
            if len(GlobalVariable.follow_sheet) > 0:
                GlobalVariable.nowClientKey = GlobalVariable.follow_sheet[0]
                for key in GlobalVariable.nowClientKey:
                    add_window_key(key)
                update_key()
            break
    plyer.notification.notify(
        app_name='小星弹琴软件',
        app_icon=path.join(getResourcesPath("systemTools"), "icon.ico"),
        title='检测完毕',
        message='OK',
        timeout=1
    )

def quit_window():
    send_command(f"exit\n")
    GlobalVariable.follow_client.shutdown(socket.SHUT_RDWR)  # 关闭套接字的读写
    GlobalVariable.follow_client.close()
    GlobalVariable.follow_client = None
    stop_follow_process()

def wait_for_server(host, port, max_retries=30, delay=2):
    """等待服务器启动并可连接"""
    retries = 0
    while retries < max_retries:
        try:
            with socket.create_connection((host, port), timeout=1) as sock:
                return True  # 服务器已启动
        except (ConnectionRefusedError, OSError):
            retries += 1
            time.sleep(delay)
    return False  # 超时

def send_command(command):
    try:
        if GlobalVariable.follow_client is None:
            if not wait_for_server("localhost", 12345):
                print("无法连接到 draw_server.exe，超时退出。")
                return
            GlobalVariable.follow_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            GlobalVariable.follow_client.connect(("localhost", 12345))  # 连接到服务器
        GlobalVariable.follow_client.send(command.encode("utf-8"))
        print(f"发送命令: {command}")
    except WindowsError as e:
        GlobalVariable.exit_flag = True
        print("send Command错误", e.__doc__)
    except Exception as e:
        print("send Command错误", e.__doc__)
        GlobalVariable.exit_flag = True
        # GlobalVariable.follow_client.shutdown(socket.SHUT_RDWR)  # 关闭套接字的读写
        # GlobalVariable.follow_client.close()
        # GlobalVariable.follow_client = None
