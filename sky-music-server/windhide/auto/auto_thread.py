import time
import threading
import time

import plyer

from windhide._global import global_variable
from windhide.playRobot._robot import click_window_position, key_press, mouse_wheel_scroll
from windhide.utils.ocr_screenshot_util import resetGameFrame, get_model_position


class HeartFireThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._running = False  # 控制线程运行的标志位
        self._lock = threading.Lock()  # 保证线程安全

    def run(self):
        """线程启动后执行的主逻辑"""
        self._running = True
        resetGameFrame()
        mouse_wheel_scroll("down")
        time.sleep(2)
        key_press("g")
        time.sleep(3)
        # 先判断是不是第一页
        while self._running:
            friend_button = get_model_position(0.2)["button"]
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
            results = get_model_position(0.2)
            button = results["button"]
            send_fire = results["send_fire"]
            get_fire = results["get_fire"]
            if len(get_fire) != 0:
                for position in get_fire:
                    time.sleep(0.3)
                    click_window_position(position["x"], position["y"])
            if len(send_fire) != 0:
                for position in send_fire:
                    if not self._running:
                        break
                    time.sleep(1)
                    click_window_position(position["x"], position["y"])
                    time.sleep(3.5)
                    key_press("f")
                    time.sleep(1)
                    key_press("ESC")
                # 下一页
                key_press("c")
                time.sleep(3)
            else:
                # 如果没有，显示别是不是到第一页去了，否则直接下一页
                if len(button) < 2:
                    key_press("c")
                    time.sleep(3)
                else:
                    plyer.notification.notify(
                        title='🔥🔥🔥🔥🔥🔥🔥🔥',
                        message='点火结束🔥🔥🔥🔥🔥',
                        timeout=1
                    )
                    return "点火结束"

    def stop(self):
        """安全停止线程"""
        with self._lock:
            self._running = False
        global_variable.auto_thread = None

    def check_running(self):
        """检查线程是否正在运行，若未运行则安全退出"""
        with self._lock:
            if not self._running:
                raise StopIteration("线程已停止")
