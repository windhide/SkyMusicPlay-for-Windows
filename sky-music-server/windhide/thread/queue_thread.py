from windhide.playRobot import intel_robot, amd_robot
from windhide.static.global_variable import GlobalVariable


def process_tasks():
    while True:
        print("?")
        request = GlobalVariable.task_queue.get()  # 从队列中取出任务
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
            print(f"Error in processing task: {str(e)}")
        GlobalVariable.task_queue.task_done()  # 标记任务完成
