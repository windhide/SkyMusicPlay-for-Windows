import chardet
from windhide.playRobot import intel_robot, amd_robot
from windhide.static.global_variable import GlobalVariable

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(32000)  # 读取文件的前32KB进行编码检测
        return chardet.detect(raw_data)['encoding']  # 直接返回编码

def start(request: dict):
    try:
        print(f"Starting music: {request['fileName']} of type {request['type']}")
        if GlobalVariable.window["hWnd"] is None and GlobalVariable.compatibility_mode is False:
            return
        GlobalVariable.now_play_music = request["fileName"]
        match GlobalVariable.cpu_type:
            case "Intel":
                intel_robot.playMusic(request["fileName"], request["type"])
            case "AMD":
                amd_robot.playMusic(request["fileName"], request["type"])
    except Exception as e:
        print(f"Error in /start: {str(e)}")


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
