import difflib
import hashlib
import os
import shutil
from collections import defaultdict


def get_file_hash(file_path, block_size=65536):
    """计算文件的 SHA-256 哈希值"""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(block_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_file_similarity(file1, file2):
    """计算两个文件的内容相似度"""
    with open(file1, 'r', errors='ignore') as f1, open(file2, 'r', errors='ignore') as f2:
        text1 = f1.readlines()
        text2 = f2.readlines()
    return difflib.SequenceMatcher(None, text1, text2).ratio()


def find_similar_files(input_folder, threshold=0.8):
    """查找相似文件并标记需要删除的文件"""
    files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if
             os.path.isfile(os.path.join(input_folder, f))]

    # 用哈希分组
    hash_groups = defaultdict(list)

    for file in files:
        file_hash = get_file_hash(file)
        hash_groups[file_hash].append(file)

    to_delete = set()
    checked_pairs = set()

    for group in hash_groups.values():
        # 如果 MD5 相同的文件超过 1 个，则这些都属于重复文件
        if len(group) > 1:
            # 保留最大（或最老）的一个，其余删除
            group_sorted = sorted(group, key=lambda f: os.path.getsize(f), reverse=True)
            keep = group_sorted[0]
            duplicates = group_sorted[1:]
            to_delete.update(duplicates)
            continue

        # 其它情况下才继续相似度比对（不同 hash）
        for i, file1 in enumerate(group):
            for file2 in group[i + 1:]:
                if (file1, file2) in checked_pairs:
                    continue
                checked_pairs.add((file1, file2))

                similarity = get_file_similarity(file1, file2)

                if similarity >= threshold:
                    smaller_file = min(file1, file2, key=lambda f: os.path.getsize(f))
                    to_delete.add(smaller_file)

    return to_delete


def process_files(input_folder, output_folder, threshold=0.8):
    """处理文件夹，删除重复文件并移动剩余文件"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    to_delete = find_similar_files(input_folder, threshold)

    # 删除重复文件
    deleted_files = list(to_delete)
    for file in to_delete:
        os.remove(file)

    # 移动剩余文件
    for file in os.listdir(input_folder):
        full_path = os.path.join(input_folder, file)
        if os.path.isfile(full_path):
            shutil.move(full_path, os.path.join(output_folder, file))

    print(f"删除了 {len(deleted_files)} 个文件：")
    for file in deleted_files:
        print(file)


if __name__ == "__main__":
    input_folder = r"D:\Desktop\处理好的"  # 输入文件夹路径
    output_folder = r"D:\Desktop\二次处理的"  # 处理后正常输出路径
    process_files(input_folder, output_folder)
