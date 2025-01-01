import os
import json
import chardet  # 用于检测文件编码
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# 初始化全局计数器和锁
duplicate_count = 0
lock = Lock()

def process_file(file_path, output_folder, keyword="1Key"):
    global duplicate_count

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
            return

        # 尝试将文件内容解析为 JSON 数组
        json_data = json.loads(content)
        if isinstance(json_data, list) and len(json_data) > 0:
            first_name = json_data[0].get('name')
            if first_name:
                # 重命名文件并更改后缀
                new_file_name = f"{first_name}.txt"
                new_file_path = os.path.join(output_folder, new_file_name)

                # 检查目标文件是否已经存在并更新计数器
                with lock:
                    if os.path.exists(new_file_path):
                        duplicate_count += 1

                # 将内容转换为 UTF-8 并保存（直接覆盖同名文件）
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(content)

                print(f"文件 {os.path.basename(file_path)} 已重命名并保存为 {new_file_path}")
    except (json.JSONDecodeError, KeyError, IOError, UnicodeDecodeError) as e:
        print(f"处理文件 {os.path.basename(file_path)} 时出错: {e}")

def process_files(input_folder, output_folder, keyword="1Key"):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 获取所有文件路径
    file_paths = [os.path.join(input_folder, file_name) for file_name in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file_name))]

    # 使用线程池并发处理文件
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, file_path, output_folder, keyword) for file_path in file_paths]

        # 等待所有线程完成
        for future in futures:
            future.result()

    # 输出重复文件计数
    print(f"共有 {duplicate_count} 个文件因重名被覆盖。")

if __name__ == '__main__':
    # 示例用法
    input_folder = "D:\\Desktop\\music\\original"  # 输入文件夹路径
    output_folder = "D:\\Desktop\\music\\out"  # 输出文件夹路径
    process_files(input_folder, output_folder)
