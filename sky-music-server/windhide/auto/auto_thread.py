import threading
from os import path

import time

import plyer
from pynput.keyboard import Controller, Key

from windhide.static.global_variable import GlobalVariable
from windhide.utils.ocr_heart_utils import get_friend_model_position
from windhide.utils.ocr_normal_utils import resetGameFrame
from windhide.utils.path_util import getResourcesPath

if GlobalVariable.cpu_type == 'Intel':
    from windhide.playRobot.intel_robot import mouse_move_to, key_press
else:
    from windhide.playRobot.amd_robot import mouse_move_to, key_press

keyboard = Controller()
class HeartFireThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._running = False  # 控制线程运行的标志位
        self._lock = threading.Lock()  # 保证线程安全

    def run(self):
        """线程启动后执行的主逻辑"""
        self._running = True
        resetGameFrame()
        # mouse_wheel_scroll("down")
        # time.sleep(2)
        # key_press("g")
        time.sleep(2)
        # 先判断是不是第一页
        while self._running:
            friend_button = get_friend_model_position(0.5)["button"]
            if len(friend_button) >= 2:
                break
            else:
                key_press("z")
            self.check_running()
            time.sleep(3)
        key_press("c")
        time.sleep(2)
        # 来到第一页
        while True:
            if not self._running:
                break
            results = get_friend_model_position(0.5)
            button = results["button"]
            friend = results["friend"]
            if len(friend) != 0:
                for position in friend:
                    if not self._running:
                        break
                    time.sleep(1)
                    mouse_move_to(position[0], position[1])
                    key_press("space")
                    time.sleep(0.1)
                    key_press("space")
                    time.sleep(1.5)
                    key_press("f")
                    time.sleep(1)
                    key_press("ESC")
                # 下一页
                time.sleep(1.5)
                key_press("c")
                time.sleep(3)
            else:
                # 如果没有，显示别是不是到第一页去了，否则直接下一页
                if len(button) < 2:
                    key_press("c")
                    time.sleep(3)
                else:
                    plyer.notification.notify(
                        app_name='小星弹琴软件',
                        app_icon=path.join(getResourcesPath("systemTools"), "icon.ico"),
                        title='🔥🔥🔥🔥🔥🔥🔥🔥',
                        message='点火结束🔥🔥🔥🔥🔥',
                        timeout=1
                    )
                    return "点火结束"

    def stop(self):
        """安全停止线程"""
        with self._lock:
            self._running = False
        GlobalVariable.auto_thread = None

    def check_running(self):
        """检查线程是否正在运行，若未运行则安全退出"""
        with self._lock:
            if not self._running:
                raise StopIteration("线程已停止")


def press_left():
    keyboard.press(Key.left)
    time.sleep(0.1)
    keyboard.release(Key.left)
