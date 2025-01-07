import time
import threading

from windhide._global import global_variable
from windhide.playRobot._robot import key_down, key_up, mouse_wheel_scroll


class ControlThread:
    def __init__(self, mapSelect, json):
        self.mapSelect = mapSelect
        self.json = json
        self.stop_event = threading.Event()  # 用于停止线程的事件

    def run_control(self):
        mouse_wheel_scroll("down")
        time.sleep(2)
        if self.stop_event.is_set():  # 检查是否要求停止
            return
        if self.mapSelect == 'all':  # 全图
            return
        if self.mapSelect == 'home':  # 遇境
            return
        if self.mapSelect == 'isle':  # 晨岛
            return
        if self.mapSelect == 'prairie':  # 云野
            return
        if self.mapSelect == 'forest':  # 雨林
            return
        if self.mapSelect == 'valley':  # 霞谷
            return
        if self.mapSelect == 'wasteland':  # 墓土
            return
        if self.mapSelect == 'library':  # 禁阁
            return
        if self.mapSelect == 'afk':  # 挂机用
            return
        if self.mapSelect == 'developer':  # 调试用
            # 顺序执行操作
            for operator in self.json:
                if self.stop_event.is_set():  # 检查是否要求停止
                    return
                self.type_control(operator)
        return "已经结束嘞"

    def type_control(self, operator):
        if self.stop_event.is_set():  # 检查是否要求停止
            return
        match operator["type"]:
            case "Down":
                key_down(operator["key"])
            case "Up":
                key_up(operator["key"])
        time.sleep(int(operator["delay"]) / 1000)

    def start(self):
        self.thread = threading.Thread(target=self.run_control)
        self.thread.start()

    def stop(self):
        self.stop_event.set()  # 设置停止标志
        self.thread.join()  # 等待线程结束
        global_variable.auto_thread = None
