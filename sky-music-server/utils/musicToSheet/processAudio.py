import json
import os
import mido

from utils._global import global_state
from utils.musicToSheet.transferMID import inference
from utils.pathUtils import getResourcesPath


def get_bpm_from_midi(midi_file_path):
    """
    从 MIDI 文件中提取 BPM 值
    """
    midi = mido.MidiFile(midi_file_path)
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'set_tempo':  # 查找设置节奏的事件
                # BPM的计算方式：BPM = 60000000 / tempo
                bpm = 60000000 / msg.tempo
                return bpm
    return 120  # 如果没有找到BPM，则返回默认BPM 120


def generate_combination_keys(key, note_to_key, min_note, max_note):
    """
    根据音符的值生成可能的组合键。
    如果音符不在直接映射表中，则通过组合来生成。
    """
    combination_keys = []

    # 检查音符是否在映射表中
    if key in note_to_key:
        return [note_to_key[key]]

    # 如果音符在映射表中不存在，则通过组合其他音符来生成
    for i in range(min_note, max_note):
        if (key - i) in note_to_key:  # 检查两个音符的差值
            combination_keys.append(note_to_key[i])
            combination_keys.append(note_to_key[key - i])
            break  # 假设每个音符只会有一种组合方式

    return combination_keys


def process_midi_to_txt(input_path, output_path, min_note=60, max_note=84):
    # 15个音符与键盘按键的映射
    note_to_key = {
        60: '1Key1',  # Do
        62: '1Key2',  # Re
        64: '1Key3',  # Mi
        65: '1Key4',  # Fa
        67: '1Key5',  # So
        69: '1Key6',  # La
        71: '1Key7',  # Xi
        72: '1Key8',  # Do (高音)
        74: '1Key9',  # Re (高音)
        76: '1Key10',  # Mi (高音)
        77: '1Key11',  # Fa (高音)
        79: '1Key12',  # So (高音)
        81: '1Key13',  # La (高音)
        83: '1Key14',  # Xi (高音)
        84: '1Key15'  # 高高音Do
    }

    # 获取MIDI中的音符信息
    midi = mido.MidiFile(input_path)
    notes = []  # 存储所有音符的信息

    for index,track in enumerate(midi.tracks):
        time = 0  # 时间从零开始
        for msg in track:
            time += msg.time  # 累积时间
            if msg.type == 'note_on':
                notes.append({'time': time, 'note': msg.note})  # 记录音符和其时间点

    # 获取BPM值
    bpm = get_bpm_from_midi(input_path)

    # 按时间分类音符
    time_dict = {}

    for index, note in enumerate(notes):
        time = note['time']
        key = note['note']

        # 调整音符，如果超出范围则进行升调或降调
        if key < min_note:
            while key < min_note:
                key += 12  # 升调12个半音
        elif key > max_note:
            while key > max_note:
                key -= 12  # 降调12个半音

        # 如果时间点已存在，则添加到该时间点的列表中
        if time not in time_dict:
            time_dict[time] = []

        # 如果音符在指定范围内，则映射到相应的键位
        if key in note_to_key:
            time_dict[time].append(note_to_key[key])
        else:
            # 动态生成组合键
            combination_keys = generate_combination_keys(key, note_to_key, min_note, max_note)
            time_dict[time].extend(combination_keys)  # 将组合键添加到时间点的音符列表中

    # 处理同时按键的情况
    result = []
    for time in sorted(time_dict.keys()):
        keys = time_dict[time]
        # 按时间点顺序，为每个按键添加前缀
        for idx, key in enumerate(keys):
            result.append({
                "time": time,
                "key": f"{len(keys)}{key[1:]}"  # 替换"1Key"前缀并根据按键数添加前缀
            })

    # 构建输出字典
    output = [
        {
            "name": os.path.basename(input_path),  # 获取文件名
            "author": "skyMusic-WindHide",
            "transcribedBy": "WindHide'System",
            "bpm": bpm,  # 从MIDI中提取BPM
            "bitsPerPage": 15,
            "pitchLevel": 0,
            "isComposed": True,
            "songNotes": result,
            "isEncrypted": False,
        }
    ]
    # 将结果写入txt文件
    with open(output_path, 'w') as f:
        f.write(json.dumps(output, indent=4))  # 生成美化后的 JSON 格式

    return 100

def process_directory_with_progress(use_gpu=False, output_dir=getResourcesPath("myTranslate"), modelName=""):
    os.makedirs(output_dir, exist_ok=True)
    files_to_process = [f for f in os.listdir(getResourcesPath("translateOriginalMusic")) if f.endswith('.mp3') or f.endswith('.mp4') or f.endswith(".flac") or f.endswith(".ape")]
    total_files = len(files_to_process)
    if total_files == 0:
        print("没有找到需要处理的文件")
        return
    for idx, file in enumerate(files_to_process):
        if file.find("_ok") != -1: continue # 有ok就跳过

        global_state.now_translate_text = [str(idx + 1) + "/"+str(len(files_to_process)), file]
        global_state.tran_mid_progress = 0 # 进度条清空
        fileNameNoEnd = file.replace(".mp3", "").replace(".mp4", "").replace(".flac", "").replace(".ape", "")
        midFilePath =os.path.join(getResourcesPath("translateMID"), fileNameNoEnd)
        musicFilePath = os.path.join(getResourcesPath("translateOriginalMusic"), file)
        inference(
            input_path=musicFilePath,
            output_mid_path=midFilePath+".mid",
            _cuda=use_gpu,
            checkpoint_path=os.path.join(getResourcesPath("modelData"),modelName))
        file_progress = process_midi_to_txt(midFilePath+".mid",output_dir + "\\" + fileNameNoEnd + ".txt")

        # 完成的重命名 避免继续计算浪费资源
        new_file_path = os.path.join(midFilePath+".mid",
                                     os.path.splitext(musicFilePath)[0] + "_ok" +
                                     os.path.splitext(musicFilePath)[1])
        os.rename(musicFilePath, new_file_path)
        print(f"已将文件 {musicFilePath} 重命名为 {new_file_path}")

        global_state.overall_progress = ((idx + (file_progress / 100)) / total_files) * 100

    global_state.tran_mid_progress = 100
    global_state.overall_progress = 100
