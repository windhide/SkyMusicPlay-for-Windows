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
from utils.websocket_hook import startWebsocket
from fastapi.middleware.cors import CORSMiddleware

# 创建自定义的 Handler 来处理异常输出
class ExceptionLoggingHandler(logging.StreamHandler):
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            # 如果是错误级别日志，自动加上 exc_info=True
            record.exc_info = record.exc_info or True
        super().emit(record)

# 配置日志
logger = logging.getLogger()

# 设置日志级别为 DEBUG
logger.setLevel(logging.DEBUG)

# 创建自定义的 Handler 输出到控制台
console_handler = ExceptionLoggingHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)  # 控制台显示日志的最低级别

# 创建文件日志输出
file_handler = logging.FileHandler("log.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)  # 文件日志记录 INFO 及以上级别

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 添加处理器
logger.addHandler(console_handler)
logger.addHandler(file_handler)

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
    logger.info(f"Fetching music list: {listName}, search: {searchStr}")
    return getTypeMusicList(listName, searchStr)


@app.post("/start")
def start(request: dict):
    try:
        logger.info(f"Starting music: {request['fileName']} of type {request['type']}")
        robotUtils.playMusic(request["fileName"], request["type"])
    except Exception as e:
        logger.error(f"Error in /start: {str(e)}")


@app.get("/pause")
def pause():
    try:
        logger.info("Pausing music")
        robotUtils.pause()
    except Exception as e:
        logger.error(f"Error in /pause: {str(e)}")


@app.get("/stop")
def stop():
    try:
        logger.info("Stopping music")
        robotUtils.stop()
    except Exception as e:
        logger.error(f"Error in /stop: {str(e)}")


@app.get("/resume")
def resume():
    try:
        logger.info("Resuming music")
        robotUtils.resume()
    except Exception as e:
        logger.error(f"Error in /resume: {str(e)}")


@app.get("/getProgress")
def get_progress():
    try:
        logger.info("Fetching progress")
        return {
            "overall_progress": f"{global_state.overall_progress:.1f}",
            "tran_mid_progress": f"{global_state.tran_mid_progress:.1f}",
            "now_progress": f"{global_state.now_progress:.1f}",
            "now_translate_text": global_state.now_translate_text
        }
    except Exception as e:
        logger.error(f"Error in /getProgress: {str(e)}")


@app.post("/fileUpload")
async def create_upload_files(file: UploadFile):
    try:
        logger.info(f"Uploading file: {file.filename}")
        path = os.path.join(getResourcesPath("translateOriginalMusic"), f'{file.filename}')
        with open(path, 'wb') as f:
            for chunk in iter(lambda: file.file.read(1024), b''):
                f.write(chunk)
        return "ok"
    except Exception as e:
        logger.error(f"Error in /fileUpload: {str(e)}")
        return "File upload failed"


@app.post("/userMusicUpload")
async def create_upload_files(file: UploadFile):
    try:
        logger.info(f"Uploading user music file: {file.filename}")
        path = os.path.join(getResourcesPath("myImport"), f'{file.filename}')
        with open(path, 'wb') as f:
            for chunk in iter(lambda: file.file.read(1024), b''):
                f.write(chunk)
        return "ok"
    except Exception as e:
        logger.error(f"Error in /userMusicUpload: {str(e)}")
        return "File upload failed"


@app.post("/translate")
def translate(request: dict):
    try:
        logger.info(f"Starting translation with processor: {request['processor']}")
        process_directory_with_progress(
            use_gpu=False if request["processor"] == 'cpu' else True,
            modelName="note_F1=0.9677_pedal_F1=0.9186.pth"
        )
        return "ok"
    except Exception as e:
        logger.error(f"Error in /translate: {str(e)}")
        return "Translation failed"


@app.post("/setConfig")
def set_config(request: dict):
    try:
        if request["name"] == 'delay_interval':
            global_state.delay_interval = float(request["value"])
        if request["name"] == 'sustain_time':
            global_state.sustain_time = float(request["value"])
        if request["name"] == 'set_progress':
            global_state.set_progress = float(request["value"])
        if request["name"] == 'play_speed':
            global_state.play_speed = float(request["value"])
        logger.info(f"Config set: {request['name']} = {request['value']}")
        return "ok"
    except Exception as e:
        logger.error(f"Error in /setConfig: {str(e)}")
        return "Config set failed"


@app.post("/getConfig")
def get_config(request: dict):
    try:
        returnData = eval("global_state." + request["name"])
        logger.info(f"Config fetched: {request['name']} = {returnData}")
        return returnData
    except Exception as e:
        logger.error(f"Error in /getConfig: {str(e)}")
        return "Failed to fetch config"


@app.post("/followSheet")
def set_follow_sheet(request: dict):
    try:
        logger.info(f"Setting follow sheet for file: {request['fileName']}")
        convert_notes_to_delayed_format(request["fileName"], request["type"])
        global_state.follow_sheet = list(map(lambda item: item['key'], global_state.music_sheet))
        global_state.music_sheet = []
        global_state.follow_music = request["fileName"]
    except Exception as e:
        logger.error(f"Error in /followSheet: {str(e)}")


@app.post("/nextSheet")
def next_sheet(request: dict):
    try:
        if len(global_state.follow_sheet) == 0:
            logger.warning("Follow sheet is empty")
            return ""
        if request["type"] == "ok":
            sheet = global_state.follow_sheet[0]
            global_state.follow_sheet = global_state.follow_sheet[1:]
            logger.info(f"Next sheet: {sheet}")
            return sheet
        else:
            return global_state.follow_sheet[0]
    except IndexError:
        logger.error("Empty follow sheet")
        return ""
    except Exception as e:
        logger.error(f"Error in /nextSheet: {str(e)}")


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
    logger.info(f"监听进程: {process_name}")
    while is_process_running(process_name):
        time.sleep(1)  # 每秒检查一次
    logger.info(f"{process_name} 已退出，关闭主程序。")
    os._exit(0)  # 强制退出主进程


@app.get("/openBrowser")
def open_browser(url: str):
    webbrowser.open(url)
    return 'ok'


@app.post("/getConvertSheet")
def get_convert_sheet(request: dict):
    try:
        logger.info(f"Converting sheet for file: {request['fileName']}")
        convert_notes_to_delayed_format(request["fileName"], request["type"])
        convert_sheet = list(map(lambda item: item['key'], global_state.music_sheet))
        global_state.music_sheet = []
        return convert_sheet
    except Exception as e:
        logger.error(f"Error in /getConvertSheet: {str(e)}")
        return []


@app.post('/setFavoriteMusic')
def set_favorite_music(request: dict):
    try:
        logger.info(f"Setting favorite music: {request['fileName']}")
        src = os.path.join(getResourcesPath(request['type']), request['fileName'] + ".txt")
        dst = os.path.join(getResourcesPath('myFavorite'), request['fileName'] + ".txt")
        shutil.copy(src, dst, follow_symlinks=False)
        return "ok"
    except Exception as e:
        logger.error(f"Error in /setFavoriteMusic: {str(e)}")
        return "Favorite music set failed"


@app.post('/dropFile')
def drop_file(request: dict):
    try:
        file_name = request["fileName"]
        if file_name == None:
            logger.warning("No file name provided for dropFile")
            return '不ok'
        drop_path = os.path.join(getResourcesPath(request['type']), file_name + ".txt")
        os.remove(drop_path)
        logger.info(f"File {file_name} dropped successfully")
        return 'ok'
    except Exception as e:
        logger.error(f"Error in /dropFile: {str(e)}")
        return '不ok'

@app.get('/openFiles')
def open_files():
    appdata_path = os.getenv('APPDATA')
    os.startfile(os.path.join(appdata_path, 'ThatGameCompany', 'com.netease.sky', 'images'))


if __name__ == '__main__':
    # 创建监听 WebSocket 的线程
    websocket_thread = threading.Thread(target=startWebsocket)
    websocket_thread.daemon = True  # 设置为守护线程，主线程退出时自动退出
    websocket_thread.start()

    logger.info("Now start service")
    # 启动 FastAPI 服务
    try:
        uvicorn.run("sky-music-server_dev:app", host="localhost", port=9899, log_level="debug")
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
