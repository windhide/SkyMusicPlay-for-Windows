import json
import os
import pretty_midi

from utils._global import global_state
from utils.musicToSheet.transferMID import inference
from utils.pathUtils import getResourcesPath

# 可动态配置的时间合并阈值（单位：毫秒）
TIME_MERGE_THRESHOLD = 20

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

# 特殊音符的映射规则
special_note_mapping = {
    86: 81,  # 高高音Do
    88: 83,  # 高音Xi
    89: 84,  # 高音Do
}

def get_bpm_from_midi(midi_file_path):
    midi = pretty_midi.PrettyMIDI(midi_file_path)
    tempos = midi.get_tempo_changes()
    if len(tempos[1]) > 0:
        return tempos[1][0]  # 取第一个 BPM 值
    return 120  # 默认 BPM

def merge_keys(keys):
    """
    将同一时间点的多个按键进行合并，例如 ['1Key8', '1Key1'] -> ['2Key8', '2Key1']。
    """
    key_count = len(keys)
    merged_keys = []

    for key in keys:
        base_key = key.replace('1Key', '')  # 提取键编号
        merged_key = f"{key_count}Key{base_key}"
        merged_keys.append(merged_key)

    return merged_keys

def process_midi_to_txt(input_path, output_path, time_merge_threshold=TIME_MERGE_THRESHOLD):
    midi = pretty_midi.PrettyMIDI(input_path)
    notes = []  # 存储所有音符的信息

    # 提取音符信息
    for instrument in midi.instruments:
        if not instrument.is_drum:  # 忽略打击乐器
            for note in instrument.notes:
                pitch = note.pitch
                time = int(note.start * 1000)  # 时间转换为毫秒

                # 处理音符映射
                if pitch in note_to_key:
                    notes.append({'time': time, 'key': note_to_key[pitch]})
                elif pitch in extra_note_to_key:
                    for extra_key in extra_note_to_key[pitch]:
                        notes.append({'time': time, 'key': extra_key})
                elif pitch in special_note_mapping:
                    notes.append({'time': time, 'key': note_to_key[special_note_mapping[pitch]]})

    # 按时间排序
    notes.sort(key=lambda x: x['time'])

    # 合并时间点接近的音符
    merged_notes = []
    last_time = None
    temp_keys = []
    for note in notes:
        time = note['time']
        key = note['key']
        if last_time is None or time - last_time <= time_merge_threshold:
            # 累加同一时间点的按键
            temp_keys.append(key)
        else:
            # 合并并保存上一组按键
            merged_keys = merge_keys(temp_keys)
            for merged_key in merged_keys:
                merged_notes.append({'time': last_time, 'key': merged_key})
            temp_keys = [key]

        last_time = time

    # 处理最后一组音符
    merged_keys = merge_keys(temp_keys)
    for merged_key in merged_keys:
        merged_notes.append({'time': last_time, 'key': merged_key})

    index = 10
    while(True):
        # 检查谱子的长度
        if len(merged_notes) < 50:
            new_notes = []
            for note in notes:
                pitch = note['key']
                original_pitch = int(pitch.split('Key')[-1])  # 提取原始音符编号
                new_pitch = original_pitch - 1  # 整体降调一个半音
                time = note['time']
                # 映射新的降调音符
                if new_pitch in note_to_key:
                    new_notes.append({'time': time, 'key': note_to_key[new_pitch]})
                elif new_pitch in extra_note_to_key:
                    for extra_key in extra_note_to_key[new_pitch]:
                        new_notes.append({'time': time, 'key': extra_key})
            merged_notes = new_notes  # 更新降调后的音符列表
        if len(merged_notes) > 50:
            break

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
            "songNotes": merged_notes,
            "isEncrypted": False,
        }
    ]

    # 将结果写入TXT文件
    with open(output_path, 'w') as f:
        f.write(json.dumps(output, indent=4))

    return 100

def process_directory_with_progress(use_gpu=False, output_dir=getResourcesPath("myTranslate"), modelName=""):
    os.makedirs(output_dir, exist_ok=True)
    files_to_process = [f for f in os.listdir(getResourcesPath("translateOriginalMusic")) if f.endswith(('.mp3', '.mp4', '.flac', '.ape', '.mid'))]
    total_files = len(files_to_process)

    if total_files == 0:
        print("没有找到需要处理的文件")
        return

    for idx, file in enumerate(files_to_process):
        if "_ok" in file:
            continue

        global_state.now_translate_text = [f"{idx + 1}/{total_files}", file]
        global_state.tran_mid_progress = 0
        fileNameNoEnd = file.rsplit('.', 1)[0]

        if not file.endswith(".mid"):
            midFilePath = os.path.join(getResourcesPath("translateMID"), fileNameNoEnd)
            musicFilePath = os.path.join(getResourcesPath("translateOriginalMusic"), file)
            inference(input_path=musicFilePath, output_mid_path=midFilePath + ".mid", _cuda=use_gpu, checkpoint_path=os.path.join(getResourcesPath("modelData"), modelName))
        else:
            midFilePath = os.path.join(getResourcesPath("translateOriginalMusic"), fileNameNoEnd)

        process_midi_to_txt(midFilePath + ".mid", os.path.join(output_dir, f"{fileNameNoEnd}.txt"))

        new_file_path = os.path.join(getResourcesPath("translateOriginalMusic"), f"{fileNameNoEnd}_ok.{file.split('.')[-1]}")
        os.rename(os.path.join(getResourcesPath("translateOriginalMusic"), file), new_file_path)

        print(f"已将文件 {file} 重命名为 {new_file_path}")
        global_state.overall_progress = ((idx + 1) / total_files) * 100


    global_state.tran_mid_progress = 100
    global_state.overall_progress = 100
