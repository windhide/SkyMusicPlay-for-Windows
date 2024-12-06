import os

def getResourcesPath(file):
    nowPath = os.path.dirname(os.path.abspath(__file__))
    resources_path = os.path.dirname(os.path.dirname(nowPath))
    target_subpath = os.path.join("backend_dist", "sky_windows_music")
    if target_subpath in resources_path:
        resources_path = os.path.abspath(os.path.join(resources_path, "..", ".."))

    if file is None:
        return os.path.join(resources_path, 'resources')
    else:
        return os.path.join(resources_path, 'resources', file)
