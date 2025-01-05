import os

from windhide.utils.path_util import getResourcesPath


def getTypeMusicList(type, searchStr=None):
    # 获取资源目录路径
    resources_dir = os.path.join(getResourcesPath(None), type)
    # 获取目录下所有文件名
    file_names = [
        file for file in os.listdir(resources_dir)
        if os.path.isfile(os.path.join(resources_dir, file)) and file != ".keep"
    ]    # 如果 searchStr 不为空，过滤包含 searchStr 的文件名，忽略大小写
    if searchStr and searchStr.strip():
        file_names = [file for file in file_names if searchStr.lower() in file.lower()]
    # 返回处理后的文件列表，去掉扩展名 .txt
    return [{"name": file.replace(".txt", "")} for file in file_names]
