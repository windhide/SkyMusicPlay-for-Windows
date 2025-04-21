import os
import subprocess

import psutil

from windhide.static.global_variable import GlobalVariable
from windhide.utils.ocr_normal_utils import get_game_position
from windhide.utils.path_util import getResourcesPath

GlobalVariable.draw_process = None  # 进程对象


def run_follow_process():
    try:
        x1, y1, x2, y2 = get_game_position()
        width, height = x2 - x1, y2 - y1

        GlobalVariable.draw_process = subprocess.Popen(
            [
                os.path.join(getResourcesPath("systemTools"), "drawTool", "draw_server.exe"),
                f"--width={width}",
                f"--height={height}",
                f"--x={x1}",
                f"--y={y1}",
            ],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,  # 独立进程组，便于管理
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        pass  # 直接忽略异常，避免冗余输出

def stop_follow_process():
    """彻底终止 draw_server.exe 及其所有子进程"""
    process = GlobalVariable.draw_process
    if process and process.poll() is None:
        try:
            parent = psutil.Process(process.pid)
            children = parent.children(recursive=True)

            for child in children:
                child.terminate()

            _, still_alive = psutil.wait_procs(children, timeout=5)
            for child in still_alive:
                child.kill()

            parent.terminate()
            parent.wait(5)

            GlobalVariable.draw_process = None  # 清理进程记录
        except psutil.NoSuchProcess:
            pass
        except Exception:
            pass
