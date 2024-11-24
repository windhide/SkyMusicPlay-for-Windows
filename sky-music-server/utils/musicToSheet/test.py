import librosa
import pretty_midi
import numpy as np

# 加载音频文件
y, sr = librosa.load('music_file.mp3', sr=None)

# 获取梅尔频谱
mel_spectrogram = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)

# 将梅尔频谱转换为音高（相对音高）
pitches, magnitudes = librosa.core.piptrack(S=librosa.power_to_db(mel_spectrogram), sr=sr)

# 创建一个PrettyMIDI对象
midi = pretty_midi.PrettyMIDI()

# 创建一个乐器对象 (钢琴)
instrument = pretty_midi.Instrument(program=0)

# 为乐器添加音符
for i in range(len(pitches)):
    pitch = np.argmax(pitches[:, i])
    if pitch > 0:
        note = pretty_midi.Note(
            velocity=int(magnitudes[pitch, i]), pitch=pitch + 21, start=i / sr, end=(i + 1) / sr
        )
        instrument.notes.append(note)




# 主程序
if __name__ == "__main__":
    # 将乐器添加到MIDI对象
    midi.instruments.append(instrument)
    # 将MIDI文件保存到文件
    midi.write('output.mid')
    # 播放生成的MIDI文件
    import pygame.midi
    pygame.midi.init()
    player = pygame.midi.Output(0)
    midi_data = pretty_midi.PrettyMIDI('output.mid')
    midi_data.write('output.mid')
    pygame.midi.quit()
