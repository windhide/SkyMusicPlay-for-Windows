import os.path
import subprocess

from windhide.utils.ocr_normal_utils import get_game_position
from windhide.utils.path_util import getResourcesPath


def run_follow_process():
    try:
        position = get_game_position()
        # 获取窗口左上角的逻辑坐标
        positionX = position[0]  # x1
        positionY = position[1]  # y1
        # 获取窗口宽度和高度
        width = position[2] - position[0]  # x2 - x1
        height = position[3] - position[1]  # y2 - y1
        subprocess.run([
            os.path.join(getResourcesPath("systemTools"), 'drawTool', 'draw_server.exe'),
            f"--width={width}",
            f"--height={height}",
            f"--x={positionX}",
            f"--y={positionY}"
        ])
    except FileNotFoundError:
        print("指定的.exe文件路径不正确或文件不存在")

