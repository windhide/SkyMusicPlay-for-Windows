import os


def getResourcesPath():
    nowPath = os.path.dirname(os.path.abspath(__file__))
    resourcesPath = os.path.join(os.path.dirname(os.path.dirname(nowPath)), 'resources')
    return resourcesPath

