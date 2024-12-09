import os
import threading
from fastapi import FastAPI, UploadFile
import uvicorn
# 配置文件
import logging

from utils._global import global_state
from utils.listUtils import getTypeMusicList
from utils.musicFileTranselate import convert_notes_to_delayed_format
from utils.musicToSheet.processAudio import process_directory_with_progress
from utils.pathUtils import getResourcesPath
from utils.robot import robotUtils
from utils.websocket_hook import startWebsocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源，可根据需求设置特定地址或使用 ["*"] 允许所有
    allow_credentials=True,  # 允许携带认证信息（如 Cookies）
    allow_methods=["*"],     # 允许的 HTTP 方法（如 GET、POST）
    allow_headers=["*"],     # 允许的 HTTP 请求头
)

@app.get("/")
async def get_list(listName: str):
    return  getTypeMusicList(listName)

@app.post("/start")
def start(request: dict):
    robotUtils.playMusic(request["fileName"],request["type"])
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
        # 一次读取1024字节，循环读取写入
        for chunk in iter(lambda: file.file.read(1024), b''):
            f.write(chunk)
    return "ok"

@app.post("/userMusicUpload")
async def create_upload_files(file: UploadFile):
    print(file.filename)
    # 将上传的文件保存到服务本地
    path = os.path.join(getResourcesPath("myImport"), f'{file.filename}')
    with open(path, 'wb') as f:
        # 一次读取1024字节，循环读取写入
        for chunk in iter(lambda: file.file.read(1024), b''):
            f.write(chunk)
    return "ok"

@app.post("/translate")
def translate(request: dict):
    process_directory_with_progress(use_gpu=False if request["processor"] == 'cpu' else True,modelName="note_F1=0.9677_pedal_F1=0.9186.pth")
    return "ok"

@app.post("/setConfig")
def translate(request: dict):
    if request["name"] == 'delay_interval':
        global_state.delay_interval = float(request["value"])
    if request["name"] == 'sustain_time':
        global_state.sustain_time = float(request["value"])
    if request["name"] == 'set_progress':
        global_state.set_progress = float(request["value"])
    return "ok"

@app.post("/getConfig")
def get_config(request: dict):
    returnData = eval("global_state."+request["name"])
    return returnData

@app.post("/followSheet")
def set_follow_sheet(request: dict):
    convert_notes_to_delayed_format(request["fileName"],request["type"])
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

if __name__ == '__main__':
    websocket_thread = threading.Thread(target=startWebsocket)
    websocket_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    websocket_thread.start()
    try:
        uvicorn.run(app, host="localhost", port=9899, log_level="error")
    except Exception as e:
        logging.error(e)
