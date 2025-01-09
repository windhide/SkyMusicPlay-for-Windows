import os
import shutil

from windhide._global import global_variable
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
        case 'is_simulator':
            global_variable.is_simulator = request["value"]

def get_config(request: dict):
    configValue = eval("global_variable." + request["name"])
    return configValue


def favorite_music(request: dict):
    src = os.path.join(getResourcesPath(request['type']), request['fileName'] + ".txt")
    dst = os.path.join(getResourcesPath('myFavorite'), request['fileName'] + ".txt")
    shutil.copy(src, dst, follow_symlinks=False)


def convert_sheet(request: dict):
    convert_notes_to_delayed_format(request["fileName"], request["type"])
    convert_sheet = list(map(lambda item: item['key'], global_variable.music_sheet))
    global_variable.music_sheet = []
    return convert_sheet


def drop_file(request: dict):
    file_name = request["fileName"]
    if file_name == None:
        return '不ok'
    if request.get('suffix', None) == None:
        drop_path = os.path.join(getResourcesPath(request['type']), file_name + '.txt')
    else:
        drop_path = os.path.join(getResourcesPath(request['type']), file_name + request['suffix'])
    os.remove(drop_path)
    return 'ok'
