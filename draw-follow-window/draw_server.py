import tkinter as tk
import socket
import threading
import sys
import argparse
import os

# 针对 Windows 系统设置 DPI Awareness（适用于 Windows 8.1 及以上）
if os.name == "nt":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print("无法设置 DPI Awareness，可能影响窗口几何尺寸的准确性。")

# 绘制和删除方框的 API
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
        self.port = 12345  # 固定端口

        # 设置 Canvas
        self.canvas = tk.Canvas(root, width=width, height=height, bg="white", highlightthickness=0)
        self.canvas.pack()

        # 绘制红色边框
        self.draw_red_border(width, height)

        # 添加关闭按钮
        self.add_close_button()

        # 存储用户自定义 ID 与 Tkinter 方框 ID 的映射
        self.boxes = {}

        # 启动 Socket 服务器
        threading.Thread(target=self.start_server, daemon=True).start()

    def draw_red_border(self, width, height, border_thickness=10):
        """在 Canvas 上绘制一个红色的边框"""
        self.canvas.create_rectangle(
            border_thickness // 2, border_thickness // 2,
            width - border_thickness // 2, height - border_thickness // 2,
            outline="red", width=border_thickness
        )

    def add_close_button(self):
        # 创建关闭按钮
        close_button = tk.Button(
            self.canvas,
            text="X",
            command=self.exit_program,
            fg="black",
            bg="aqua",
            highlightthickness=0,
            relief="flat",
            borderwidth=0
        )
        # 在 Canvas 上绘制按钮
        self.canvas.create_window(
            750, 10,
            anchor="nw",
            window=close_button
        )

    def start_server(self):
        # 创建 Socket 服务器
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", self.port))
        server.listen(5)
        print(f"服务器已启动，监听端口：{self.port}，等待连接...")

        while True:
            client, addr = server.accept()
            print(f"收到连接来自 {addr}")
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def handle_client(self, client):
        try:
            buffer = ""
            while True:
                data = client.recv(1024).decode("utf-8")
                if not data:
                    break
                buffer += data
                # 按换行符分割命令
                commands = buffer.split("\n")
                # 处理完整命令
                for command in commands[:-1]:  # 最后一个可能是不完整的
                    print(f"收到命令: {command}")
                    self.process_command(command)
                # 将最后一个不完整的命令保留到下一次处理
                buffer = commands[-1]
        except ConnectionResetError:
            print("客户端断开连接")
        finally:
            client.close()

    def process_command(self, command):
        parts = command.split()
        if parts[0] == "draw":
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
            box_id = parts[1]
            if box_id in self.boxes:
                tkinter_id = self.boxes[box_id]
                delete_box_api(self.canvas, tkinter_id)
                del self.boxes[box_id]
            else:
                print(f"方框 ID {box_id} 不存在，无法删除。")
        elif parts[0] == "resize":
            new_width = int(parts[1])
            new_height = int(parts[2])
            new_x = int(parts[3])
            new_y = int(parts[4])
            self.change_window_geometry(new_width, new_height, new_x, new_y)
        elif parts[0] == "exit":
            print("接收到退出指令，正在退出程序...")
            self.exit_program()

    def change_window_geometry(self, width, height, position_x, position_y):
        print("更改窗口尺寸和位置...")
        # 清除所有已绘制的框
        for tkinter_id in self.boxes.values():
            self.canvas.delete(tkinter_id)
        self.boxes.clear()

        # 更新窗口几何属性
        self.root.geometry(f"{width}x{height}+{position_x}+{position_y}")
        self.canvas.config(width=width, height=height)

    def exit_program(self):
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Transparent Box GUI")
    parser.add_argument("--width", type=int, default=800, help="Window width")  # 窗口宽度
    parser.add_argument("--height", type=int, default=600, help="Window height")  # 窗口高度
    parser.add_argument("--x", type=int, default=100, help="Window position X")  # 窗口 X 坐标
    parser.add_argument("--y", type=int, default=100, help="Window position Y")  # 窗口 Y 坐标
    args = parser.parse_args()

    width = args.width
    height = args.height
    x = args.x
    y = args.y

    root = tk.Tk()
    # 尽管已在 Windows 下尝试设置 DPI Awareness，仍保持 scaling 为 1.0
    root.tk.call('tk', 'scaling', 1.0)
    # 先设置 geometry，再调用 update_idletasks 确保尺寸生效
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.update_idletasks()

    root.overrideredirect(True)
    root.attributes("-transparentcolor", "white")
    root.attributes("-topmost", True)

    app = TransparentBoxWindow(root, width, height, x, y)
    root.mainloop()
