import json
import os
import time
import webbrowser

import psutil
import requests
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# from windhide.musicToSheet.aigc_handler_sheet import gemini_ai, general_ai
from windhide.musicToSheet.aigc_handler_sheet import general_ai
from windhide.playRobot import amd_robot, intel_robot
from windhide.static.global_variable import GlobalVariable
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

async def get_list(listName: str, searchStr: str):
    return getTypeMusicList(listName, searchStr)

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

def get_progress():
    return {
        "overall_progress": f"{GlobalVariable.overall_progress:.1f}",
        "now_progress": f"{GlobalVariable.now_progress:.1f}",
        "now_translate_text": GlobalVariable.now_translate_text,
        "now_play_music": GlobalVariable.now_play_music,
        "now_total_time": GlobalVariable.now_total_time,
        "now_current_time": GlobalVariable.now_current_time
    }

async def create_upload_files(file: UploadFile):
    path = os.path.join(getResourcesPath("translateOriginalMusic"), f'{file.filename}')
    with open(path, 'wb') as f:
        for chunk in iter(lambda: file.file.read(1024), b''):
            f.write(chunk)
    return "ok"

async def create_upload_files_user(file: UploadFile):
    # 读取文件内容
    file_content = await file.read()
    data = json.loads(file_content)

    # 提取 songNotes 并计算时间戳
    song_notes = data[0].get("songNotes", [])
    if not song_notes:
        raise ValueError("No songNotes found in the file")

    sum_time = int(song_notes[-1]["time"]) + int(song_notes[-1].get("duration", 0))

    # 生成新的文件名
    name, ext = os.path.splitext(file.filename)
    new_filename = f"{name}-#{sum_time}{ext}"
    path = os.path.join(getResourcesPath("myImport"), new_filename)

    # 保存文件
    with open(path, 'wb') as f:
        f.write(file_content)
    return "ok"

def translate(request: dict):
    from windhide.musicToSheet.process_audio import process_directory_with_progress
    match request["operate"]:
        case 'translate':
            process_directory_with_progress(request["value"])
    process_sheet_rename_time(isImportOrTranslate=True)
    return "ok"

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

def follow(request: dict):
    match request["operate"]:
        case 'setSheet':
            set_next_sheet(request)
        case 'openFollow':
            open_follow()

def check():
    return 'True'

def open_browser(url: str):
    webbrowser.open(url)
    return 'ok'

def open_files(request: dict):
    match request["operate"]:
        case 'images':
            appdata_path = os.getenv('APPDATA')
            os.startfile(os.path.join(appdata_path, 'ThatGameCompany', 'com.netease.sky', 'images'))
        case 'files':
            os.startfile(os.path.join(getResourcesPath(None), request["type"]))

def get_update():
   response = requests.get('https://gitee.com/WindHide/SkyMusicPlay-for-Windows/raw/main/.version')
   if response.status_code == 200:
       return json.loads(response.text)
   return "404"

#  下面放识别相关的调用
def auto(request: dict):
    match request["operate"]:
        case 'click_fire':
            auto_click_fire()
        case 'shutdown':
            shutdown()

def get_path(request: dict):
    return getResourcesPath(request["type"])

def test(request: dict):
    match request["operate"]:
        case 'image':
            return get_friend_model_position(float(request["conf"]), isTest=True)
        case 'key':
            test_key_model_position(float(request["conf"]))
            return None
        case 'press':
            match GlobalVariable.cpu_type:
                case 'Intel':
                    intel_robot.key_down(request["key"])
                    time.sleep(0.01)
                    intel_robot.key_up(request["key"])
                    return None
                case 'AMD':
                    amd_robot.key_down(request["key"])
                    time.sleep(0.01)
                    amd_robot.key_up(request["key"])
                    return None
            return None
    return None


def aigc(request: dict):
    print(f"okay now is running aigc {request['ai']}")
    # if request["ai"] == "Gemini":
    #     return gemini_ai(model=request["model"],filename=request["filename"],type_=request["type"])
    # else:
    return general_ai(model=request["model"],filename=request["filename"],type_=request["type"], platform=request["ai"])

def register_routes(app: FastAPI):
    app.get("/")(get_list)
    app.get("/check")(check)
    app.get("/update")(get_update)
    app.get("/getProgress")(get_progress)
    app.get("/openBrowser")(open_browser)
    app.get("/syncSheetName")(process_sheet_rename_time)
    app.post("/play_operate")(play_operate)
    app.post("/userMusicUpload")(create_upload_files_user)
    app.post("/config_operate")(config_operate)
    app.post("/fileUpload")(create_upload_files)
    app.post("/openFiles")(open_files)
    app.post("/translate")(translate)
    app.post("/follow")(follow)
    app.post("/auto")(auto)
    app.post("/aigc")(aigc)
    app.post("/path")(get_path)
    app.post("/test")(test)
