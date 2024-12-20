import math
import threading
import time

from ._global import global_state
from .robot import robotUtils


class ControlledThread:
    def __init__(self):
        self._pause_event = threading.Event()  # 用于控制暂停的事件
        self._pause_event.set()  # 初始状态为允许运行
        self._thread = threading.Thread(target=self._run)
        self._running = True  # 控制线程的终止

    def _run(self):
            if not global_state.music_sheet:  # 使用更简洁的检查
                self.stop()
                return
            # 将全局变量缓存到本地变量以提高访问速度
            local_music_sheet = global_state.music_sheet[:]
            # 遍历 local_music_sheet，减少多次访问全局变量的开销
            allLength = len(local_music_sheet) - 1
            index = 0  # 初始下标
            while index < len(local_music_sheet):
                self._pause_event.wait()  # 如果被暂停，将阻塞在这里
                if global_state.set_progress != -0.01:
                    index = math.floor(allLength * global_state.set_progress)
                    global_state.set_progress = -0.01
                    continue  # 跳过当前迭代，重新从修改后的 index 位置开始
                if not self._running:
                    return
                sheet = local_music_sheet[index]
                keys = sheet["key"]
                delay = sheet["delay"] / global_state.play_speed
                global_state.now_progress = index / allLength * 100
                # 批量发送按键
                if len(keys) == 1:
                    robotUtils.send_single_key_to_window(keys)
                else:
                    robotUtils.send_multiple_key_to_window(keys)
                time.sleep(float(delay / 1000))
                time.sleep(global_state.delay_interval)
                index += 1

    def start(self):
        self._running = True  # 确保线程运行标志正确
        if not self._thread.is_alive():  # 避免重复启动线程
            self._thread = threading.Thread(target=self._run)
            self._thread.start()

    def pause(self):
        self._pause_event.clear()  # 阻塞线程

    def resume(self):
        self._pause_event.set()  # 解除阻塞

    def stop(self):
        self._running = False  # 终止线程
        self.resume()  # 确保线程不在暂停状态，方便退出
        if self._thread.is_alive():  # 确认线程是活跃状态
            self._thread.join()  # 等待线程结束
