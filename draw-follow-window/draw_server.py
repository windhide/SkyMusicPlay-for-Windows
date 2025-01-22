import tkinter as tk
import socket
import threading
import sys
import argparse  # 用于解析命令行参数


# 绘制和删除方框的API
def draw_box_api(canvas, width, height, position_x, position_y):
    # 在 Canvas 上绘制一个指定大小和位置的方框
    return canvas.create_rectangle(
        position_x, position_y,
        position_x + width, position_y + height,
        outline="pink", width=2
    )


def delete_box_api(canvas, box_id):
    # 从 Canvas 上删除指定 ID 的方框
    canvas.delete(box_id)


# 主窗口类
class TransparentBoxWindow:
    def __init__(self, root, width, height, position_x, position_y):
        self.root = root
        self.port = 12345  # 固定端口为 12345

        # 设置 Canvas
        self.canvas = tk.Canvas(root, width=width, height=height, bg="white", highlightthickness=0)
        self.canvas.pack()

        # 添加关闭按钮
        self.add_close_button()

        # 存储用户自定义 ID 与 Tkinter 方框 ID 的映射
        self.boxes = {}

        # 启动 Socket 服务器
        threading.Thread(target=self.start_server, daemon=True).start()

    def add_close_button(self):
        # 创建关闭按钮
        close_button = tk.Button(
            self.canvas,
            text="X",
            command=self.exit_program,  # 调用退出程序的方法
            bg="pink",
            fg="white",
            relief="flat"
        )
        # 绘制按钮在窗口上
        self.canvas.create_window(
            750, 10,
            anchor="nw",
            window=close_button
        )

    def start_server(self):
        # 创建 Socket 服务器
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", self.port))  # 绑定到本地端口
        server.listen(5)  # 开始监听
        print(f"服务器已启动，监听端口：{self.port}，等待连接...")

        while True:
            client, addr = server.accept()  # 接受客户端连接
            print(f"收到连接来自 {addr}")
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def handle_client(self, client):
        # 处理客户端连接
        try:
            while True:
                data = client.recv(1024).decode("utf-8")  # 接收数据
                if not data:
                    break
                print(f"收到数据: {data}")
                self.process_command(data)  # 处理指令
        except ConnectionResetError:
            print("客户端断开连接")
        finally:
            client.close()

    def process_command(self, command):
        # 根据客户端发送的指令执行操作
        parts = command.split()
        if parts[0] == "draw":
            # 绘制方框
            box_id = parts[1]
            width = int(parts[2])
            height = int(parts[3])
            position_x = int(parts[4])
            position_y = int(parts[5])
            if box_id in self.boxes:
                print(f"方框 ID {box_id} 已存在，跳过绘制。")
            else:
                tkinter_id = draw_box_api(self.canvas, width, height, position_x, position_y)
                self.boxes[box_id] = tkinter_id
        elif parts[0] == "delete":
            # 删除方框
            box_id = parts[1]
            if box_id in self.boxes:
                tkinter_id = self.boxes[box_id]
                delete_box_api(self.canvas, tkinter_id)
                del self.boxes[box_id]
            else:
                print(f"方框 ID {box_id} 不存在，无法删除。")
        elif parts[0] == "resize":
            # 调整窗口尺寸和位置
            new_width = int(parts[1])
            new_height = int(parts[2])
            new_x = int(parts[3])
            new_y = int(parts[4])
            self.change_window_geometry(new_width, new_height, new_x, new_y)
        elif parts[0] == "exit":
            # 退出程序
            print("接收到退出指令，正在退出程序...")
            self.exit_program()

    def change_window_geometry(self, width, height, position_x, position_y):
        """更改窗口尺寸和位置，并清除所有已绘制的框"""
        print("更改窗口尺寸和位置...")
        # 清除所有已绘制的框
        for tkinter_id in self.boxes.values():
            self.canvas.delete(tkinter_id)
        self.boxes.clear()  # 清空方框的映射

        # 更新窗口几何属性
        self.root.geometry(f"{width}x{height}+{position_x}+{position_y}")
        self.canvas.config(width=width, height=height)  # 更新 Canvas 尺寸

    def exit_program(self):
        """退出程序并清理资源"""
        self.root.destroy()  # 关闭 Tkinter 窗口
        sys.exit(0)  # 强制退出程序


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Transparent Box GUI")
    parser.add_argument("--width", type=int, default=800, help="Window width")  # 窗口宽度
    parser.add_argument("--height", type=int, default=600, help="Window height")  # 窗口高度
    parser.add_argument("--x", type=int, default=100, help="Window position X")  # 窗口 X 坐标
    parser.add_argument("--y", type=int, default=100, help="Window position Y")  # 窗口 Y 坐标
    args = parser.parse_args()

    # 获取命令行参数
    width = args.width
    height = args.height
    x = args.x
    y = args.y

    # 启动程序
    root = tk.Tk()
    root.geometry(f"{width}x{height}+{x}+{y}")  # 设置初始窗口尺寸和位置
    root.overrideredirect(True)  # 去掉标题栏
    root.attributes("-transparentcolor", "white")  # 设置透明背景色
    root.attributes("-topmost", True)  # 窗口置顶

    app = TransparentBoxWindow(root, width, height, x, y)
    root.mainloop()