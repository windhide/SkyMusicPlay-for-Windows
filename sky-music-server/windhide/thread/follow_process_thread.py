import os
import subprocess

import psutil

from windhide.static.global_variable import GlobalVariable
from windhide.utils.ocr_normal_utils import get_game_position
from windhide.utils.path_util import getResourcesPath

# 全局变量存储进程对象
GlobalVariable.draw_process = None


def run_follow_process():
    """启动 draw_server.exe 并存储进程对象"""
    try:
        position = get_game_position()
        positionX, positionY = position[0], position[1]
        width, height = position[2] - position[0], position[3] - position[1]

        # 启动进程，并让它运行在新的进程组
        GlobalVariable.draw_process = subprocess.Popen(
            [
                os.path.join(getResourcesPath("systemTools"), 'drawTool', 'draw_server.exe'),
                f"--width={width}",
                f"--height={height}",
                f"--x={positionX}",
                f"--y={positionY}"
            ],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # 让 Python 能管理进程组
        )
        print(f"✅ draw_server.exe 已启动 (PID: {GlobalVariable.draw_process.pid})")

    except FileNotFoundError:
        print("❌ 指定的 .exe 文件路径不正确或文件不存在")
    except subprocess.SubprocessError as e:
        print(f"❌ 子进程启动失败: {e}")


def stop_follow_process():
    """彻底终止 draw_server.exe 及其所有子进程"""
    if GlobalVariable.draw_process and GlobalVariable.draw_process.poll() is None:
        try:
            parent = psutil.Process(GlobalVariable.draw_process.pid)  # 获取主进程对象
            children = parent.children(recursive=True)  # 获取所有子进程

            # 先终止所有子进程
            for child in children:
                print(f"🛑 终止子进程: PID={child.pid}")
                child.terminate()

            _, still_alive = psutil.wait_procs(children, timeout=5)  # 等待子进程退出
            for child in still_alive:  # 强制杀死仍存活的子进程
                print(f"⚠️ 强制杀死子进程: PID={child.pid}")
                child.kill()

            # 终止主进程
            print(f"🛑 终止主进程: PID={parent.pid}")
            parent.terminate()
            parent.wait(5)  # 等待最多 5 秒

            # 清理全局变量
            GlobalVariable.draw_process = None
            print("✅ draw_server.exe 及其所有子进程已终止")

        except psutil.NoSuchProcess:
            print("⚠️ 进程已不存在")
        except Exception as e:
            print(f"❌ 终止进程时发生错误: {e}")
    else:
        print("⚠️ draw_server.exe 未运行")
