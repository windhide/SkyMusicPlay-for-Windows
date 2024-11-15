from fastapi import FastAPI
import uvicorn
# 配置文件
import logging

from utils._global import global_state
from utils.listUtils import getTypeMusicList
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


# 文件上传
@app.post("/translate")
def translateMusic():
    return {
        "ok"
    }

# 获取当前是否有激活窗口
@app.get("/getWindowState")
def getWindowState():
    return robotUtils.is_window_exist()

@app.post("/start")
def start(request: dict):
    print(request)
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
    return f"{global_state.now_progress:.1f}"

if __name__ == '__main__':
    logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info("Now start service")

    try:
        uvicorn.run("mainController:app", host="localhost", port=9899, log_level="info")
    except Exception as e:
        logging.error(e)
