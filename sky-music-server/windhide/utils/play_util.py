import chardet

from windhide.playRobot import intel_robot, amd_robot
from windhide.static.global_variable import GlobalVariable


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(32000)  # 读取文件的前32KB进行编码检测
        return chardet.detect(raw_data)['encoding']  # 直接返回编码

def start(request: dict):
    GlobalVariable.task_queue.put(request)  # 将请求放入队列

def pause():
    try:
        print("Pausing music")
        match GlobalVariable.cpu_type:
            case "Intel":
                intel_robot.pause()
            case "AMD":
                amd_robot.pause()
    except Exception as e:
        print(f"Error in /pause: {str(e)}")


def stop():
    try:
        print("Stopping music")
        GlobalVariable.now_play_music = "没有正在播放的歌曲哦"
        match GlobalVariable.cpu_type:
            case "Intel":
                intel_robot.stop()
            case "AMD":
                amd_robot.stop()
    except Exception as e:
        print(f"Error in /stop: {str(e)}")


def resume():
    try:
        print("Resuming music")
        match GlobalVariable.cpu_type:
            case "Intel":
                intel_robot.resume()
            case "AMD":
                amd_robot.resume()
    except Exception as e:
        print(f"Error in /resume: {str(e)}")
