import json
import os
import chardet
from windhide._global import globalVariable
from windhide._global.globalVariable import keyMap
from windhide.utils.pathUtils import getResourcesPath

def convert_notes_to_delayed_format(fileName, type):
    # 优化了文件路径构建
    file_path = os.path.join(getResourcesPath(type), fileName + ".txt")
    with open(file_path, 'r', encoding=detect_encoding(file_path)) as file:
        data = json.load(file)
    song_notes = data[0].get("songNotes", [])
    if not song_notes:
        return []

    result = []
    combined_keys = ""  # 按键累积
    combined_time = None  # 当前时间

    for i, note in enumerate(song_notes):
        current_time = note["time"]
        key = note["key"]

        # 处理新时间点
        if current_time != combined_time:
            if combined_keys:
                next_time = song_notes[i]["time"] if i < len(song_notes) else current_time
                delay = next_time - combined_time
                result.append({"key": combined_keys, "delay": delay})

            combined_time = current_time
            combined_keys = keyMap.get(key, '')  # 获取按键，默认空字符串
        else:
            combined_keys += keyMap.get(key, '')  # 如果时间相同，合并按键
    # 处理最后的累积按键
    if combined_keys:
        result.append({"key": combined_keys, "delay": 0})  # 最后条目的延迟为0
    globalVariable.music_sheet = result


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(32000)  # 读取文件的前32KB进行编码检测
        return chardet.detect(raw_data)['encoding']  # 直接返回编码
