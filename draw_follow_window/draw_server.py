import tkinter as tk
import socket
import threading
import sys  # 用于程序退出


# 绘制和删除方框的API
def draw_box_api(canvas, width, height, position_x, position_y):
    return canvas.create_rectangle(
        position_x, position_y,
        position_x + width, position_y + height,
        outline="pink", width=2
    )


def delete_box_api(canvas, box_id):
    canvas.delete(box_id)


# 主窗口类
class TransparentBoxWindow:
    def __init__(self, root, width, height, position_x, position_y):
        self.root = root

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
        server.bind(("localhost", 12345))
        server.listen(5)
        print("服务器已启动，等待连接...")

        while True:
            client, addr = server.accept()
            print(f"收到连接来自 {addr}")
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def handle_client(self, client):
        try:
            while True:
                data = client.recv(1024).decode("utf-8")
                if not data:
                    break
                print(f"收到数据: {data}")
                self.process_command(data)
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
        elif parts[0] == "exit":
            print("接收到退出指令，正在退出程序...")
            self.exit_program()

    def exit_program(self):
        """退出程序并清理资源"""
        self.root.destroy()  # 关闭 Tkinter 窗口
        sys.exit(0)  # 强制退出程序


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600+100+100")

    # 设置窗口透明和无边框
    root.overrideredirect(True)
    root.attributes("-transparentcolor", "white")
    root.attributes("-topmost", True)  # 窗口置于最上层

    # 创建主窗口类
    app = TransparentBoxWindow(root, 800, 600, 100, 100)
    root.mainloop()
