import time
from windhide.playRobot._robot import key_down, key_up, mouse_wheel_scroll


def run_control(mapSelect, json):
    mouse_wheel_scroll("down")
    time.sleep(2)
    if mapSelect == 'all': # 全图
        return
    if mapSelect == 'home': # 遇境
        return
    if mapSelect == 'isle': # 晨岛
        return
    if mapSelect == 'prairie': # 云野
        return
    if mapSelect == 'forest': # 雨林
        return
    if mapSelect == 'valley': # 霞谷
        return
    if mapSelect == 'wasteland': # 墓土
        return
    if mapSelect == 'library': # 禁阁
        return
    if mapSelect == 'afk': # 挂机用
        return
    if mapSelect == 'developer': # 调试用
        for operator in json:
            type_control(operator)
    return "已经结束嘞"

def type_control(operator):
   match operator["type"]:
       case "Down":
           key_down(operator["key"])
       case "Up":
           key_up(operator["key"])
   time.sleep(int(operator["delay"]) / 1000)

32