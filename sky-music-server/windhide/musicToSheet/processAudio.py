import json
import os
import pretty_midi

from windhide._global import globalVariable
from windhide.musicToSheet.transferMID import inference
from windhide.utils.pathUtils import getResourcesPath

# 可动态配置的时间合并阈值（单位：毫秒）
TIME_MERGE_THRESHOLD = 20

# 15个音符与键盘按键的映射
note_to_key = {'standard':{60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13',84:'1Key14'},"low_harf":{53:'1Key0',55:'1Key1',57:'1Key2',58:'1Key3',60:'1Key4',62:'1Key5',64:'1Key6',65:'1Key7',67:'1Key8',69:'1Key9',70:'1Key10',72:'1Key11',74:'1Key12',76:'1Key13',77:'1Key14'},"low":{46:'1Key0',48:'1Key1',50:'1Key2',51:'1Key3',53:'1Key4',55:'1Key5',57:'1Key6',58:'1Key7',60:'1Key8',62:'1Key9',63:'1Key10',65:'1Key11',67:'1Key12',69:'1Key13',70:'1Key14'},"high_harf":{67:'1Key0',69:'1Key1',71:'1Key2',72:'1Key3',74:'1Key4',76:'1Key5',78:'1Key6',79:'1Key7',81:'1Key8',83:'1Key9',84:'1Key10',86:'1Key11',88:'1Key12',90:'1Key13',91:'1Key14'},"high":{74:'1Key0',76:'1Key1',78:'1Key2',79:'1Key3',81:'1Key4',83:'1Key5',85:'1Key6',86:'1Key7',88:'1Key8',90:'1Key9',91:'1Key10',93:'1Key11',95:'1Key12',97:'1Key13',98:'1Key14'},}
extra_note_to_key = {'standard':{61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],},"low_harf":{54:['1Key0','1Key1'],56:['1Key1','1Key2'],59:['1Key3','1Key4'],61:['1Key4','1Key5'],63:['1Key5','1Key6'],66:['1Key6','1Key7'],68:['1Key8','1Key9'],71:['1Key10','1Key11'],73:['1Key11','1Key12'],75:['1Key12','1Key13'],},"low":{47:['1Key0','1Key1'],49:['1Key1','1Key2'],52:['1Key3','1Key4'],54:['1Key4','1Key5'],56:['1Key5','1Key6'],59:['1Key6','1Key7'],61:['1Key8','1Key9'],64:['1Key10','1Key11'],66:['1Key11','1Key12'],68:['1Key12','1Key13'],},"high_harf":{68:['1Key0','1Key1'],70:['1Key1','1Key2'],73:['1Key3','1Key4'],75:['1Key4','1Key5'],77:['1Key5','1Key6'],80:['1Key6','1Key7'],82:['1Key8','1Key9'],85:['1Key10','1Key11'],87:['1Key11','1Key12'],89:['1Key12','1Key13'],},"high":{75:['1Key0','1Key1'],77:['1Key1','1Key2'],80:['1Key3','1Key4'],82:['1Key4','1Key5'],84:['1Key5','1Key6'],87:['1Key6','1Key7'],89:['1Key8','1Key9'],92:['1Key10','1Key11'],94:['1Key11','1Key12'],96:['1Key12','1Key13'],},}

# 特殊音符的映射规则
special_note_mapping = {'standard':{86:81,88:83,89:84,},'low_harf':{79:74,81:76,82:77,},'low':{72:67,74:69,75:70,},'high_harf':{93:88,95:90,96:91,},'high':{100:95,102:97,103:98,},}

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

def process_midi_to_txt(input_path, output_path, version, time_merge_threshold=TIME_MERGE_THRESHOLD):
    midi = pretty_midi.PrettyMIDI(input_path)
    notes = []  # 存储所有音符的信息

    # 提取音符信息
    for instrument in midi.instruments:
        if not instrument.is_drum:  # 忽略打击乐器
            for note in instrument.notes:
                pitch = note.pitch
                time = int(note.start * 1000)  # 时间转换为毫秒

                # 处理音符映射
                if pitch in note_to_key[version]:
                    notes.append({'time': time, 'key': note_to_key[version][pitch]})
                elif pitch in extra_note_to_key[version]:
                    for extra_key in extra_note_to_key[version][pitch]:
                        notes.append({'time': time, 'key': extra_key})
                elif pitch in special_note_mapping[version]:
                    notes.append({'time': time, 'key': note_to_key[version][special_note_mapping[version][pitch]]})

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

        globalVariable.now_translate_text = [f"{idx + 1}/{total_files}", file]
        globalVariable.tran_mid_progress = 0
        fileNameNoEnd = file.rsplit('.', 1)[0]

        if not file.endswith(".mid"):
            midFilePath = os.path.join(getResourcesPath("translateMID"), fileNameNoEnd)
            musicFilePath = os.path.join(getResourcesPath("translateOriginalMusic"), file)
            inference(input_path=musicFilePath, output_mid_path=midFilePath + ".mid", _cuda=use_gpu, checkpoint_path=os.path.join(getResourcesPath("modelData"), modelName))
        else:
            midFilePath = os.path.join(getResourcesPath("translateOriginalMusic"), fileNameNoEnd)

        process_midi_to_txt(midFilePath + ".mid", os.path.join(output_dir, f"{fileNameNoEnd}{'_标准'}.txt"),"standard")
        process_midi_to_txt(midFilePath + ".mid", os.path.join(output_dir, f"{fileNameNoEnd}{'_降半音'}.txt"),"low_harf")
        process_midi_to_txt(midFilePath + ".mid", os.path.join(output_dir, f"{fileNameNoEnd}{'_降调'}.txt"),"low")
        process_midi_to_txt(midFilePath + ".mid", os.path.join(output_dir, f"{fileNameNoEnd}{'_升半音'}.txt"),"high_harf")
        process_midi_to_txt(midFilePath + ".mid", os.path.join(output_dir, f"{fileNameNoEnd}{'_升调'}.txt"),"high")
        new_file_path = os.path.join(getResourcesPath("translateOriginalMusic"), f"{fileNameNoEnd}_ok.{file.split('.')[-1]}")
        os.rename(os.path.join(getResourcesPath("translateOriginalMusic"), file), new_file_path)

        print(f"已将文件 {file} 重命名为 {new_file_path}")
        globalVariable.overall_progress = ((idx + 1) / total_files) * 100


    globalVariable.tran_mid_progress = 100
    globalVariable.overall_progress = 100
