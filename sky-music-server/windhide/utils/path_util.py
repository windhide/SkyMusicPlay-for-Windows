import json
import os
import re

import chardet
import plyer

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
                result.append({"key": combined_keys, "delay": delay, "duration": note["duration"] if "duration" in note else 0})


            combined_time = current_time
            combined_keys = GlobalVariable.keyMap.get(matchKey(key), '')  # 获取按键，默认空字符串
        else:
            combined_keys += GlobalVariable.keyMap.get(matchKey(key), '')  # 如果时间相同，合并按键
    # 处理最后的累积按键
    if combined_keys:
        result.append({"key": combined_keys, "delay": 0, 'duration':song_notes[len(song_notes) - 1]['duration'] if "duration" in note else 0})  # 最后条目的延迟为0
    GlobalVariable.music_sheet = result


def convert_json_to_play(song_notes):
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
                result.append({"key": combined_keys, "delay": delay, "duration": note["duration"]})
            combined_time = current_time
            combined_keys = GlobalVariable.keyMap.get(matchKey(key), '')  # 获取按键，默认空字符串
        else:
            combined_keys += GlobalVariable.keyMap.get(matchKey(key), '')  # 如果时间相同，合并按键
    if combined_keys:
        result.append({"key": combined_keys, "delay": 0, "duration": song_notes[len(song_notes) - 1]['duration']})  # 最后条目的延迟为0
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
        if os.path.isfile(os.path.join(resources_dir, file))
           and file != ".keep"
           and not re.search(r"-#\d+(?=\.\w+)?$", file)  # 排除匹配 -#数字 的文件
    ]
    # 如果 searchStr 不为空，过滤包含 searchStr 的文件名，忽略大小写
    if searchStr and searchStr.strip():
        file_names = [file for file in file_names if searchStr.lower() in file.lower()]

    # 构建返回的音乐列表，包含文件名和总时长
    music_list = []
    for file in file_names:
        music_list.append({
            "name": re.sub(r"-#(\d+)(?=\.\w+)?", "", file.replace(".txt", "")),
            "total_duration": format_time(int(re.search(r"-#(\d+)(?=\.\w+)?", file).group(1) if re.search(r"-#(\d+)(?=\.\w+)?", file) else "0")),
            "truthName": f"{file.replace('.txt', '')}"
        })

    return music_list

def process_sheet_rename_time(isImportOrTranslate = False):
    plyer.notification.notify(
        app_name='小星弹琴软件',
        app_icon=os.path.join(getResourcesPath("systemTools"), "icon.ico"),
        title='开始同步乐谱时长操作',
        message='时间可能会比较长，耐心等待，执行过程中可能会影响正常演奏。',
        timeout=1
    )
    if isImportOrTranslate:
        resource_dirs = [
            os.path.join(getResourcesPath(None), "myImport"),
            os.path.join(getResourcesPath(None), "myTranslate"),
        ]
    else:
        resource_dirs = [
            os.path.join(getResourcesPath(None), "systemMusic"),
            os.path.join(getResourcesPath(None), "myTranslate"),
            os.path.join(getResourcesPath(None), "myImport"),
            os.path.join(getResourcesPath(None), "myFavorite")
        ]
    all_file_paths = []
    for resources_dir in resource_dirs:
        if not os.path.exists(resources_dir):
            continue
        file_paths = [
            os.path.abspath(os.path.join(resources_dir, file))
            for file in os.listdir(resources_dir)
            if os.path.isfile(os.path.join(resources_dir, file)) and file != ".keep"
        ]
        all_file_paths.extend(file_paths)

    for file_path in all_file_paths:
        if re.search(r"-#(\d+)(?=\.\w+)?", file_path):
            continue
        try:
            with open(file_path, 'r', encoding=detect_encoding(file_path)) as file:
                data = json.load(file)
            song_notes = data[0].get("songNotes", [])
            if not song_notes:
                continue
            sumTime = int(song_notes[-1]["time"]) + int(song_notes[-1].get("duration", 0))
            directory, filename = os.path.split(file_path)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}-#{sumTime}{ext}"
            new_file_path = os.path.join(directory, new_filename)
            # 重命名文件
            os.rename(file_path, new_file_path)
        except Exception as e:
            continue
    plyer.notification.notify(
        app_name='小星弹琴软件',
        app_icon=os.path.join(getResourcesPath("systemTools"), "icon.ico"),
        title='开始同步乐谱时长操作',
        message='操作完成',
        timeout=1
    )

def format_time(milliseconds):
    """
    将毫秒数格式化为时分秒格式（HH:MM:SS 或 MM:SS）
    """
    seconds = milliseconds / 1000
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    else:
        return f"{int(minutes):02}:{int(seconds):02}"

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(32000)  # 读取文件的前32KB进行编码检测
        return chardet.detect(raw_data)['encoding']  # 直接返回编码