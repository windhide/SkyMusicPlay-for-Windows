import json
import os
import re

# from google import genai
from openai import OpenAI

from windhide.static.global_variable import GlobalVariable
from windhide.utils.path_util import getResourcesPath
from windhide.utils.play_util import detect_encoding


# def gemini_ai(model,filename, type_):
#     client = genai.Client(api_key=GlobalVariable.ai_token["Gemini"])
#     song_data = loadSheetFile(type_,filename)
#     contents = GlobalVariable.duration_prompt if model == 'duration' else GlobalVariable.translate_prompt
#     contents = contents.replace("{input}",json.dumps(song_data["songNotes"]))
#     print(contents)
#     response = client.models.generate_content(
#         model="gemini-2.5-flash-preview-05-20", contents=contents
#     )
#     return match_to_sheet(response.text, filename+"Gemini", song_data["bpm"], model)

# noinspection PyTypeChecker
def general_ai(model, filename, type_, platform):
    try:
        client = OpenAI(
            api_key=GlobalVariable.general_ai[platform]["key"],
            base_url=GlobalVariable.general_ai[platform]["url"]
        )

        # 加载原始乐谱
        song_data = loadSheetFile(type_, filename)
        target_length = len(song_data["songNotes"])

        # 准备初始提示词
        contents = GlobalVariable.duration_prompt if model == 'duration' else GlobalVariable.translate_prompt
        # 初始化消息上下文
        messages = [
            {"role": "system", "content": contents},
            {"role": "user", "content": json.dumps(song_data["songNotes"])},
        ]

        # 初始化状态变量
        full_objects = []
        max_retry = 20
        retry_count = 0
        total_segments = None
        current_segment = 1

        print("🎼 开始生成 JSON 音符数据...")

        while retry_count < max_retry:
            # 向模型发起请求
            response = client.chat.completions.create(
                model=GlobalVariable.general_ai[platform]["model"],
                messages=messages,
                stream=True,
            )

            # 逐步拼接响应内容
            partial = ""
            for chunk in response:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        partial += delta.content
                        print(delta.content, end="", flush=True)

            # 提取段落信息
            seg_cur, seg_tot = parse_segment_info(partial)
            if seg_cur and seg_tot:
                current_segment = seg_cur
                total_segments = seg_tot
                allow_extra_retry = 5
                max_retry = total_segments + allow_extra_retry
                retry_count = current_segment
                print(f"\n🔍 当前第 {current_segment} 段 / 共 {total_segments} 段")

            # 提取 JSON 对象
            new_objs = re.findall(r'\{[^{}]*?"time"\s*:\s*\d+[^{}]*?\}', partial)
            full_objects.extend(new_objs)
            print(f"\n📦 已收集 JSON 元素数：{len(full_objects)} / 目标 {target_length}")

            # ✅ 判断是否完成（段数或数量）
            if (total_segments and current_segment >= total_segments) or len(full_objects) >= target_length:
                json_text = f"[{','.join(full_objects)}]"
                saveSheetFile(json_text, filename + platform, song_data["bpm"], model)
                print("✅ JSON 输出已完成，已保存")
                return "ok"

            # 🚫 若未完成，续问 —— 精简上下文避免 token 超限
            retry_count += 1
            print(f"⚠️ 第 {current_segment} 段未完成，开始第 {retry_count} 次续问...")

            messages = [
                {"role": "system", "content": contents},
                {"role": "user", "content": json.dumps(song_data["songNotes"])},
                {"role": "assistant", "content": partial},
                {"role": "user", "content": "请继续上次未完成的 JSON 输出。"}
            ]

        print("❌ 达到最大重试次数，输出失败")
        return "output incomplete"

    except Exception as e:
        print("❗ 异常：", e)
        return "Nothing to do"

def parse_segment_info(text):
    """
    解析格式如“第 N 段（共预计 M 段）”，返回 (N, M)
    """
    pattern = r'第\s*(\d+)\s*段（共预计\s*(\d+)\s*段）'
    match = re.search(pattern, text)
    if match:
        current_segment = int(match.group(1))
        total_segments = int(match.group(2))
        return current_segment, total_segments
    return None, None

def match_to_sheet(text, filename, bpm, model):
    start_idx = text.find('[')
    end_idx = text.rfind(']')

    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        return "error"

    json_str = text[start_idx:end_idx + 1]

    try:
        parsed = json.loads(json_str)
        if isinstance(parsed, list) and len(parsed) >= 20:
            print("✅ 成功解析 JSON 数组，长度：", len(parsed))
            saveSheetFile(json.dumps(parsed), filename, bpm, model)
            return "ok"
        else:
            return "error"
    except json.JSONDecodeError as e:
        print("⚠️ JSON 解码失败:", e)
        return "error"


def loadSheetFile(type, fileName):
    # 优化了文件路径构建
    file_path = os.path.join(getResourcesPath(type), fileName + ".txt")
    with open(file_path, 'r', encoding=detect_encoding(file_path)) as file:
        data = json.load(file)
    song_notes = data[0].get("songNotes", [])
    bpm = data[0].get("bpm", [])
    if not song_notes:
        return []
    return {
        "songNotes": song_notes,
        "bpm": bpm
    }

def saveSheetFile(song_notes, fileName, bpm, model):
    if isinstance(song_notes, str):
        song_notes = json.loads(song_notes)
    output_file_name = fileName + "_AIGC_Handler_"+ ("延音" if model == "duration" else "间隔优化")
    output = [{
        "name": output_file_name,
        "author": "skyMusic-WindHide",
        "transcribedBy": "WindHide's Software",
        "bpm": bpm,
        "bitsPerPage": 15,
        "pitchLevel": 0,
        "isComposed": True,
        "songNotes": song_notes,
        "isEncrypted": False,
    }]
    file_output_path =os.path.join(getResourcesPath("myTranslate"), f"{output_file_name}.txt")
    with open(file_output_path, 'w') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

