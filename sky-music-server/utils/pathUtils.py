import os


def getResourcesPath(file):
    nowPath = os.path.dirname(os.path.abspath(__file__))
    if file is None:
        resources_path = os.path.join(os.path.dirname(os.path.dirname(nowPath)), 'resources')
    else:
        resources_path = os.path.join(os.path.dirname(os.path.dirname(nowPath)), 'resources', file)
    return resources_path
