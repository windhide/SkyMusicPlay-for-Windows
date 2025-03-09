import math
import threading
import time

from windhide.playRobot import intel_robot
from windhide.static.global_variable import GlobalVariable


class ControlledThread:
    def __init__(self):
        self._pause_event = threading.Event()
        self._pause_event.set()  # 初始状态为运行
        self._thread = None
        self._running = False

    def _run(self):
        if not GlobalVariable.music_sheet:
            self.stop()
            return

        local_music_sheet = GlobalVariable.music_sheet[:]
        total_length = len(local_music_sheet) - 1
        index = 0

        while self._running and index < len(local_music_sheet):
            self._pause_event.wait()  # 等待恢复

            if GlobalVariable.set_progress != -0.01:
                index = math.floor(total_length * GlobalVariable.set_progress)
                GlobalVariable.set_progress = -0.01
                continue

            sheet = local_music_sheet[index]
            keys = sheet["key"]
            delay = sheet["delay"] / GlobalVariable.play_speed
            if total_length == 0:
                GlobalVariable.now_progress = 100
            else:
                GlobalVariable.now_progress = (index / total_length) * 100
            if keys:
                (intel_robot.send_single_key_to_window if len(keys) == 1
                 else intel_robot.send_multiple_key_to_window)(keys, sheet["duration"] if "duration" in sheet else 0)

            time.sleep(delay / 1000 + GlobalVariable.delay_interval)
            index += 1

    def start(self):
        if self._running:
            return
        self._running = True
        if self._thread and self._thread.is_alive():
            self._thread.join()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def pause(self):
        self._pause_event.clear()

    def resume(self):
        self._pause_event.set()

    def stop(self):
        self._running = False
        self.resume()  # 防止死锁
        if self._thread and self._thread.is_alive():
            self._thread.join()
        self._thread = None
