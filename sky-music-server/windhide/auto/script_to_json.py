import json
import re
from os import path
from charset_normalizer import detect

from windhide.utils.path_util import getResourcesPath


async def script_to_json(content, file_name):
    file_content = content.decode(detect(content)['encoding']) + ""
    stringList = file_content.splitlines()
    result = []
    # 匹配并提取数据
    for index, value in enumerate(stringList):
        if index % 2 == 1:
            type = "Down" if "Down" in stringList[index-1] else "Up"
            result.append({
                "key": stringList[index-1].replace(" ", "").replace(f"Key{type}:",""),
                "type": type,
                "delay": stringList[index].replace(" ", "").replace("延迟:","").replace("ms","")
            })
    # 按原始文本顺序输出结果
    output_json = json.dumps(result, ensure_ascii=False, indent=4)
    filePath = path.join(getResourcesPath("systemTools"),"scriptTemplate", f"{file_name}.json")
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(output_json)
    return output_json