from windhide._global import global_variable
from windhide.playRobot import intel_robot, amd_robot


def start(request: dict):
    try:
        print(f"Starting music: {request['fileName']} of type {request['type']}")
        if global_variable._hWnd is None and global_variable.compatibility_mode is False:
            return {
                "statusCode": 8008208820,
                "messeage": "没检测到存活的光遇窗口"
            }
        global_variable.nowPlayMusic = request["fileName"]

        match global_variable.cpu_type:
            case "Intel":
                intel_robot.playMusic(request["fileName"], request["type"])
            case "AMD":
                amd_robot.playMusic(request["fileName"], request["type"])
    except Exception as e:
        print(f"Error in /start: {str(e)}")


def pause():
    try:
        print("Pausing music")
        match global_variable.cpu_type:
            case "Intel":
                intel_robot.pause()
            case "AMD":
                amd_robot.pause()

    except Exception as e:
        print(f"Error in /pause: {str(e)}")


def stop():
    try:
        print("Stopping music")
        global_variable.nowPlayMusic = "没有正在播放的歌曲哦"
        match global_variable.cpu_type:
            case "Intel":
                intel_robot.stop()
            case "AMD":
                amd_robot.stop()
    except Exception as e:
        print(f"Error in /stop: {str(e)}")


def resume():
    try:
        print("Resuming music")
        match global_variable.cpu_type:
            case "Intel":
                intel_robot.resume()
            case "AMD":
                amd_robot.resume()
    except Exception as e:
        print(f"Error in /resume: {str(e)}")
