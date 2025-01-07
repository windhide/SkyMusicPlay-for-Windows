from windhide._global import global_variable
from windhide.playRobot import _robot


def start(request: dict):
    try:
        print(f"Starting music: {request['fileName']} of type {request['type']}")
        if global_variable._hWnd is None:
            return {
                "statusCode": 8008208820,
                "messeage": "没检测到存活的光遇窗口"
            }
        global_variable.nowPlayMusic = request["fileName"]
        _robot.playMusic(request["fileName"], request["type"])
    except Exception as e:
        print(f"Error in /start: {str(e)}")


def pause():
    try:
        print("Pausing music")
        _robot.pause()
    except Exception as e:
        print(f"Error in /pause: {str(e)}")


def stop():
    try:
        print("Stopping music")
        _robot.stop()
        global_variable.nowPlayMusic = "没有正在播放的歌曲哦"
    except Exception as e:
        print(f"Error in /stop: {str(e)}")


def resume():
    try:
        print("Resuming music")
        _robot.resume()
    except Exception as e:
        print(f"Error in /resume: {str(e)}")
