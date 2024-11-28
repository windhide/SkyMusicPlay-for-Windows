import os
from typing import List
from fastapi import FastAPI, UploadFile, File
import uvicorn
# 配置文件
import logging
import utils._global
from utils.listUtils import getTypeMusicList
from utils.musicToSheet.processAudio import process_directory_with_progress
from utils.pathUtils import getResourcesPath
from utils.robot import robotUtils

app = FastAPI()


@app.get("/")
def root():
    return {
        "systemMusic": getTypeMusicList("systemMusic"),
        "myImport": getTypeMusicList("myImport"),
        "myTranslate": getTypeMusicList("myTranslate"),
        "translateOriginalMusic": getTypeMusicList("translateOriginalMusic")
        }

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
def getProgress():
    return {
        "overall_progress": f"{utils._global.global_state.overall_progress:.1f}",
        "tran_mid_progress": f"{utils._global.global_state.tran_mid_progress:.1f}",
        "now_progress": f"{utils._global.global_state.now_progress:.1f}",
        "now_translate_text": utils._global.global_state.now_translate_text
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

@app.post("/translate")
def translate(request: dict):
    process_directory_with_progress(use_gpu=False if request["processor"] == 'cpu' else True,modelName="note_F1=0.9677_pedal_F1=0.9186.pth")
    return "ok"


if __name__ == '__main__':
    logging.info("Now start service")
    try:
        # uvicorn.run("mainController:app", host="localhost", port=9899, log_level="info")
        uvicorn.run("mainController:app", host="localhost", port=9899, log_level="error")
    except Exception as e:
        logging.error(e)
