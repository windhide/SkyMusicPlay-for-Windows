import json
import os

import pretty_midi

from windhide.musicToSheet.transfer_MID import inference
from windhide.static.global_variable import GlobalVariable
from windhide.utils.path_util import getResourcesPath

# 15个音符与键盘按键的映射
note_to_key = {'c¹_c³':{60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13',84:'1Key14'},"c_c²":{48:'1Key0',50:'1Key1',52:'1Key2',53:'1Key3',55:'1Key4',57:'1Key5',59:'1Key6',60:'1Key7',62:'1Key8',64:'1Key9',65:'1Key10',67:'1Key11',69:'1Key12',71:'1Key13',72:'1Key14'},"C_c¹":{36:'1Key0',38:'1Key1',40:'1Key2',41:'1Key3',43:'1Key4',45:'1Key5',47:'1Key6',48:'1Key7',50:'1Key8',52:'1Key9',53:'1Key10',55:'1Key11',57:'1Key12',59:'1Key13',60:'1Key14'},"c²_c⁴":{72:'1Key0',74:'1Key1',76:'1Key2',77:'1Key3',79:'1Key4',81:'1Key5',83:'1Key6',84:'1Key7',86:'1Key8',88:'1Key9',89:'1Key10',91:'1Key11',93:'1Key12',95:'1Key13',96:'1Key14'},"c³_c⁵":{84:'1Key0',86:'1Key1',88:'1Key2',89:'1Key3',91:'1Key4',93:'1Key5',95:'1Key6',96:'1Key7',98:'1Key8',100:'1Key9',101:'1Key10',103:'1Key11',105:'1Key12',107:'1Key13',108:'1Key14'},}
extra_note_to_key = {'c¹_c³':{61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],},"c_c²":{49:['1Key0','1Key1'],51:['1Key1','1Key2'],54:['1Key3','1Key4'],56:['1Key4','1Key5'],58:['1Key5','1Key6'],61:['1Key6','1Key7'],63:['1Key8','1Key9'],66:['1Key10','1Key11'],68:['1Key11','1Key12'],70:['1Key12','1Key13'],},"C_c¹":{37:['1Key0','1Key1'],39:['1Key1','1Key2'],42:['1Key3','1Key4'],44:['1Key4','1Key5'],46:['1Key5','1Key6'],49:['1Key6','1Key7'],51:['1Key8','1Key9'],54:['1Key10','1Key11'],56:['1Key11','1Key12'],58:['1Key12','1Key13'],},"c²_c⁴":{73:['1Key0','1Key1'],75:['1Key1','1Key2'],78:['1Key3','1Key4'],80:['1Key4','1Key5'],82:['1Key5','1Key6'],85:['1Key6','1Key7'],87:['1Key8','1Key9'],90:['1Key10','1Key11'],92:['1Key11','1Key12'],94:['1Key12','1Key13'],},"c³_c⁵":{85:['1Key0','1Key1'],87:['1Key1','1Key2'],90:['1Key3','1Key4'],92:['1Key4','1Key5'],94:['1Key5','1Key6'],97:['1Key6','1Key7'],99:['1Key8','1Key9'],102:['1Key10','1Key11'],104:['1Key11','1Key12'],106:['1Key12','1Key13'],},}
# 特殊音符的映射规则
special_note_mapping = {'c¹_c³':{86:81,88:83,89:84,},'c_c²':{74:69,76:71,77:72,},'C_c¹':{62:57,64:59,65:60,},'c²_c⁴':{98:93,100:95,101:96,},'c³_c⁵':{110:105,112:107,113:108,},}


# 根据 BPM 动态调整时间合并阈值
def get_dynamic_time_merge_threshold(bpm):
    # return max(20, min(80, int(60000 / bpm / 4)))  # 限制阈值在 10-50ms 之间
    return 0


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
                pitch, time, velocity= note.pitch, int(note.start * 1000), note.velocity
                if velocity < 10:
                    continue
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
        "name": os.path.basename(input_path) + version,
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

        for version in ["c³_c⁵", "c²_c⁴", "c¹_c³", "C_c¹", "c_c²"]:
            process_midi_to_txt(midFilePath + ".mid", os.path.join(output_dir, f"{fileNameNoEnd}_Range_{version}.txt"),
                                version)

        new_file_path = os.path.join(getResourcesPath("translateOriginalMusic"),
                                     f"{fileNameNoEnd}_ok.{file.split('.')[-1]}")
        os.rename(os.path.join(getResourcesPath("translateOriginalMusic"), file), new_file_path)
        print(f"已将文件 {file} 重命名为 {new_file_path}")
        GlobalVariable.overall_progress = ((idx + 1) / total_files) * 100

    GlobalVariable.overall_progress = 100
