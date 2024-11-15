import os
import json
import librosa
import numpy as np
from tqdm import tqdm
import torch

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
    os.makedirs(output_dir, exist_ok=True)  # 确保目标目录存在
    device = select_device(use_gpu)
    try:
        y, sr = librosa.load(file_path, sr=None)
        y = librosa.resample(y, orig_sr=sr, target_sr=44100)
        sr = 44100
        total_frames = len(y)
        frame_rate = sr / 1000

        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = round(tempo)

        song_notes = []

        with tqdm(total=total_frames, desc="Processing Audio", unit="frame") as pbar:
            for frame_number in range(0, total_frames, int(frame_rate)):
                frame_time_ms = int((frame_number / sr) * 1000)  # 将时间戳转换为整数毫秒
                pitches, magnitudes = librosa.piptrack(y=y[frame_number:frame_number+int(frame_rate)], sr=sr)

                detected_notes = []
                for pitch_index, pitch in enumerate(pitches[:, 0]):
                    if magnitudes[pitch_index, 0] > 0.1:
                        key = get_advanced_key_mapping(pitch)
                        if key:
                            detected_notes.append(key)

                if detected_notes:
                    num_simultaneous = len(detected_notes)
                    for i, key in enumerate(detected_notes):
                        song_notes.append({"time": frame_time_ms, "key": f"{num_simultaneous}Key{i}"})

                pbar.update(int(frame_rate))

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
        new_file_path = os.path.join(os.path.dirname(file_path),
                                     os.path.splitext(name)[0] + "_ok" + os.path.splitext(file_path)[1])
        os.rename(file_path, new_file_path)
        print(f"已将文件 {file_path} 重命名为 {new_file_path}")

    except Exception as e:
        print(f"处理 {file_path} 时出错: {e}")

def process_directory_with_progress(directory_path, use_gpu=False, output_dir=getResourcesPath("myTranslate")):
    os.makedirs(output_dir, exist_ok=True)  # 确保目标目录存在
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.mp4'):
                process_audio_with_progress(os.path.join(root, file), use_gpu, output_dir)

# 示例调用
# process_audio_with_progress('example.mp3', use_gpu=True)
# process_directory_with_progress('/path/to/folder', use_gpu=True)
