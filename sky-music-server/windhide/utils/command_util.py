import socket

from windhide.static.global_variable import GlobalVariable


def add_window_key(x, y, positionX, positionY):
    id = "asd"
    send_command(f"draw {id} {x} {y} {positionX} {positionY}")  # 绘制

def del_window_key(key):
    haveKeys = "asd"
    send_command(f"delete {haveKeys[key]}")  # 删除第二个方框

def clear_window_key():
    haveKeys = "asd"
    for key in haveKeys:
        send_command(f"delete {key}")

def reset_window_size_position(width, height, positionX, positionY):
    send_command(f"resize {width} {height} {positionX} {positionY}")

def reset_and_reload_key(width, height, positionX, positionY):
    reset_window_size_position(width, height, positionX, positionY)
    clear_window_key()
    for key in GlobalVariable.music_sheet:
        print("?")



def quit_window():
    send_command("exit")  # 发送退出指令到服务器

def send_command(command):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 12345))  # 连接到服务器
        client.sendall(command.encode("utf-8"))  # 发送命令
        print(f"发送命令: {command}")
    except ConnectionRefusedError:
        print("无法连接到服务器，请确保服务端已启动。")
    finally:
        client.close()