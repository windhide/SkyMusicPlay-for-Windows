import ctypes
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
    hwnd = global_variable._hWnd
    # 获取窗口物理坐标
    rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    # 获取窗口 DPI 缩放比例
    dpi = ctypes.c_uint()
    ctypes.windll.shcore.GetDpiForWindow(hwnd, ctypes.byref(dpi))
    scale_factor = dpi.value / 96.0  # DPI 标准比例为 96
    # 计算边框和标题栏的逻辑偏移
    border_x = (rect[2] - rect[0] - client_rect[2]) // 2
    border_y = (rect[3] - rect[1] - client_rect[3] - border_x)
    # 转换物理坐标为逻辑坐标，去掉边框和标题栏
    x1 = int((rect[0] + border_x) / scale_factor)
    y1 = int((rect[1] + border_y) / scale_factor)
    x2 = int((rect[2] - border_x) / scale_factor)
    y2 = int((rect[3] - border_y) / scale_factor)
    return (x1, y1, x2, y2)
