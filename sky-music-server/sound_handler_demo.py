import sounddevice as sd
import librosa
import numpy as np
import time

samplerate = 44100
blocksize = 2048

# 音符映射
mapping = {0:"do", 2:"re", 4:"mi", 5:"fa", 7:"so", 9:"la", 11:"si"}

def freq_to_note(freq):
    if freq <= 0:
        return None
    midi = int(round(69 + 12 * np.log2(freq / 440.0)))
    return mapping.get(midi % 12)

current_note = None
note_start = time.time()

def callback(indata, frames, time_info, status):
    global current_note, note_start
    y = indata[:, 0]  # 取左声道即可

    # 静音检测
    rms = np.sqrt(np.mean(y**2))
    if rms < 0.01:  # 阈值可调
        return

    # pitch 检测
    f0 = librosa.yin(y, fmin=65, fmax=1000, sr=samplerate)
    freq = np.median(f0) if len(f0) else 0
    note = freq_to_note(freq)

    # 输出逻辑
    if note != current_note:
        if current_note is not None:
            duration = time.time() - note_start
            print(f"{current_note} - 持续 {duration:.2f}s")
        current_note = note
        note_start = time.time()


# ===== 自动获取系统默认输出设备 =====
default_output_index = sd.default.device[1]  # (input, output) tuple
device_info = sd.query_devices(default_output_index)
print("默认输出设备:", device_info['name'])

# ===== 配置 WASAPI 回环 =====
try:
    wasapi = sd.WasapiSettings()
    wasapi.loopback = True  # 开启回环
except AttributeError:
    print("⚠ 你的 sounddevice 版本太低，无法使用 WASAPI loopback。请升级：pip install --upgrade sounddevice")
    exit(1)

# ===== 开始监听系统播放声音 =====
with sd.InputStream(
    samplerate=samplerate,
    blocksize=blocksize,
    channels=1,
    device=default_output_index,
    dtype='float32',
    extra_settings=wasapi,
    callback=callback
):
    print("开始监听电脑播放的声音... Ctrl+C 停止")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("停止监听")
