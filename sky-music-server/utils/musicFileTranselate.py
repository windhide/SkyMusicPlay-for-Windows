import json


def convert_notes_to_delayed_format(json_data):
    song_notes = json_data.get("songNotes", [])
    if not song_notes:
        return []

    result = []
    combined_keys = []  # 用于存储相同时间的按键
    combined_time = None  # 记录当前处理的相同时间

    for i, note in enumerate(song_notes):
        current_time = note["time"]
        key = note["key"]

        # 如果是新的时间点
        if current_time != combined_time:
            # 如果之前有累积的相同时间按键，先保存到结果中
            if combined_keys:
                # 计算延迟为下一个时间点与当前时间点的差
                next_time = song_notes[i]["time"] if i < len(song_notes) else current_time
                delay = next_time - combined_time
                result.append({"key": combined_keys, "delay": delay})

            # 开始新的时间点处理
            combined_time = current_time
            combined_keys = [key]
        else:
            # 如果时间相同，合并按键
            combined_keys.append(key)

    # 处理最后的累积按键
    if combined_keys:
        result.append({"key": combined_keys, "delay": 0})  # 最后一个条目的延迟为 0

    return result

