import json
import re
from os import path
from charset_normalizer import detect

from windhide.utils.path_util import getResourcesPath


async def script_to_json(content, file_name):
    file_content = content.decode(detect(content)['encoding']) + ""
    # 处理换行符
    file_content = file_content.replace("\r\n", "\n")
    lines = file_content.split("\n")

    # 定义正则表达式匹配事件和延迟
    event_pattern = re.compile(r"(Key Down|Key Up|Mouse Position|Mouse Event|Mouse Scroll Down) ?.*")
    delay_pattern = re.compile(r"延迟\s*:\s*(\d+)\s*ms")
    position_pattern = re.compile(r"Mouse Position\s*:\s*X:(\d+)\s*Y:(\d+)")  # 匹配鼠标位置

    # 转换日志为数组
    events = []
    unparsed_lines = []  # 用于记录无法解析的行

    # 遍历每行并处理事件和延迟
    i = 0
    while i < len(lines):
        line = lines[i]
        event_match = event_pattern.search(line)

        if event_match:
            event_type = event_match.group(1)
            # 预检查下一行是否有延迟信息
            delay = 0
            if i + 1 < len(lines):
                delay_match = delay_pattern.search(lines[i + 1])
                if delay_match:
                    delay = int(delay_match.group(1))
                    i += 1  # 跳过已处理的延迟行

            # 处理鼠标事件
            if "Mouse" in event_type:
                if "Scroll Down" in event_type:
                    key = "mouse"
                    type_ = "scroll_down"
                elif "Left Down" in event_type:
                    key = "mouse"
                    type_ = "left_down"
                elif "Left Up" in event_type:
                    key = "mouse"
                    type_ = "left_up"
                else:
                    key = "mouse"
                    type_ = "unknown"
            # 处理键盘事件
            elif "Key" in event_type:
                key = line.split(":")[-1].strip()  # 提取键值
                if "Down" in event_type:
                    type_ = "Down"
                elif "Up" in event_type:
                    type_ = "Up"
            else:
                i += 1
                continue  # 跳过无法解析的行

            # 如果前一个事件与当前事件类型和键值相同，则累加延迟
            if events and events[-1]['key'] == key and events[-1]['type'] == type_:
                events[-1]['delay'] += delay
            else:
                events.append({
                    "key": key,
                    "type": type_,
                    "delay": delay
                })
        else:
            # 如果行无法解析，记录下来
            unparsed_lines.append(line)

        i += 1

    # 输出未解析的行
    if unparsed_lines:
        print("无法解析的行：")
        for unparsed in unparsed_lines:
            print(unparsed)

    # 按原始文本顺序输出结果
    output_json = json.dumps(events, ensure_ascii=False, indent=4)
    filePath = path.join(getResourcesPath("systemTools"), "scriptTemplate", file_name.replace(".txt", "") + ".json")
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(output_json)
    return events

