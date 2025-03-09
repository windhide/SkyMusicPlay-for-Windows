from windhide.playRobot import intel_robot, amd_robot
from windhide.static.global_variable import GlobalVariable


def music_start_tasks():
    while True:
        request = GlobalVariable.task_queue.get()  # 从队列中取出任务
        try:
            if GlobalVariable.window["hWnd"] is None and GlobalVariable.compatibility_mode is False:
                return
            GlobalVariable.now_play_music = ("" if 'sheet' in request else request["fileName"])
            match GlobalVariable.cpu_type:
                case "Intel":
                    intel_robot.playMusic_edit(request["sheet"]) if 'sheet' in request else intel_robot.playMusic(request["fileName"], request["type"])
                case "AMD":
                    amd_robot.playMusic_edit(request["sheet"]) if 'sheet' in request else amd_robot.playMusic(request["fileName"], request["type"])
        except Exception as e:
            print(f"Error in processing task: {str(e)}")
        GlobalVariable.task_queue.task_done()  # 标记任务完成