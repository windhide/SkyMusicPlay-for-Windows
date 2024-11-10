import os

from utils.pathUtils import getResourcesPath


def getTypeMusicList(type):
    resources_dir = os.path.join(getResourcesPath() , type)
    file_names = [file for file in os.listdir(resources_dir) if os.path.isfile(os.path.join(resources_dir, file))]
    file_names_array = []
    for item in file_names:
        file_names_array.append({"name": item.replace(".txt", "")})
    return file_names_array
