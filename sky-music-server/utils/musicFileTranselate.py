import json
import os
import chardet
from utils import global_state
from utils.pathUtils import getResourcesPath

keyMap = {
    '1Key0':'y', '1Key1':'u', '1Key2':'i', '1Key3':'o', '1Key4':'p',
    '1Key5':'h', '1Key6':'j', '1Key7':'k', '1Key8':'l', '1Key9': ';',
    '1Key10':'n', '1Key11':'m', '1Key12':',', '1Key13':'.', '1Key14':'/',

    '2Key0': 'y', '2Key1': 'u', '2Key2': 'i', '2Key3': 'o', '2Key4': 'p',
    '2Key5': 'h', '2Key6': 'j', '2Key7': 'k', '2Key8': 'l', '2Key9': ';',
    '2Key10': 'n', '2Key11': 'm', '2Key12': ',', '2Key13': '.', '2Key14': '/',

    '3Key0': 'y', '3Key1': 'u', '3Key2': 'i', '3Key3': 'o', '3Key4': 'p',
    '3Key5': 'h', '3Key6': 'j', '3Key7': 'k', '3Key8': 'l', '3Key9': ';',
    '3Key10': 'n', '3Key11': 'm', '3Key12': ',', '3Key13': '.', '3Key14': '/',

    '4Key0': 'y', '4Key1': 'u', '4Key2': 'i', '4Key3': 'o', '4Key4': 'p',
    '4Key5': 'h', '4Key6': 'j', '4Key7': 'k', '4Key8': 'l', '4Key9': ';',
    '4Key10': 'n', '4Key11': 'm', '4Key12': ',', '4Key13': '.', '4Key14': '/',

    '5Key0': 'y', '5Key1': 'u', '5Key2': 'i', '5Key3': 'o', '5Key4': 'p',
    '5Key5': 'h', '5Key6': 'j', '5Key7': 'k', '5Key8': 'l', '5Key9': ';',
    '5Key10': 'n', '5Key11': 'm', '5Key12': ',', '5Key13': '.', '5Key14': '/',

    '6Key0': 'y', '6Key1': 'u', '6Key2': 'i', '6Key3': 'o', '6Key4': 'p',
    '6Key5': 'h', '6Key6': 'j', '6Key7': 'k', '6Key8': 'l', '6Key9': ';',
    '6Key10': 'n', '6Key11': 'm', '6Key12': ',', '6Key13': '.', '6Key14': '/',

    '7Key0': 'y', '7Key1': 'u', '7Key2': 'i', '7Key3': 'o', '7Key4': 'p',
    '7Key5': 'h', '7Key6': 'j', '7Key7': 'k', '7Key8': 'l', '7Key9': ';',
    '7Key10': 'n', '7Key11': 'm', '7Key12': ',', '7Key13': '.', '7Key14': '/'
}


def convert_notes_to_delayed_format(fileName, type):
    import os
    import json

    with open(os.path.join(getResourcesPath(), type, fileName + ".txt"), 'r',
              encoding=detect_encoding(os.path.join(getResourcesPath(), type, fileName + ".txt"))) as file:
        data = json.load(file)

    song_notes = data[0].get("songNotes", [])
    if not song_notes:
        return []

    result = []
    combined_keys = ""  # 将按键作为字符串存储
    combined_time = None  # 记录当前处理的相同时间

    for i, note in enumerate(song_notes):
        current_time = note["time"]
        key = note["key"]

        # 如果是新的时间点
        if current_time != combined_time:
            # 如果之前有累积的相同时间按键，先保存到结果中
            if combined_keys:
                # 计算延迟为下一个时间点与当前时间点的差
                next_time = song_notes[i]["time"] if i < len(song_notes) else current_time
                delay = next_time - combined_time
                result.append({"key": combined_keys, "delay": delay})

            # 开始新的时间点处理
            combined_time = current_time
            combined_keys = keyMap[key]  # 重新开始累积按键（存储为字符串）
        else:
            # 如果时间相同，合并按键（用逗号或其他分隔符连接字符串）
            combined_keys += keyMap[key]
    # 处理最后的累积按键
    if combined_keys:
        result.append({"key": combined_keys, "delay": 0})  # 最后一个条目的延迟为 0

    global_state.music_sheet = result





def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        # 读取文件的一部分进行编码检测
        raw_data = file.read(32000)  # 读取32KB数据
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        return encoding
