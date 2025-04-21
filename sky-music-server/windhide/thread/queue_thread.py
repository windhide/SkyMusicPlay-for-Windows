import queue
import re
from os import path

import plyer

from windhide.playRobot import intel_robot, amd_robot
from windhide.static.global_variable import GlobalVariable
from windhide.utils.path_util import getResourcesPath


def music_start_tasks():
    while True:
        try:
            request = GlobalVariable.task_queue.get(block=True, timeout=0.5)  # 最多等待1秒
        except queue.Empty:
            continue
        try:
            if GlobalVariable.window["hWnd"] is None and GlobalVariable.compatibility_mode is False:
                plyer.notification.notify(
                    app_name='小星弹琴软件',
                    app_icon=path.join(getResourcesPath("systemTools"),"icon.ico"),
                    title='🔥🔥🔥🔥🔥',
                    message='未检测到游戏窗口，请打开游戏或者去句柄页面进行指定！本次播放操作释放',
                    timeout=1
                )
                GlobalVariable.now_progress = 100
                GlobalVariable.task_queue.task_done()
                continue
            GlobalVariable.now_play_music = ("" if 'sheet' in request else  re.sub(r"-#(\d+)(?=\.\w+)?", "", request["fileName"].replace(".txt", "")))
            match GlobalVariable.cpu_type:
                case "Intel":
                    intel_robot.playMusic_edit(request["sheet"]) if 'sheet' in request else intel_robot.playMusic(request["fileName"], request["type"])
                case "AMD":
                    amd_robot.playMusic_edit(request["sheet"]) if 'sheet' in request else amd_robot.playMusic(request["fileName"], request["type"])
        except Exception as e:
            print(f"Error in processing task: {str(e)}")
        GlobalVariable.task_queue.task_done()  # 标记任务完成