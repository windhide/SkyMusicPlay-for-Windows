import json
import re
from os import path
from charset_normalizer import detect

from windhide.utils.path_util import getResourcesPath


async def script_to_json(content):
    file_content = content.decode(detect(content)['encoding'])
    event_pattern = re.compile(r"(Key (?:Down|Up)) : (\S+)\n延迟 : (\d+) ms")
    # 用于存储结果的列表
    result = []
    # 匹配并提取数据
    for match in event_pattern.finditer(file_content):
        event_type = match.group(1).replace("Key ", "")  # "Down" 或 "Up"
        key = match.group(2)  # 键值，例如 "2" 或 "Space"
        delay = int(match.group(3))  # 延迟时间（整数）
        # 构建 JSON 对象
        result.append({
            "type": event_type,
            "key": key,
            "delay": delay
        })
    # 按原始文本顺序输出结果
    output_json = json.dumps(result, ensure_ascii=False, indent=4)
    filePath = path.join(getResourcesPath(""),"output.json")
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(output_json)
    return output_json