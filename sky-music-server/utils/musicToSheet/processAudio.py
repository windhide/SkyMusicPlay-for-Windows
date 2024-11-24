import os
import json
import librosa
import numpy as np
from tqdm import tqdm
import torch

from utils._global import global_state
from utils.pathUtils import getResourcesPath
import matplotlib.pyplot as plt
import librosa.display
from scipy.signal import butter, lfilter

try:
    np.complex = np.complex128
except AttributeError:
    pass  # Attribute was already corrected

def butter_highpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = lfilter(b, a, data)
    return y

def select_device(use_gpu=False):
    if use_gpu and torch.cuda.is_available():
        device = torch.device('cuda')
        print("使用 GPU 进行计算")
    else:
        device = torch.device('cpu')
        print("使用 CPU 进行计算")
    return device

def get_advanced_key_mapping(pitch_value):
    # 音高映射区间，从降E开始，逐步对应音符
    key_mapping = {
        (233, 261): '1Key1',    # 降E (E♭)
        (261, 293): '1Key2',    # F
        (293, 329): '1Key3',    # G
        (329, 349): '1Key4',    # 降A (A♭)
        (349, 370): '1Key5',    # 降B (B♭)
        (370, 415): '1Key6',    # C
        (415, 466): '1Key7',    # D
        (466, 523): '1Key8',    # 降E (E♭)
        (523, 587): '1Key9',    # F
        (587, 622): '1Key10',   # G
        (622, 698): '1Key11',   # 降A (A♭)
        (698, 784): '1Key12',   # 降B (B♭)
        (784, 880): '1Key13',   # C
        (880, 987): '1Key14',   # D
        (987, 1046): '1Key15',  # 降E (E♭)
    }

    for (low, high), key in key_mapping.items():
        if low <= pitch_value < high:
            return key
    return None

def process_audio_with_progress(file_path, use_gpu=False, output_dir=getResourcesPath("myTranslate")):
    if '_ok' in os.path.splitext(os.path.basename(file_path))[0]:
        print(f"跳过文件 {file_path}，因为它已带有 '_ok' 标记")
        # return 0

    os.makedirs(output_dir, exist_ok=True)
    device = select_device(use_gpu)
    global_state.translate_progress = 0
    try:
        y, sr = librosa.load(file_path, sr=None)

        # 1. 应用高通滤波器以去除低频鼓点
        cutoff_frequency = 100  # 设定高通滤波器截止频率
        y = butter_highpass_filter(y, cutoff=cutoff_frequency, fs=sr)

        # 2. 确保采样率为 44100
        y = librosa.resample(y, orig_sr=sr, target_sr=44100)
        sr = 44100
        total_frames = len(y)

        # 3. 提取节奏和 BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = round(float(tempo))

        song_notes = []
        frame_duration_ms = 100
        frame_samples = int(sr * (frame_duration_ms / 1000.0))

        with tqdm(total=total_frames, desc="处理进度", unit="样本") as pbar:
            for frame_start in range(0, total_frames, frame_samples):
                global_state.translate_progress = int((frame_start / total_frames) * 100)

                frame_y = y[frame_start:frame_start + frame_samples]
                if len(frame_y) == 0:
                    continue

                # 4. 音高检测
                f0, voiced_flag, voiced_probs = librosa.pyin(
                    frame_y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr
                )

                # 如果 f0 为空或者包含 NaN 值，跳过这一帧
                if f0 is None or np.all(np.isnan(f0)):
                    continue

                detected_notes = []
                for pitch in f0:
                    if pitch is not None and not np.isnan(pitch):  # 确保音高有效
                        # 5. 自动升调或降调
                        adjusted_pitch = pitch
                        while adjusted_pitch < 233:
                            adjusted_pitch *= 2
                        while adjusted_pitch > 1046:
                            adjusted_pitch /= 2

                        # 6. 获取音符映射
                        key = get_advanced_key_mapping(adjusted_pitch)
                        if key:
                            detected_notes.append(key)

                if detected_notes:
                    num_simultaneous = len(detected_notes)
                    frame_time_ms = int((frame_start / sr) * 1000)
                    for i, key in enumerate(detected_notes):
                        song_notes.append({"time": frame_time_ms, "key": f"{num_simultaneous}Key{i+1}"})

                pbar.update(frame_samples)  # 更新进度条

        # 7. 保存输出结果
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

        new_file_path = os.path.join(os.path.dirname(file_path), os.path.splitext(name)[0] + "_ok" + os.path.splitext(file_path)[1])
        os.rename(file_path, new_file_path)
        print(f"已将文件 {file_path} 重命名为 {new_file_path}")

        global_state.translate_progress = 100

    except Exception as e:
        print(f"处理 {file_path} 时出错: {e}")

    return global_state.translate_progress

def process_directory_with_progress(use_gpu=False, output_dir=getResourcesPath("myTranslate")):
    os.makedirs(output_dir, exist_ok=True)
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
