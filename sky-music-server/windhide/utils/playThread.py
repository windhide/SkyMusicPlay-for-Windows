import math
import threading
import time
from windhide._global import globalVariable
from windhide.playRobot import robotUtils


class ControlledThread:
    def __init__(self):
        self._pause_event = threading.Event()  # 控制线程暂停
        self._pause_event.set()  # 初始状态为非阻塞（允许运行）
        self._thread = None
        self._running = False

    def _run(self):
        if not globalVariable.music_sheet:
            self.stop()
            return

        local_music_sheet = globalVariable.music_sheet[:]
        allLength = len(local_music_sheet) - 1
        index = 0
        delay_interval = globalVariable.delay_interval

        while index < len(local_music_sheet):
            if not self._running:
                break

            if not self._pause_event.wait(timeout=0.1):  # 避免线程完全阻塞
                continue

            if globalVariable.set_progress != -0.01:
                index = math.floor(allLength * globalVariable.set_progress)
                globalVariable.set_progress = -0.01
                continue

            sheet = local_music_sheet[index]
            keys = sheet["key"]
            delay = sheet["delay"] / globalVariable.play_speed
            globalVariable.now_progress = index / allLength * 100

            if len(keys) == 1:
                robotUtils.send_single_key_to_window(keys)
            else:
                robotUtils.send_multiple_key_to_window(keys)

            time.sleep(delay / 1000)
            time.sleep(delay_interval)
            index += 1

    def start(self):
        if self._running:
            return
        self._running = True
        if self._thread and self._thread.is_alive():
            self._thread.join()
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def pause(self):
        self._pause_event.clear()

    def resume(self):
        if self._running:
            self._pause_event.set()

    def stop(self):
        self._running = False  # 停止运行
        self.resume()  # 确保线程不在暂停状态
        if self._thread and self._thread.is_alive():  # 确认线程存在并正在运行
            self._thread.join()  # 等待线程完成
        self._thread = None  # 清理线程对象，方便后续重启

