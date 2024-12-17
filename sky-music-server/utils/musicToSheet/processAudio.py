import json
import os
import pretty_midi

from utils._global import global_state
from utils.musicToSheet.transferMID import inference
from utils.pathUtils import getResourcesPath

# 15个音符与键盘按键的映射
note_to_key = {
    60: '1Key0',  # Do
    62: '1Key1',  # Re
    64: '1Key2',  # Mi
    65: '1Key3',  # Fa
    67: '1Key4',  # So
    69: '1Key5',  # La
    71: '1Key6',  # Xi
    72: '1Key7',  # Do (高音)
    74: '1Key8',  # Re (高音)
    76: '1Key9',  # Mi (高音)
    77: '1Key10',  # Fa (高音)
    79: '1Key11',  # So (高音)
    81: '1Key12',  # La (高音)
    83: '1Key13',  # Xi (高音)
    84: '1Key14'   # 高高音Do
}

# 范围内但不在 note_to_key 中的音符映射（表示同时按键）
extra_note_to_key = {
    61: ['1Key0', '1Key1'],
    63: ['1Key1', '1Key2'],
    66: ['1Key3', '1Key4'],
    68: ['1Key4', '1Key5'],
    70: ['1Key5', '1Key6'],
    73: ['1Key6', '1Key7'],
    75: ['1Key8', '1Key9'],
    78: ['1Key10', '1Key11'],
    80: ['1Key11', '1Key12'],
    82: ['1Key12', '1Key13'],
}

# 允许的音符集合
allowed_notes = set(note_to_key.keys()).union(extra_note_to_key.keys())

# 特殊音符的映射规则
special_note_mapping = {
    86: 81,  # 高高音Do
    88: 83,  # 高音Xi
    89: 84,  # 高音Do
}

# 获取BPM值
def get_bpm_from_midi(midi_file_path):
    midi = pretty_midi.PrettyMIDI(midi_file_path)
    tempos = midi.get_tempo_changes()
    if len(tempos[1]) > 0:
        return tempos[1][0]  # 取第一个 BPM 值
    return 120  # 默认 BPM


# 处理MIDI文件并转换为txt格式
def process_midi_to_txt(input_path, output_path):
    midi = pretty_midi.PrettyMIDI(input_path)
    notes = []  # 存储所有音符的信息

    for instrument in midi.instruments:
        for note in instrument.notes:
            pitch = note.pitch
            time = int(note.start * 1000)  # 时间转换为毫秒

            # 处理标准音符
            if pitch in note_to_key:
                notes.append({'time': time, 'key': note_to_key[pitch]})

            # 处理额外音符（如范围内的音符）
            elif pitch in extra_note_to_key:
                for extra_key in extra_note_to_key[pitch]:
                    notes.append({'time': time, 'key': extra_key})

            # 处理特殊音符（如高音符）
            elif pitch in special_note_mapping:
                notes.append({'time': time, 'key': note_to_key[special_note_mapping[pitch]]})

    # 按时间点整理音符
    time_dict = {}
    for note in notes:
        time = note['time']
        key = note['key']
        if time not in time_dict:
            time_dict[time] = []
        time_dict[time].append(key)

    # 生成结果，处理同时按键的情况
    result = []
    for time in sorted(time_dict.keys()):
        keys = time_dict[time]
        for key in keys:
            result.append({
                "time": time,
                "key": key
            })

    # 获取BPM值
    bpm = get_bpm_from_midi(input_path)

    # 构建输出字典
    output = [
        {
            "name": os.path.basename(input_path),
            "author": "skyMusic-WindHide",
            "transcribedBy": "WindHide'System",
            "bpm": bpm,
            "bitsPerPage": 15,
            "pitchLevel": 0,
            "isComposed": True,
            "songNotes": result,
            "isEncrypted": False,
        }
    ]

    # 将结果写入TXT文件
    with open(output_path, 'w') as f:
        f.write(json.dumps(output, indent=4))

    return 100


# 处理文件夹内的所有MIDI文件
def process_directory_with_progress(use_gpu=False, output_dir=getResourcesPath("myTranslate"), modelName=""):
    os.makedirs(output_dir, exist_ok=True)
    files_to_process = [f for f in os.listdir(getResourcesPath("translateOriginalMusic")) if f.endswith('.mp3') or f.endswith('.mp4') or f.endswith(".flac") or f.endswith(".ape") or f.endswith(".mid")]
    total_files = len(files_to_process)
    if total_files == 0:
        print("没有找到需要处理的文件")
        return
    for idx, file in enumerate(files_to_process):
        if file.find("_ok") != -1: continue # 有ok就跳过
        try:
            global_state.now_translate_text = [str(idx + 1) + "/"+str(len(files_to_process)), file]
            global_state.tran_mid_progress = 0 # 进度条清空
            fileNameNoEnd = ''
            musicFilePath = ''
            if not file.endswith(".mid"):
                fileNameNoEnd = file.replace(".mp3", "").replace(".mp4", "").replace(".flac", "").replace(".ape", "")
                midFilePath =os.path.join(getResourcesPath("translateMID"), fileNameNoEnd)
                musicFilePath = os.path.join(getResourcesPath("translateOriginalMusic"), file)
                inference(
                    input_path=musicFilePath,
                    output_mid_path=midFilePath+".mid",
                    _cuda=use_gpu,
                    checkpoint_path=os.path.join(getResourcesPath("modelData"),modelName))
            else:
                fileNameNoEnd = file.replace(".mid","")
                midFilePath =os.path.join(getResourcesPath("translateOriginalMusic"), fileNameNoEnd)

            file_progress = process_midi_to_txt(midFilePath+".mid",output_dir + "\\" + fileNameNoEnd + ".txt")
            # 完成的重命名 避免继续计算浪费资源
            new_file_path = os.path.join(midFilePath+".mid",
                                         os.path.splitext(musicFilePath)[0] + "_ok" +
                                         os.path.splitext(musicFilePath)[1])
            os.rename(musicFilePath, new_file_path)
            print(f"已将文件 {musicFilePath} 重命名为 {new_file_path}")

            global_state.overall_progress = ((idx + (file_progress / 100)) / total_files) * 100
        except Exception as e:
            print(e)

    global_state.tran_mid_progress = 100
    global_state.overall_progress = 100
