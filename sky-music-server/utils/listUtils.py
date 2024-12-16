import os

from utils.pathUtils import getResourcesPath


def getTypeMusicList(type,searchStr = None):
    resources_dir = os.path.join(getResourcesPath(None) , type)
    file_names = [file for file in os.listdir(resources_dir) if os.path.isfile(os.path.join(resources_dir, file))]
    file_names_array = []
    print("searchStr",searchStr)
    if searchStr is not None and searchStr != '' and searchStr != ' ':
        for item in [item for item in file_names if searchStr.lower() in item.lower()]:
            file_names_array.append({"name": item.replace(".txt", "")})
    else:
        for item in file_names:
            file_names_array.append({"name": item.replace(".txt", "")})

    return file_names_array