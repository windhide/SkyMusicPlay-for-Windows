import json
import os
import re
import shutil  # 用于移动文件
from concurrent.futures import ThreadPoolExecutor

import chardet  # 用于检测文件编码


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    return re.sub(r'[<>:"/\\\\|?*]', '_', name)


def process_file(file_path, normal_output_folder, encrypted_folder, keyword="1Key"):
    try:
        # 自动检测文件编码
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            detected = chardet.detect(raw_data)
            encoding = detected.get('encoding', 'utf-8') or 'utf-8'  # 避免 None

        # 用检测到的编码读取文件
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()

        # 解析 JSON
        try:
            json_data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"❌ 解析 JSON 失败: {file_path}, 错误: {e}")
            return

        # 确保 JSON 是列表并且不为空
        if not isinstance(json_data, list) or len(json_data) == 0:
            print(f"❌ 无效的 JSON 结构: {file_path}")
            return

        # **检查是否包含关键词 "1Key"**
        if keyword in content:
            first_name = json_data[0].get('name', '未命名文件')
            sanitized_name = sanitize_filename(first_name)
            new_file_name = f"{sanitized_name}.txt"
            new_file_path = os.path.join(normal_output_folder, new_file_name)

            # 避免文件名冲突
            counter = 1
            while os.path.exists(new_file_path):
                new_file_name = f"{sanitized_name}_{counter}.txt"
                new_file_path = os.path.join(normal_output_folder, new_file_name)
                counter += 1

            # **将内容转换为 UTF-8 并保存**
            with open(new_file_path, 'w', encoding='utf-8') as new_file:
                new_file.write(content)

            print(f"✅ 文件 {os.path.basename(file_path)} 已重命名并保存到 {normal_output_folder}")
            return

        # **检查是否包含 isEncrypted: true**
        for item in json_data:
            if isinstance(item, dict) and item.get("isEncrypted") is True:
                # **直接移动文件到加密文件夹**
                shutil.move(file_path, os.path.join(encrypted_folder, os.path.basename(file_path)))
                print(f"✅ 文件 {os.path.basename(file_path)} 已移动到 {encrypted_folder}")
                return

        # **如果既不是加密文件，也不包含关键词 "1Key"，则跳过**
        print(f"⚠️ 文件 {os.path.basename(file_path)} 不包含 'isEncrypted': true 或 '{keyword}'，跳过处理")

    except (KeyError, IOError, UnicodeDecodeError) as e:
        print(f"❌ 处理文件 {os.path.basename(file_path)} 时出错: {e}")


def process_files(input_folder, normal_output_folder, encrypted_folder, keyword="1Key"):
    # **确保目标文件夹存在**
    os.makedirs(normal_output_folder, exist_ok=True)
    os.makedirs(encrypted_folder, exist_ok=True)

    # **使用线程池并行处理文件**
    with ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(input_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                executor.submit(process_file, file_path, normal_output_folder, encrypted_folder, keyword)

    print("✅ 所有文件处理完成。")


if __name__ == '__main__':
    # **文件夹路径**
    input_folder = "D:\\Desktop\\WuHaoYe\\crack sheet\\original"  # 输入文件夹路径
    normal_output_folder = "D:\\Desktop\\WuHaoYe\\crack sheet\\crack"  # 处理后正常输出路径
    encrypted_folder = "D:\\Desktop\\WuHaoYe\\crack sheet\\encrypted"  # 加密文件存放路径

    process_files(input_folder, normal_output_folder, encrypted_folder)
