import json
import os

import pretty_midi

from windhide.musicToSheet.transfer_MID import inference
from windhide.static.global_variable import GlobalVariable
from windhide.utils.path_util import getResourcesPath

# 15个音符与键盘按键的映射
note_to_key = {'standard':{60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13',84:'1Key14'},"low_harf":{53:'1Key0',55:'1Key1',57:'1Key2',58:'1Key3',60:'1Key4',62:'1Key5',64:'1Key6',65:'1Key7',67:'1Key8',69:'1Key9',70:'1Key10',72:'1Key11',74:'1Key12',76:'1Key13',77:'1Key14'},"low":{46:'1Key0',48:'1Key1',50:'1Key2',51:'1Key3',53:'1Key4',55:'1Key5',57:'1Key6',58:'1Key7',60:'1Key8',62:'1Key9',63:'1Key10',65:'1Key11',67:'1Key12',69:'1Key13',70:'1Key14'},"high_harf":{67:'1Key0',69:'1Key1',71:'1Key2',72:'1Key3',74:'1Key4',76:'1Key5',78:'1Key6',79:'1Key7',81:'1Key8',83:'1Key9',84:'1Key10',86:'1Key11',88:'1Key12',90:'1Key13',91:'1Key14'},"high":{74:'1Key0',76:'1Key1',78:'1Key2',79:'1Key3',81:'1Key4',83:'1Key5',85:'1Key6',86:'1Key7',88:'1Key8',90:'1Key9',91:'1Key10',93:'1Key11',95:'1Key12',97:'1Key13',98:'1Key14'},}
extra_note_to_key = {'standard':{61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],},"low_harf":{54:['1Key0','1Key1'],56:['1Key1','1Key2'],59:['1Key3','1Key4'],61:['1Key4','1Key5'],63:['1Key5','1Key6'],66:['1Key6','1Key7'],68:['1Key8','1Key9'],71:['1Key10','1Key11'],73:['1Key11','1Key12'],75:['1Key12','1Key13'],},"low":{47:['1Key0','1Key1'],49:['1Key1','1Key2'],52:['1Key3','1Key4'],54:['1Key4','1Key5'],56:['1Key5','1Key6'],59:['1Key6','1Key7'],61:['1Key8','1Key9'],64:['1Key10','1Key11'],66:['1Key11','1Key12'],68:['1Key12','1Key13'],},"high_harf":{68:['1Key0','1Key1'],70:['1Key1','1Key2'],73:['1Key3','1Key4'],75:['1Key4','1Key5'],77:['1Key5','1Key6'],80:['1Key6','1Key7'],82:['1Key8','1Key9'],85:['1Key10','1Key11'],87:['1Key11','1Key12'],89:['1Key12','1Key13'],},"high":{75:['1Key0','1Key1'],77:['1Key1','1Key2'],80:['1Key3','1Key4'],82:['1Key4','1Key5'],84:['1Key5','1Key6'],87:['1Key6','1Key7'],89:['1Key8','1Key9'],92:['1Key10','1Key11'],94:['1Key11','1Key12'],96:['1Key12','1Key13'],},}

# 特殊音符的映射规则
special_note_mapping = {'standard':{86:81,88:83,89:84,},'low_harf':{79:74,81:76,82:77,},'low':{72:67,74:69,75:70,},'high_harf':{93:88,95:90,96:91,},'high':{100:95,102:97,103:98,},}


# 根据 BPM 动态调整时间合并阈值
def get_dynamic_time_merge_threshold(bpm):
    return max(10, min(50, int(60000 / bpm / 4)))  # 限制阈值在 10-50ms 之间


# 15 个音符与键盘按键的映射
def get_bpm_from_midi(midi_file_path):
    midi = pretty_midi.PrettyMIDI(midi_file_path)
    tempos = midi.get_tempo_changes()
    return tempos[1][0] if len(tempos[1]) > 0 else 120


def merge_keys(keys):
    key_count = len(keys)
    return [f"{key_count}Key{key.replace('1Key', '')}" for key in keys]


def process_midi_to_txt(input_path, output_path, version):
    midi = pretty_midi.PrettyMIDI(input_path)
    bpm = get_bpm_from_midi(input_path)
    time_merge_threshold = get_dynamic_time_merge_threshold(bpm)
    notes = []

    for instrument in midi.instruments:
        if not instrument.is_drum:
            for note in instrument.notes:
                pitch, time = note.pitch, int(note.start * 1000)
                if pitch in note_to_key[version]:
                    notes.append({'time': time, 'key': note_to_key[version][pitch]})
                elif pitch in special_note_mapping[version]:
                    notes.append({'time': time, 'key': note_to_key[version][special_note_mapping[version][pitch]]})

    notes.sort(key=lambda x: x['time'])
    merged_notes, last_time, temp_keys = [], None, []

    for note in notes:
        if last_time is None or note['time'] - last_time <= time_merge_threshold:
            temp_keys.append(note['key'])
        else:
            merged_notes.extend({'time': last_time, 'key': k} for k in merge_keys(temp_keys))
            temp_keys = [note['key']]
        last_time = note['time']

    merged_notes.extend({'time': last_time, 'key': k} for k in merge_keys(temp_keys))
    output = [{
        "name": os.path.basename(input_path),
        "author": "skyMusic-WindHide",
        "transcribedBy": "WindHide'System",
        "bpm": bpm,
        "bitsPerPage": 15,
        "pitchLevel": 0,
        "isComposed": True,
        "songNotes": merged_notes,
        "isEncrypted": False,
    }]

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=4)

    return 100


def process_directory_with_progress(output_dir=getResourcesPath("myTranslate")):
    GlobalVariable.overall_progress = 0
    os.makedirs(output_dir, exist_ok=True)
    files_to_process = [f for f in os.listdir(getResourcesPath("translateOriginalMusic"))
                        if f.endswith(('.mp3', '.ogg', '.wav', '.flac', '.mid', '.m4a'))]
    total_files = len(files_to_process)

    if not total_files:
        print("没有找到需要处理的文件")
        return

    for idx, file in enumerate(files_to_process):
        if "_ok" in file:
            continue

        GlobalVariable.now_translate_text = [f"{idx + 1}/{total_files}", file]
        fileNameNoEnd = file.rsplit('.', 1)[0]
        midFilePath = os.path.join(getResourcesPath("translateMID"), f"{fileNameNoEnd}_basic_pitch")
        musicFilePath = os.path.join(getResourcesPath("translateOriginalMusic"), file)

        if not file.endswith(".mid"):
            inference(input_path=musicFilePath)
        else:
            midFilePath = os.path.join(getResourcesPath("translateOriginalMusic"), f"{fileNameNoEnd}")

        for version in ["high", "high_harf", "standard", "low", "low_harf"]:
            process_midi_to_txt(midFilePath + ".mid", os.path.join(output_dir, f"{fileNameNoEnd}_{version}.txt"),
                                version)

        new_file_path = os.path.join(getResourcesPath("translateOriginalMusic"),
                                     f"{fileNameNoEnd}_ok.{file.split('.')[-1]}")
        os.rename(os.path.join(getResourcesPath("translateOriginalMusic"), file), new_file_path)
        print(f"已将文件 {file} 重命名为 {new_file_path}")
        GlobalVariable.overall_progress = ((idx + 1) / total_files) * 100

    GlobalVariable.overall_progress = 100
