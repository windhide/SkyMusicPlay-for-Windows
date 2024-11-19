import os
import json
import librosa
import numpy as np
from tqdm import tqdm
import torch

from utils._global import global_state
from utils.pathUtils import getResourcesPath


def select_device(use_gpu=False):
    if use_gpu and torch.cuda.is_available():
        device = torch.device('cuda')
        print("使用 GPU 进行计算")
    else:
        device = torch.device('cpu')
        print("使用 CPU 进行计算")
    return device

def get_advanced_key_mapping(pitch_value):
    if 260 <= pitch_value < 293:  # Do (C)
        return '1Key1'
    elif 293 <= pitch_value < 329:  # Re (D)
        return '1Key2'
    elif 329 <= pitch_value < 349:  # Mi (E)
        return '1Key3'
    elif 349 <= pitch_value < 392:  # Fa (F)
        return '1Key4'
    elif 392 <= pitch_value < 440:  # So (G)
        return '1Key5'
    elif 440 <= pitch_value < 493:  # La (A)
        return '1Key6'
    elif 493 <= pitch_value < 523:  # Xi (B)
        return '1Key7'
    elif 523 <= pitch_value < 554:  # 高音 Do (C)
        return '1Key8'
    elif 554 <= pitch_value < 587:  # 高音 Re (D)
        return '1Key9'
    elif 587 <= pitch_value < 622:  # 高音 Mi (E)
        return '1Key10'
    elif 622 <= pitch_value < 698:  # 高音 Fa (F)
        return '1Key11'
    elif 698 <= pitch_value < 784:  # 高音 So (G)
        return '1Key12'
    elif 784 <= pitch_value < 880:  # 高音 La (A)
        return '1Key13'
    elif 880 <= pitch_value < 987:  # 高音 Xi (B)
        return '1Key14'
    elif 987 <= pitch_value < 1046:  # 高高音 Do (C)
        return '1Key15'
    return None

def process_audio_with_progress(file_path, use_gpu=False, output_dir=getResourcesPath("myTranslate")):
    if '_ok' in os.path.splitext(os.path.basename(file_path))[0]:
        print(f"跳过文件 {file_path}，因为它已带有 '_ok' 标记")
        return 0  # 不处理的文件返回进度为 0%

    os.makedirs(output_dir, exist_ok=True)  # 确保目标目录存在
    device = select_device(use_gpu)
    global_state.translate_progress = 0  # 初始化进度变量
    try:
        y, sr = librosa.load(file_path, sr=None)
        y = librosa.resample(y, orig_sr=sr, target_sr=44100)
        sr = 44100
        total_frames = len(y)
        frame_rate = sr / 1000

        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = round(float(tempo))

        song_notes = []

        for frame_number in range(0, total_frames, int(frame_rate)):
            # 更新进度百分比
            global_state.translate_progress = int((frame_number / total_frames) * 100)
            print(f"处理进度: {global_state.translate_progress}%")  # 输出进度

            frame_time_ms = int((frame_number / sr) * 1000)  # 将时间戳转换为整数毫秒
            pitches, magnitudes = librosa.piptrack(y=y[frame_number:frame_number + int(frame_rate)], sr=sr, n_fft=512, hop_length=256)

            detected_notes = []
            for pitch_index, pitch in enumerate(pitches[:, 0]):
                if magnitudes[pitch_index, 0] > 0.1:
                    key = get_advanced_key_mapping(pitch)
                    print(f"Detected pitch: {pitch}")
                    if key:
                        detected_notes.append(key)
                    else:
                        print(f"Pitch {pitch} did not match any key mapping")

            if detected_notes:
                num_simultaneous = len(detected_notes)
                for i, key in enumerate(detected_notes):
                    song_notes.append({"time": frame_time_ms, "key": f"{num_simultaneous}Key{i}"})

        name = os.path.basename(file_path)
        output_filename = os.path.join(output_dir, f"{os.path.splitext(name)[0]}.txt")
        result = [{
            "name": name,
            "bpm": bpm,
            "bitsPerPage": 16,
            "pitchLevel": 0,
            "isComposed": False,
            "songNotes": song_notes
        }]

        with open(output_filename, 'w') as f:
            json.dump(result, f)

        # 标记处理完成的源文件
        new_file_path = os.path.join(os.path.dirname(file_path), os.path.splitext(name)[0] + "_ok" + os.path.splitext(file_path)[1])
        os.rename(file_path, new_file_path)
        print(f"已将文件 {file_path} 重命名为 {new_file_path}")

        # 处理完成时将进度设置为100%
        global_state.translate_progress = 100
        print(f"处理进度: {global_state.translate_progress}%")

    except Exception as e:
        print(f"处理 {file_path} 时出错: {e}")

    return global_state.translate_progress


def process_directory_with_progress(use_gpu=False, output_dir=getResourcesPath("myTranslate")):
    os.makedirs(output_dir, exist_ok=True)  # 确保目标目录存在
    files_to_process = [f for f in os.listdir(getResourcesPath("translateOriginalMusic")) if f.endswith('.mp3') or f.endswith('.mp4') or f.endswith(".flac")]
    total_files = len(files_to_process)
    if total_files == 0:
        print("没有找到需要处理的文件")
        return
    for idx, file in enumerate(files_to_process):
        file_path = os.path.join(getResourcesPath("translateOriginalMusic"), file)
        global_state.now_translate_text = [str(idx + 1) + "/"+str(len(files_to_process)), file.replace(".mp3","")]
        file_progress = process_audio_with_progress(file_path, use_gpu, output_dir)
        global_state.overall_progress = ((idx + (file_progress / 100)) / total_files) * 100
