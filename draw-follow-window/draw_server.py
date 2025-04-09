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
def draw_box_api(canvas, width, height, position_x, position_y, box_id=None):
    # 在 Canvas 上绘制一个指定大小和位置的方框
    if box_id is not None:
        # 重用已有的方框对象
        canvas.coords(box_id,
            position_x, position_y,
            position_x + width, position_y + height)
        return box_id
    else:
        # 创建新的方框对象
        return canvas.create_rectangle(
            position_x, position_y,
            position_x + width, position_y + height,
            outline="#00ffff", width=3
        )


def delete_box_api(canvas, box_id, box_pool=None):
    # 从 Canvas 上删除指定 ID 的方框
    if box_pool is not None and len(box_pool) < 100:
        # 将方框对象添加到对象池中
        canvas.itemconfig(box_id, state='hidden')
        box_pool.append(box_id)
    else:
        # 对象池已满或未使用对象池，直接删除
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
        # self.draw_red_border(width, height)

        # 存储用户自定义 ID 与 Tkinter 方框 ID 的映射
        self.boxes = {}
        # 对象池 - 存储可重用的方框对象
        self.box_pool = []
        self.max_pool_size = 100  # 对象池最大容量

        # 启动 Socket 服务器
        threading.Thread(target=self.start_server, daemon=True).start()

    def draw_red_border(self, width, height, border_thickness=10):
        """在 Canvas 上绘制一个红色的边框"""
        self.canvas.create_rectangle(
            border_thickness // 2, border_thickness // 2,
            width - border_thickness // 2, height - border_thickness // 2,
            outline="red", width=border_thickness, tags="red_border"
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
            command_batch = []
            while True:
                data = client.recv(1024).decode("utf-8")
                if not data:
                    break
                buffer += data
                # 按换行符分割命令
                commands = buffer.split("\n")
                # 收集完整命令到批处理列表
                for command in commands[:-1]:
                    print(f"收到命令: {command}")
                    command_batch.append(command)
                    # 当积累了足够的命令或遇到特殊命令时执行批处理
                    if len(command_batch) >= 30 or any(cmd.startswith(("resize", "exit", "update")) for cmd in command_batch):
                        self.process_command_batch(command_batch)
                        command_batch = []
                # 将最后一个不完整的命令保留到下一次处理
                buffer = commands[-1]
            # 处理剩余的命令
            if command_batch:
                self.process_command_batch(command_batch)
        except ConnectionResetError:
            print("客户端断开连接")
        finally:
            client.close()

    def process_command_batch(self, commands):
        # 创建命令分类字典
        command_groups = {
            "draw": [],
            "delete": [],
            "update": None,
            "resize": None,
            "exit": False
        }
        
        # 对命令进行分类
        for command in commands:
            parts = command.split()
            cmd_type = parts[0]
            
            if cmd_type == "draw":
                command_groups["draw"].append({
                    "id": parts[1],
                    "width": int(parts[2]),
                    "height": int(parts[3]),
                    "x": int(parts[4]),
                    "y": int(parts[5])
                })
            elif cmd_type == "delete":
                command_groups["delete"].append(parts[1])
            elif cmd_type == "update":
                # 将update命令作为触发批处理的信号
                command_groups["update"] = True
            elif cmd_type == "resize":
                command_groups["resize"] = {
                    "width": int(parts[1]),
                    "height": int(parts[2]),
                    "x": int(parts[3]),
                    "y": int(parts[4])
                }
            elif cmd_type == "exit":
                command_groups["exit"] = True
        
        # 批量处理删除命令
        for box_id in command_groups["delete"]:
            if box_id in self.boxes:
                tkinter_id = self.boxes[box_id]
                delete_box_api(self.canvas, tkinter_id, self.box_pool)
                del self.boxes[box_id]
        
        # 批量处理绘制命令
        for box in command_groups["draw"]:
            if box["id"] not in self.boxes:
                # 尝试从对象池中获取方框对象
                reused_box_id = None
                if self.box_pool:
                    reused_box_id = self.box_pool.pop()
                    self.canvas.itemconfig(reused_box_id, state='normal')
                
                tkinter_id = draw_box_api(
                    self.canvas,
                    box["width"],
                    box["height"],
                    box["x"],
                    box["y"],
                    reused_box_id
                )
                self.boxes[box["id"]] = tkinter_id
        
        # 处理调整窗口大小命令
        if command_groups["resize"]:
            resize = command_groups["resize"]
            self.change_window_geometry(
                resize["width"],
                resize["height"],
                resize["x"],
                resize["y"]
            )
        
        # 处理退出命令
        if command_groups["exit"]:
            print("接收到退出指令，正在退出程序...")
            self.exit_program()
        
        # 更新Canvas
        self.root.update_idletasks()

    def change_window_geometry(self, width, height, position_x, position_y):
        print(f"更改窗口尺寸和位置为：{width}x{height}, 坐标: ({position_x}, {position_y})")

        # 隐藏所有方框而不是删除它们
        for tkinter_id in self.boxes.values():
            self.canvas.itemconfig(tkinter_id, state='hidden')
            if len(self.box_pool) < self.max_pool_size:
                self.box_pool.append(tkinter_id)
        self.boxes.clear()

        # 修改窗口和Canvas大小
        self.root.geometry(f"{width}x{height}+{position_x}+{position_y}")
        self.canvas.config(width=width, height=height)

        # 一次性更新UI
        self.root.update_idletasks()

        # 输出调整后的实际窗口大小
        actual_width = self.root.winfo_width()
        actual_height = self.root.winfo_height()
        print(f"调整后实际窗口尺寸: {actual_width}x{actual_height}")

        # 输出调整后的实际窗口大小
        actual_width = self.root.winfo_width()
        actual_height = self.root.winfo_height()
        print(f"调整后实际窗口尺寸: {actual_width}x{actual_height}")

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
