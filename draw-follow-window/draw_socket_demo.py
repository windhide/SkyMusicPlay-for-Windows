import socket
import time


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


# 示例指令序列
send_command("draw box1 100 50 200 200\n")  # 绘制第一个方框
time.sleep(1)  # 等待 1 秒
send_command("draw box2 150 100 300 300\n")  # 绘制第二个方框
time.sleep(1)  # 等待 1 秒

# 调整窗口尺寸和位置，同时清空所有已绘制的方框
# send_command("resize 2560 1080 50 10\n")  # 更改窗口为 1000x800 大小，位置 (50, 50)
# time.sleep(2)  # 等待 2 秒

send_command("draw box2 150 100 1000 1000\n")  # 绘制第二个方框
time.sleep(1)  # 等待 1 秒
# 再次绘制新的方框
send_command("draw box3 120 80 400 100\n")  # 绘制第三个方框
time.sleep(1)  # 等待 1 秒
send_command("draw box4 200 150 500 400\n")  # 绘制第四个方框
time.sleep(2)  # 等待 2 秒

# 删除某些方框
send_command("delete box3\n")  # 删除第三个方框
time.sleep(2)  # 等待 2 秒
send_command("delete box4\n")  # 删除第四个方框
time.sleep(2)  # 等待 2 秒

# 添加退出指令
send_command("exit \n")  # 发送退出指令到服务器
print("发送退出指令，客户端结束运行。")
