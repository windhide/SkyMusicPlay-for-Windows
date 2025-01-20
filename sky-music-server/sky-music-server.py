import json
import logging
import os
import threading
import time
import webbrowser

import psutil
import requests
import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from windhide._global import global_variable
from windhide.auto.script_to_json import script_to_json
from windhide.musicToSheet.process_audio import process_directory_with_progress
from windhide.playRobot import amd_robot, intel_robot
from windhide.thread.follow_thread import startThread as follow_thread
from windhide.thread.hwnd_check_thread import start_thread as hwnd_check_thread
from windhide.thread.shortcut_thread import startThread as shortcut_thread
from windhide.utils.auto_util import auto_click_fire, shutdown, auto_candles_run
from windhide.utils.config_util import set_config, get_config, favorite_music, convert_sheet, drop_file
from windhide.utils.follow_util import set_next_sheet, get_next_sheet
from windhide.utils.list_util import getTypeMusicList
from windhide.utils.ocr_screenshot_util import get_friend_model_position, test_key_model_position, get_key_position
from windhide.utils.path_util import getResourcesPath
from windhide.utils.play_util import start, pause, stop, resume

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
        "overall_progress": f"{global_variable.overall_progress:.1f}",
        "now_progress": f"{global_variable.now_progress:.1f}",
        "now_translate_text": global_variable.now_translate_text,
        "now_play_music": global_variable.nowPlayMusic
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
    match request["operate"]:
        case 'translate':
            process_directory_with_progress()
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
    return "ok"

@app.post("/follow")
def follow(request: dict):
    match request["operate"]:
        case 'setSheet':
            set_next_sheet(request)
        case 'nextSheet':
            return get_next_sheet(request)

@app.get("/check")
def check():
    return 'True'

@app.get("/openBrowser")
def open_browser(url: str):
    webbrowser.open(url)
    return 'ok'

@app.get('/openFiles')
def open_files():
    appdata_path = os.getenv('APPDATA')
    os.startfile(os.path.join(appdata_path, 'ThatGameCompany', 'com.netease.sky', 'images'))

@app.get("/update")
def get_update():
    if global_variable.isShow is False:
        response = requests.get('https://gitee.com/WindHide/SkyMusicPlay-for-Windows/raw/main/.version')
        global_variable.isShow = True
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

@app.post("/autoScriptUpload")
async def create_upload_files(file: UploadFile):
    json = await script_to_json(await file.read(),file.filename)
    await auto_candles_run("developer", json)
    return "ok"

@app.post("/test")
def test(request: dict):
    match request["operate"]:
        case 'image':
            return get_friend_model_position(float(request["conf"]), isTest=True)
        case 'key':
            test_key_model_position(float(request["conf"]))
        case 'press':
            match global_variable.cpu_type:
                case 'Intel':
                    intel_robot.key_down(request["key"])
                    time.sleep(0.01)
                    intel_robot.key_up(request["key"])
                case 'AMD':
                    amd_robot.key_down(request["key"])
                    time.sleep(0.01)
                    amd_robot.key_up(request["key"])

if __name__ == '__main__':
    global_variable.isProd = True
    # 创建监听 WebSocket 的线程
    follow_websocket_thread = threading.Thread(target=follow_thread)
    follow_websocket_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    follow_websocket_thread.start()

    # 创建监听 快捷键 的线程
    shortcut_websocket_thread = threading.Thread(target=shortcut_thread)
    shortcut_websocket_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    shortcut_websocket_thread.start()

    # 创建监听 光遇 窗口的线程
    hwnd_thread = threading.Thread(target=hwnd_check_thread)
    hwnd_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    hwnd_thread.start()

    # 启动 FastAPI 服务
    try:
        uvicorn.run(app, host="localhost", port=9899, log_level="debug")
    except Exception as e:
        logging.error(e)