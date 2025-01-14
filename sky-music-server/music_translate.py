import os

from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict_and_save

if __name__ == '__main__':
    # 定义输入文件和输出路径
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # 获取桌面路径
    output_midi_path = "D:\\Desktop"
    try:
        predict_and_save(
            [
                r"D:\Desktop\Dungeon and Fighter - 银色村庄 - silver crown.mp3"
            ],
            output_midi_path,
            True,
            False,
            False,
            False,
            ICASSP_2022_MODEL_PATH
        )
    except Exception as e:
        print(f"处理失败：{e}")
