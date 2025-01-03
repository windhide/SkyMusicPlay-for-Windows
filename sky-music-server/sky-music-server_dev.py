import json
import shutil
import threading
import time
import webbrowser
import psutil  # 新增，用于检查进程状态
import requests
from fastapi import FastAPI, UploadFile
import uvicorn
import os
from windhide._global import globalVariable
from windhide.utils.listUtils import getTypeMusicList
from windhide.utils.musicFileTranselate import convert_notes_to_delayed_format
from windhide.musicToSheet.processAudio import process_directory_with_progress
from windhide.utils.pathUtils import getResourcesPath
from windhide.playRobot import robotUtils
from windhide.thread.follow_hook import startThread as follow_thread
from windhide.thread.shortcut_hook import startThread as shortcut_thread
from windhide.thread.hwnd_check_hook import startThread as hwnd_check_thread
from fastapi.middleware.cors import CORSMiddleware

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
    print(f"Fetching music list: {listName}, search: {searchStr}")
    return getTypeMusicList(listName, searchStr)


@app.post("/start")
def start(request: dict):
    try:
        print(f"Starting music: {request['fileName']} of type {request['type']}")
        if globalVariable._hWnd is None:
            return {
                "statusCode": 8008208820,
                "messeage": "没检测到存活的光遇窗口"
            }
        robotUtils.playMusic(request["fileName"], request["type"])
    except Exception as e:
        print(f"Error in /start: {str(e)}")


@app.get("/pause")
def pause():
    try:
        print("Pausing music")
        robotUtils.pause()
    except Exception as e:
        print(f"Error in /pause: {str(e)}")


@app.get("/stop")
def stop():
    try:
        print("Stopping music")
        robotUtils.stop()
    except Exception as e:
        print(f"Error in /stop: {str(e)}")


@app.get("/resume")
def resume():
    try:
        print("Resuming music")
        robotUtils.resume()
    except Exception as e:
        print(f"Error in /resume: {str(e)}")


@app.get("/getProgress")
def get_progress():
    try:
        print("Fetching progress")
        return {
            "overall_progress": f"{globalVariable.overall_progress:.1f}",
            "tran_mid_progress": f"{globalVariable.tran_mid_progress:.1f}",
            "now_progress": f"{globalVariable.now_progress:.1f}",
            "now_translate_text": globalVariable.now_translate_text
        }
    except Exception as e:
        print(f"Error in /getProgress: {str(e)}")


@app.post("/fileUpload")
async def create_upload_files(file: UploadFile):
    try:
        print(f"Uploading file: {file.filename}")
        path = os.path.join(getResourcesPath("translateOriginalMusic"), f'{file.filename}')
        with open(path, 'wb') as f:
            for chunk in iter(lambda: file.file.read(1024), b''):
                f.write(chunk)
        return "ok"
    except Exception as e:
        print(f"Error in /fileUpload: {str(e)}")
        return "File upload failed"


@app.post("/userMusicUpload")
async def create_upload_files(file: UploadFile):
    try:
        print(f"Uploading user music file: {file.filename}")
        path = os.path.join(getResourcesPath("myImport"), f'{file.filename}')
        with open(path, 'wb') as f:
            for chunk in iter(lambda: file.file.read(1024), b''):
                f.write(chunk)
        return "ok"
    except Exception as e:
        print(f"Error in /userMusicUpload: {str(e)}")
        return "File upload failed"


@app.post("/translate")
def translate(request: dict):
    try:
        print(f"Starting translation with processor: {request['processor']}")
        process_directory_with_progress(
            use_gpu=False if request["processor"] == 'cpu' else True,
            modelName="note_F1=0.9677_pedal_F1=0.9186.pth"
        )
        return "ok"
    except Exception as e:
        print(f"Error in /translate: {str(e)}")
        return "Translation failed"


@app.post("/setConfig")
def set_config(request: dict):
    try:
        if request["name"] == 'delay_interval':
            globalVariable.delay_interval = float(request["value"])
        if request["name"] == 'sustain_time':
            globalVariable.sustain_time = float(request["value"])
        if request["name"] == 'set_progress':
            globalVariable.set_progress = float(request["value"])
        if request["name"] == 'play_speed':
            globalVariable.play_speed = float(request["value"])
        print(f"Config set: {request['name']} = {request['value']}")
        return "ok"
    except Exception as e:
        print(f"Error in /setConfig: {str(e)}")
        return "Config set failed"


@app.post("/getConfig")
def get_config(request: dict):
    try:
        returnData = eval("globalVariable." + request["name"])
        print(f"Config fetched: {request['name']} = {returnData}")
        return returnData
    except Exception as e:
        print(f"Error in /getConfig: {str(e)}")
        return "Failed to fetch config"


@app.post("/followSheet")
def set_follow_sheet(request: dict):
    try:
        print(f"Setting follow sheet for file: {request['fileName']}")
        convert_notes_to_delayed_format(request["fileName"], request["type"])
        globalVariable.follow_sheet = list(map(lambda item: item['key'], globalVariable.music_sheet))
        globalVariable.music_sheet = []
        globalVariable.follow_music = request["fileName"]
    except Exception as e:
        print(f"Error in /followSheet: {str(e)}")


@app.post("/nextSheet")
def next_sheet(request: dict):
    try:
        if len(globalVariable.follow_sheet) == 0:
            print("Follow sheet is empty")
            return ""
        if request["type"] == "ok":
            sheet = globalVariable.follow_sheet[0]
            globalVariable.nowClientKey = sheet
            globalVariable.follow_sheet = globalVariable.follow_sheet[1:]
            print(f"Next sheet: {sheet}")
            return sheet
        elif request["type"] == "pre":
            return globalVariable.follow_sheet[1]
        else:
            globalVariable.nowClientKey = globalVariable.follow_sheet[0]
            return globalVariable.follow_sheet[0]


    except IndexError:
        print("Empty follow sheet")
        return ""
    except Exception as e:
        print(f"Error in /nextSheet: {str(e)}")


@app.get("/check")
def check():
    return 'True'


def is_process_running(process_name):
    """检查目标进程是否运行"""
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False


def monitor_process(process_name):
    """监听目标进程的状态，如果退出则结束主程序"""
    print(f"监听进程: {process_name}")
    while is_process_running(process_name):
        time.sleep(1)  # 每秒检查一次
    print(f"{process_name} 已退出，关闭主程序。")
    os._exit(0)  # 强制退出主进程


@app.get("/openBrowser")
def open_browser(url: str):
    webbrowser.open(url)
    return 'ok'


@app.post("/getConvertSheet")
def get_convert_sheet(request: dict):
    try:
        print(f"Converting sheet for file: {request['fileName']}")
        convert_notes_to_delayed_format(request["fileName"], request["type"])
        convert_sheet = list(map(lambda item: item['key'], globalVariable.music_sheet))
        globalVariable.music_sheet = []
        return convert_sheet
    except Exception as e:
        print(f"Error in /getConvertSheet: {str(e)}")
        return []


@app.post('/setFavoriteMusic')
def set_favorite_music(request: dict):
    try:
        print(f"Setting favorite music: {request['fileName']}")
        src = os.path.join(getResourcesPath(request['type']), request['fileName'] + ".txt")
        dst = os.path.join(getResourcesPath('myFavorite'), request['fileName'] + ".txt")
        shutil.copy(src, dst, follow_symlinks=False)
        return "ok"
    except Exception as e:
        print(f"Error in /setFavoriteMusic: {str(e)}")
        return "Favorite music set failed"


@app.post('/dropFile')
def drop_file(request: dict):
    file_name = request["fileName"]
    if file_name == None:
        return '不ok'
    if request.get('suffix', None) == None:
        drop_path = os.path.join(getResourcesPath(request['type']),file_name + '.txt')
    else:
        drop_path = os.path.join(getResourcesPath(request['type']),file_name + request['suffix'])
    os.remove(drop_path)
    return 'ok'

@app.get('/openFiles')
def open_files():
    appdata_path = os.getenv('APPDATA')
    os.startfile(os.path.join(appdata_path, 'ThatGameCompany', 'com.netease.sky', 'images'))

@app.get("/update")
def get_update():
    if globalVariable.isShow is False:
        response = requests.get('https://gitee.com/WindHide/SkyMusicPlay-for-Windows/raw/main/.version')
        globalVariable.isShow = True
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f'请求失败，状态码：{response.status_code}')
        return "404"

if __name__ == '__main__':
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

    print("Now start service")
    # 启动 FastAPI 服务
    try:
        uvicorn.run("sky-music-server_dev:app", host="localhost", port=9899, log_level="error")
    except Exception as e:
        print(f"Error starting server: {str(e)}")
