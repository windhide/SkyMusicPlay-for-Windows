import json
import logging
import os
import queue
import threading
import time
import webbrowser

import psutil
import requests
import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from windhide.crack.crackSheet import crack_skySheet
from windhide.playRobot import amd_robot, intel_robot
from windhide.static.global_variable import GlobalVariable
from windhide.thread.frame_alive_thread import monitor_process
from windhide.thread.hwnd_check_thread import start_thread as hwnd_check_thread
from windhide.thread.queue_thread import music_start_tasks
from windhide.thread.shortcut_thread import startThread as shortcut_thread
from windhide.utils.auto_util import auto_click_fire, shutdown
from windhide.utils.config_util import set_config, get_config, favorite_music, convert_sheet, drop_file
from windhide.utils.hwnd_utils import get_running_apps, get_running_apps_by_struct
from windhide.utils.ocr_follow_util import set_next_sheet, get_key_position, test_key_model_position, \
    open_follow
from windhide.utils.ocr_heart_utils import get_friend_model_position
from windhide.utils.path_util import getTypeMusicList, getResourcesPath, process_sheet_rename_time
from windhide.utils.play_util import start, pause, resume, stop

# 避开与光遇相同核心运行
process = psutil.Process(os.getpid())
all_cores = list(range(psutil.cpu_count()))
cores_to_use = [core for core in all_cores if core != 0]
process.cpu_affinity(cores_to_use)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源，可根据需求设置特定地址或使用 ["*"] 允许所有
    allow_credentials=True,  # 允许携带认证信息（如 Cookies）
    allow_methods=["*"],  # 允许的 HTTP 方法（如 GET、POST）
    allow_headers=["*"],  # 允许的 HTTP 请求头
)

@app.get("/")
async def get_list(listName: str, searchStr: str):
    return getTypeMusicList(listName, searchStr)

@app.post("/play_operate")
def play_operate(request: dict):
    match request["operate"]:
        case 'start':
            start(request)
        case 'pause':
            pause()
        case 'resume':
            resume()
        case 'stop':
            stop()

@app.get("/getProgress")
def get_progress():
    return {
        "overall_progress": f"{GlobalVariable.overall_progress:.1f}",
        "now_progress": f"{GlobalVariable.now_progress:.1f}",
        "now_translate_text": GlobalVariable.now_translate_text,
        "now_play_music": GlobalVariable.now_play_music,
        "now_total_time": GlobalVariable.now_total_time,
        "now_current_time": GlobalVariable.now_current_time
    }

@app.post("/fileUpload")
async def create_upload_files(file: UploadFile):
    path = os.path.join(getResourcesPath("translateOriginalMusic"), f'{file.filename}')
    with open(path, 'wb') as f:
        for chunk in iter(lambda: file.file.read(1024), b''):
            f.write(chunk)
    return "ok"

@app.post("/userMusicUpload")
async def create_upload_files(file: UploadFile):
    path = os.path.join(getResourcesPath("myImport"), f'{file.filename}')
    with open(path, 'wb') as f:
        for chunk in iter(lambda: file.file.read(1024), b''):
            f.write(chunk)
    return "ok"

@app.post("/translate")
def translate(request: dict):
    from windhide.musicToSheet.process_audio import process_directory_with_progress
    match request["operate"]:
        case 'translate':
            process_directory_with_progress(request["value"])
    return "ok"

@app.post("/config_operate")
def config_operate(request: dict):
    match request["operate"]:
        case 'set':
            set_config(request)
        case 'get':
            return get_config(request)
        case 'favorite_music':
            favorite_music(request)
        case 'convert_sheet':
            return convert_sheet(request)
        case 'drop_file':
            drop_file(request)
        case 'get_key_position':
            return get_key_position(float(request["conf"]))
        case 'cpu_type':
            return True if GlobalVariable.cpu_type == "AMD" else False
        case 'hwnd_get':
            return  get_running_apps()
        case 'hwnd_get_now':
            if GlobalVariable.window["hWnd"] is None:
                return "Nothing"
            else:
                return GlobalVariable.hwnd_title
        case 'hwnd_set':
            if request["value"] == 'reset':
                GlobalVariable.is_custom_hwnd = False
            else:
                return get_running_apps_by_struct(request["value"])
    return "ok"

@app.post("/follow")
def follow(request: dict):
    match request["operate"]:
        case 'setSheet':
            set_next_sheet(request)
        case 'openFollow':
            open_follow()

@app.get("/check")
def check():
    return 'True'

@app.get("/openBrowser")
def open_browser(url: str):
    webbrowser.open(url)
    return 'ok'

@app.post('/openFiles')
def open_files(request: dict):
    match request["operate"]:
        case 'images':
            appdata_path = os.getenv('APPDATA')
            os.startfile(os.path.join(appdata_path, 'ThatGameCompany', 'com.netease.sky', 'images'))
        case 'files':
            os.startfile(os.path.join(getResourcesPath(None), request["type"]))

@app.get("/update")
def get_update():
   response = requests.get('https://gitee.com/WindHide/SkyMusicPlay-for-Windows/raw/main/.version')
   if response.status_code == 200:
       return json.loads(response.text)
   return "404"

#  下面放识别相关的调用
@app.post("/auto")
def auto(request: dict):
    match request["operate"]:
        case 'click_fire':
            auto_click_fire()
        case 'shutdown':
            shutdown()

@app.post("/path")
def get_path(request: dict):
    return getResourcesPath(request["type"])

@app.post("/test")
def test(request: dict):
    match request["operate"]:
        case 'image':
            return get_friend_model_position(float(request["conf"]), isTest=True)
        case 'key':
            test_key_model_position(float(request["conf"]))
        case 'press':
            match GlobalVariable.cpu_type:
                case 'Intel':
                    intel_robot.key_down(request["key"])
                    time.sleep(0.01)
                    intel_robot.key_up(request["key"])
                case 'AMD':
                    amd_robot.key_down(request["key"])
                    time.sleep(0.01)
                    amd_robot.key_up(request["key"])

@app.post("/crack_skySheet")
async def crack(request: dict):
    await crack_skySheet(request["bpm"],request["interval"], request["songName"])
    return "ok"

if __name__ == '__main__':
    GlobalVariable.isProd = True
    # 创建监听 快捷键 的线程
    shortcut_websocket_thread = threading.Thread(target=shortcut_thread)
    shortcut_websocket_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    shortcut_websocket_thread.start()

    # 创建监听目标进程的线程
    target_process = "Sky_Music.exe"
    process_monitor_thread = threading.Thread(target=monitor_process, args=(target_process,))
    process_monitor_thread.daemon = True
    process_monitor_thread.start()


    # 创建监听 光遇 窗口的线程
    hwnd_thread = threading.Thread(target=hwnd_check_thread)
    hwnd_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    hwnd_thread.start()

    # 播放队列监听
    GlobalVariable.task_queue = queue.Queue()
    task_thread = threading.Thread(target=music_start_tasks, daemon=True)
    task_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    task_thread.start()

    process_sheet_rename_time()
    # 启动 FastAPI 服务
    try:
        uvicorn.run(app, host="localhost", port=9899, log_config=None)
    except Exception as e:
        logging.error(e)