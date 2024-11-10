from fastapi import FastAPI
import uvicorn
# 配置文件
import logging

from utils import RobotUtils
from utils.listUtils import getTypeMusicList
from elevate import elevate

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
    return RobotUtils.is_window_exist()

@app.post("/start")
def start(request: dict):
    print(request)
    RobotUtils.playMusic(request["fileName"],request["type"])
@app.get("/pause")
def pause():
    RobotUtils.pause()

@app.get("/stop")
def stop():
    RobotUtils.stop()

@app.get("/resume")
def resume():
    RobotUtils.resume()

if __name__ == '__main__':
    logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info("Now start service")

    try:
        uvicorn.run("mainController:app", host="localhost", port=9899, log_level="info")
    except Exception as e:
        logging.error(e)

    elevate()