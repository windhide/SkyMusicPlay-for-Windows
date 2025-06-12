import os
import shutil

from windhide.musicToSheet.music2html import generatorSheetHtml
from windhide.static.global_variable import GlobalVariable
from windhide.utils.path_util import getResourcesPath, convert_notes_to_delayed_format


def set_config(request: dict):
    match request["name"]:
        case 'delay_interval':
            GlobalVariable.delay_interval = float(request["value"])
        case 'duration':
            GlobalVariable.duration = float(request["value"])
        case 'set_progress':
            GlobalVariable.set_progress = float(request["value"])
        case 'play_speed':
            GlobalVariable.play_speed = float(request["value"])
        case 'compatibility_mode':
            GlobalVariable.compatibility_mode = request["value"]
        case 'is_post_w':
            GlobalVariable.is_post_w = request["value"]
        case 'cpu_type':
            GlobalVariable.cpu_type = "AMD" if request["value"] else "Intel"
        case 'shortcutStruct':
            GlobalVariable.shortcutStruct = request["value"]
        case 'keyMap':
            GlobalVariable.keyMap = request["value"]
        case 'merge_min':
            GlobalVariable.merge_min = int(request["value"])
        case 'merge_max':
            GlobalVariable.merge_max = int(request["value"])
        case 'velocity_filter':
            GlobalVariable.velocity_filter = int(request["value"])
        case 'is_singular':
            GlobalVariable.is_singular = request["value"]
        case 'semitone_switch':
            GlobalVariable.semitone_switch = request["value"]
        case 'detail_switch':
            GlobalVariable.detail_switch = request["value"]
        case 'ai_token':
            GlobalVariable.ai_token[request["value"]["type"]] = request["value"]["token"]
        case 'translate_prompt':
            GlobalVariable.translate_prompt = request["value"]
        case 'duration_prompt':
            GlobalVariable.duration_prompt = request["value"]

def get_config(request: dict):
    configValue = eval("GlobalVariable." + request["name"])
    return configValue

def favorite_music(request: dict):
    src = os.path.join(getResourcesPath(request['type']), request['fileName'] + ".txt")
    dst = os.path.join(getResourcesPath('myFavorite'), request['fileName'] + ".txt")
    shutil.copy(src, dst, follow_symlinks=False)


def convert_sheet(request: dict):
    convert_notes_to_delayed_format(request["fileName"], request["type"])
    generatorSheetHtml(request["fileName"], list(map(lambda item: item['key'], GlobalVariable.music_sheet)))
    GlobalVariable.music_sheet = []
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