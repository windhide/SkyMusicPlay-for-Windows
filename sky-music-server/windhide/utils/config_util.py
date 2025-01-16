import os
import shutil

import win32gui

from windhide._global import global_variable
from windhide.musicToSheet.music2html import generatorSheetHtml
from windhide.utils.music_file_transelate import convert_notes_to_delayed_format
from windhide.utils.path_util import getResourcesPath


def set_config(request: dict):
    match request["name"]:
        case 'delay_interval':
            global_variable.delay_interval = float(request["value"])
        case 'sustain_time':
            global_variable.sustain_time = float(request["value"])
        case 'set_progress':
            global_variable.set_progress = float(request["value"])
        case 'play_speed':
            global_variable.play_speed = float(request["value"])
        case 'compatibility_mode':
            global_variable.compatibility_mode = request["value"]
        case 'is_post_w':
            global_variable.is_post_w = request["value"]

def get_config(request: dict):
    configValue = eval("global_variable." + request["name"])
    return configValue

def favorite_music(request: dict):
    src = os.path.join(getResourcesPath(request['type']), request['fileName'] + ".txt")
    dst = os.path.join(getResourcesPath('myFavorite'), request['fileName'] + ".txt")
    shutil.copy(src, dst, follow_symlinks=False)


def convert_sheet(request: dict):
    convert_notes_to_delayed_format(request["fileName"], request["type"])
    generatorSheetHtml(request["fileName"], list(map(lambda item: item['key'], global_variable.music_sheet)))
    global_variable.music_sheet = []
    return "ok"


def drop_file(request: dict):
    file_name = request["fileName"]
    if file_name is None:
        return '不ok'
    if request.get('suffix', None) is None:
        drop_path = os.path.join(getResourcesPath(request['type']), file_name + '.txt')
    else:
        drop_path = os.path.join(getResourcesPath(request['type']), file_name + request['suffix'])
    os.remove(drop_path)
    return 'ok'


def get_game_position():
    rect = win32gui.GetWindowRect(global_variable._hWnd)
    # 获取窗口的客户区坐标
    client_rect = win32gui.GetClientRect(global_variable._hWnd)
    # 获取窗口边框和标题栏的偏移
    border_x = rect[2] - rect[0] - client_rect[2]
    border_y = rect[3] - rect[1] - client_rect[3]
    # 调整坐标去掉边框和标题栏偏移
    return (rect[0] + border_x // 2, rect[1] + border_y, rect[2] - border_x // 2, rect[3] - border_y)
