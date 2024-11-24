import librosa
import numpy as np
from midiutil import MIDIFile
import pygame
import os


def extract_main_melody(audio_file, sr=22050, hop_length=512, threshold=0.1):
    """
    提取音频文件中的主旋律音符。
    """
    # 加载音频
    y, sr = librosa.load(audio_file, sr=sr)

    # 计算谐波频谱
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, hop_length=hop_length)

    melody_notes = []
    for t in range(pitches.shape[1]):  # 遍历每一帧
        index = magnitudes[:, t].argmax()  # 获取强度最大的频率索引
        pitch = pitches[index, t]
        if magnitudes[index, t] > threshold:  # 过滤掉低强度的音高
            midi_note = librosa.hz_to_midi(pitch)
            melody_notes.append(int(midi_note))

    # 去除重复音符（简单降噪）
    filtered_notes = []
    prev_note = None
    for note in melody_notes:
        if note != prev_note:  # 只保留音高变化的音符
            filtered_notes.append(note)
            prev_note = note

    return filtered_notes


def create_midi(notes, output_file, tempo=120):
    """
    将音符列表转换为 MIDI 文件。
    """
    midi = MIDIFile(1)  # 创建一个单轨 MIDI 文件
    track = 0
    time = 0
    midi.addTrackName(track, time, "Extracted Melody")
    midi.addTempo(track, time, tempo)

    duration = 1  # 每个音符持续 1 拍
    channel = 0
    volume = 100

    for note in notes:
        midi.addNote(track, channel, note, time, duration, volume)
        time += duration  # 时间递增

    with open(output_file, "wb") as f:
        midi.writeFile(f)


def play_midi(file_path):
    """
    播放 MIDI 文件。
    """
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.quit()


def main(audio_file):
    """
    主函数：从音频文件生成主旋律并播放。
    """
    print("提取主旋律中...")
    notes = extract_main_melody(audio_file)
    print(f"提取到的主旋律音符数量: {len(notes)}")

    midi_file = "output_melody.mid"
    print("生成主旋律 MIDI 文件...")
    create_midi(notes, midi_file)

    print("播放生成的主旋律 MIDI 文件...")
    play_midi(midi_file)

    # 可选：清理生成的 MIDI 文件
    os.remove(midi_file)


# 测试用例
audio_file = "your_audio_file.wav"  # 替换为你的音频文件路径
main(audio_file)
