import json
import os
import re

import chardet

from windhide.static.global_variable import GlobalVariable


def matchKey(key):
    match = re.search(r'(Key-?\d+)', key)
    return match.group(1)

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
            combined_keys = GlobalVariable.keyMap.get(matchKey(key), '')  # 获取按键，默认空字符串
        else:
            combined_keys += GlobalVariable.keyMap.get(matchKey(key), '')  # 如果时间相同，合并按键
    # 处理最后的累积按键
    if combined_keys:
        result.append({"key": combined_keys, "delay": 0})  # 最后条目的延迟为0
    GlobalVariable.music_sheet = result
    
def getResourcesPath(file):
    nowPath = os.path.dirname(os.path.abspath(__file__))
    resources_path = os.path.dirname(os.path.dirname(nowPath))
    target_subpath = os.path.join("backend_dist", "sky-music-server")
    resources_path = os.path.abspath(
        os.path.join(resources_path, "..", "..", "..")) if target_subpath in resources_path else os.path.abspath(
        os.path.join(resources_path, ".."))
    if file is None:
        return os.path.join(resources_path, 'resources')
    else:
        return os.path.join(resources_path, 'resources', file)


def getTypeMusicList(type, searchStr=None):
    # 获取资源目录路径
    resources_dir = os.path.join(getResourcesPath(None), type)
    # 获取目录下所有文件名
    file_names = [
        file for file in os.listdir(resources_dir)
        if os.path.isfile(os.path.join(resources_dir, file)) and file != ".keep"
    ]    # 如果 searchStr 不为空，过滤包含 searchStr 的文件名，忽略大小写
    if searchStr and searchStr.strip():
        file_names = [file for file in file_names if searchStr.lower() in file.lower()]
    # 返回处理后的文件列表，去掉扩展名 .txt
    return [{"name": file.replace(".txt", "")} for file in file_names]

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(32000)  # 读取文件的前32KB进行编码检测
        return chardet.detect(raw_data)['encoding']  # 直接返回编码