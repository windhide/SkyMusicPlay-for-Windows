import os
import json
import chardet  # 用于检测文件编码


def process_files(input_folder, output_folder, keyword="1Key"):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 初始化重复文件计数器
    duplicate_count = 0

    # 遍历输入文件夹下的所有文件
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)

        # 跳过非文件的对象
        if not os.path.isfile(file_path):
            continue

        try:
            # 自动检测文件编码
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                detected = chardet.detect(raw_data)
                encoding = detected.get('encoding', 'utf-8')

            # 用检测到的编码读取文件
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()

            # 检查是否包含关键词
            if keyword not in content:
                continue

            # 尝试将文件内容解析为 JSON 数组
            json_data = json.loads(content)
            if isinstance(json_data, list) and len(json_data) > 0:
                first_name = json_data[0].get('name')
                if first_name:
                    # 重命名文件并更改后缀
                    new_file_name = f"{first_name}.txt"
                    new_file_path = os.path.join(output_folder, new_file_name)

                    # 检查目标文件是否已经存在
                    if os.path.exists(new_file_path):
                        duplicate_count += 1  # 记录重复文件的覆盖

                    # 将内容转换为 UTF-8 并保存（直接覆盖同名文件）
                    with open(new_file_path, 'w', encoding='utf-8') as new_file:
                        new_file.write(content)

                    print(f"文件 {file_name} 已重命名并保存为 {new_file_path}")
        except (json.JSONDecodeError, KeyError, IOError, UnicodeDecodeError) as e:
            print(f"处理文件 {file_name} 时出错: {e}")

    # 输出重复文件计数
    print(f"共有 {duplicate_count} 个文件因重名被覆盖。")


if __name__ == '__main__':
    # 示例用法
    input_folder = "D:\\Desktop\\music\\original"  # 输入文件夹路径
    output_folder = "D:\\Desktop\\music\\out"  # 输出文件夹路径
    process_files(input_folder, output_folder)
