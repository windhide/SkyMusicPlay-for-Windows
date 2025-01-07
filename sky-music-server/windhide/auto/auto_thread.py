import os
import time
import threading

from windhide._global import global_variable
from windhide.playRobot._robot import click_window_position, key_press, mouse_wheel_scroll
from windhide.utils.ocr_screenshot_util import resetGameFrame, get_window_screenshot, match_template_and_return_coordinates
from windhide.utils.path_util import getResourcesPath


class HeartFireThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._running = False  # 控制线程运行的标志位
        self._lock = threading.Lock()  # 保证线程安全

    def run(self):
        """线程启动后执行的主逻辑"""
        self._running = True
        # 0.4 heartFire_template.png
        # 0.45 fire_template.png
        # 0.8 add_friend_template.png
        resetGameFrame()
        mouse_wheel_scroll("down")
        time.sleep(2)
        key_press("g")
        time.sleep(2)
        # 先判断是不是第一页
        while self._running:
            friend_position = self.get_add_friend_position()
            if len(friend_position) != 0:
                break
            else:
                key_press("z")
            self.check_running()
            time.sleep(2)
        key_press("c")
        time.sleep(2)
        # 来到第一页
        while True:
            if not self._running:
                break
            heart_positions = self.get_heart_fire_position()
            if len(heart_positions) != 0:
                for position in heart_positions:
                    if not self._running:
                        break
                    # 点火处理
                    time.sleep(1)
                    click_window_position(position["x"], position["y"])
                    time.sleep(2)
                if self.can_fire():  # 在点击光崽靠近的时候可能会识别不到，不过在上边已经拖动滚轮了
                    key_press("f")
                    time.sleep(0.8)
                    key_press("ESC")
                # 下一页
                key_press("c")
                time.sleep(2.5)
            else:
                # 如果没有，显示别是不是到第一页去了，否则直接下一页
                if len(self.get_add_friend_position()) == 0:
                    key_press("c")
                    time.sleep(2.5)
                else:
                    return "点火结束"

    def stop(self):
        """安全停止线程"""
        with self._lock:
            self._running = False
        global_variable.auto_thread = None

    @staticmethod
    def get_heart_fire_position():
        return match_template_and_return_coordinates(
            source_image=get_window_screenshot(),
            template_image_path=os.path.join(
                os.path.join(getResourcesPath("systemTools"), "ocrTemplate"),
                "heartFire_template.png"
            ),
            match_threshold=float(0.4)
        )

    @staticmethod
    def get_add_friend_position():
        return match_template_and_return_coordinates(
            source_image=get_window_screenshot(),
            template_image_path=os.path.join(
                os.path.join(getResourcesPath("systemTools"), "ocrTemplate"),
                "add_friend_template.png"
            ),
            match_threshold=float(0.4)
        )

    @staticmethod
    def can_fire():
        return len(match_template_and_return_coordinates(
            source_image=get_window_screenshot(),
            template_image_path=os.path.join(
                os.path.join(getResourcesPath("systemTools"), "ocrTemplate"),
                "fire_template.png"
            ),
            match_threshold=float(0.45)
        )) > 0
