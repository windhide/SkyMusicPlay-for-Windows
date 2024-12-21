import shutil
import threading
import time
import webbrowser

import psutil  # 新增，用于检查进程状态
from fastapi import FastAPI, UploadFile
import uvicorn
# 配置文件
import logging
import sys, os
from utils._global import global_state
from utils.listUtils import getTypeMusicList
from utils.musicFileTranselate import convert_notes_to_delayed_format
from utils.musicToSheet.processAudio import process_directory_with_progress
from utils.pathUtils import getResourcesPath
from utils.robot import robotUtils
from utils.websocket_hook import startWebsocket as follow_webSocket
from utils.shortcut_hook import startWebsocket as shortcut_webSocket
from fastapi.middleware.cors import CORSMiddleware

# 关闭print的输出
sys.stdout = open(os.devnull, 'w')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源，可根据需求设置特定地址或使用 ["*"] 允许所有
    allow_credentials=True,  # 允许携带认证信息（如 Cookies）
    allow_methods=["*"],     # 允许的 HTTP 方法（如 GET、POST）
    allow_headers=["*"],     # 允许的 HTTP 请求头
)

@app.get("/")
async def get_list(listName: str,searchStr: str):
    return getTypeMusicList(listName,searchStr)

@app.post("/start")
def start(request: dict):
    robotUtils.playMusic(request["fileName"], request["type"])

@app.get("/pause")
def pause():
    robotUtils.pause()

@app.get("/stop")
def stop():
    robotUtils.stop()

@app.get("/resume")
def resume():
    robotUtils.resume()

@app.get("/getProgress")
def get_progress():
    return {
        "overall_progress": f"{global_state.overall_progress:.1f}",
        "tran_mid_progress": f"{global_state.tran_mid_progress:.1f}",
        "now_progress": f"{global_state.now_progress:.1f}",
        "now_translate_text": global_state.now_translate_text
    }

@app.post("/fileUpload")
async def create_upload_files(file: UploadFile):
    print(file.filename)
    # 将上传的文件保存到服务本地
    path = os.path.join(getResourcesPath("translateOriginalMusic"), f'{file.filename}')
    with open(path, 'wb') as f:
        for chunk in iter(lambda: file.file.read(1024), b''):
            f.write(chunk)
    return "ok"

@app.post("/userMusicUpload")
async def create_upload_files(file: UploadFile):
    print(file.filename)
    # 将上传的文件保存到服务本地
    path = os.path.join(getResourcesPath("myImport"), f'{file.filename}')
    with open(path, 'wb') as f:
        for chunk in iter(lambda: file.file.read(1024), b''):
            f.write(chunk)
    return "ok"

@app.post("/translate")
def translate(request: dict):
    process_directory_with_progress(
        use_gpu=False if request["processor"] == 'cpu' else True,
        modelName="note_F1=0.9677_pedal_F1=0.9186.pth"
    )
    return "ok"

@app.post("/setConfig")
def translate(request: dict):
    if request["name"] == 'delay_interval':
        global_state.delay_interval = float(request["value"])
    if request["name"] == 'sustain_time':
        global_state.sustain_time = float(request["value"])
    if request["name"] == 'set_progress':
        global_state.set_progress = float(request["value"])
    if request["name"] == 'play_speed':
        global_state.play_speed = float(request["value"])
    return "ok"

@app.post("/getConfig")
def get_config(request: dict):
    returnData = eval("global_state." + request["name"])
    return returnData

@app.post("/followSheet")
def set_follow_sheet(request: dict):
    convert_notes_to_delayed_format(request["fileName"], request["type"])
    global_state.follow_sheet = list(map(lambda item: item['key'], global_state.music_sheet))
    global_state.music_sheet = []
    global_state.follow_music = request["fileName"]

@app.post("/nextSheet")
def next_sheet(request: dict):
    if len(global_state.follow_sheet) == 0:
        return ""
    try:
        if request["type"] == "ok":
            sheet = global_state.follow_sheet[0]
            global_state.follow_sheet = global_state.follow_sheet[1:]
            return sheet
        else:
            return global_state.follow_sheet[0]
    except IndexError:
        print("空数组")
        return ""

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
    convert_notes_to_delayed_format(request["fileName"], request["type"])
    convert_sheet = list(map(lambda item: item['key'], global_state.music_sheet))
    global_state.music_sheet = []
    return convert_sheet

@app.post('/setFavoriteMusic')
def set_favorite_music(request: dict):
        src = os.path.join(getResourcesPath(request['type']), request['fileName'] + ".txt")
        dst = os.path.join(getResourcesPath('myFavorite'), request['fileName'] + ".txt")
        shutil.copy(src, dst, follow_symlinks=False)

@app.post('/dropFile')
def drop_file(request: dict):
    file_name = request["fileName"]
    if file_name == None:
        return '不ok'
    drop_path = os.path.join(getResourcesPath(request['type']),file_name + ".txt")
    os.remove(drop_path)
    return 'ok'

@app.get('/openFiles')
def open_files():
    appdata_path = os.getenv('APPDATA')
    os.startfile(os.path.join(appdata_path, 'ThatGameCompany', 'com.netease.sky', 'images'))


if __name__ == '__main__':
    # 创建监听 WebSocket 的线程
    follow_websocket_thread = threading.Thread(target=follow_webSocket)
    follow_websocket_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    follow_websocket_thread.start()

    # 创建监听 快捷键 的线程
    shortcut_websocket_thread = threading.Thread(target=shortcut_webSocket)
    shortcut_websocket_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    shortcut_websocket_thread.start()

    # 创建监听目标进程的线程
    target_process = "Sky_Music.exe"
    process_monitor_thread = threading.Thread(target=monitor_process, args=(target_process,))
    process_monitor_thread.daemon = True
    process_monitor_thread.start()

    # 启动 FastAPI 服务
    try:
        uvicorn.run(app, host="localhost", port=9899, log_level="debug")
    except Exception as e:
        logging.error(e)
