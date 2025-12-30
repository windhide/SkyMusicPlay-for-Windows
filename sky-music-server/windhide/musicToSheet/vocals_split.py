import os
import shutil

import demucs.separate

from windhide.utils.path_util import getResourcesPath

def split_vocals(musicFilePath):
    ffmpeg_dir = os.path.join(getResourcesPath("systemTools"), "ffmpeg")

    if not os.path.exists(os.path.join(ffmpeg_dir, "ffmpeg.exe")):
        raise RuntimeError("FFmpeg 未找到，请确认路径正确")
    # 注入 PATH
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

    os.environ['TORCH_HOME'] = os.path.join(getResourcesPath("systemTools"), "modelData")
    demucs.separate.main([
        "--flac",
        "--two-stems",
        "vocals",
        "-o", getResourcesPath("splitMusic"),
        "-n", "mdx_extra",
        musicFilePath
    ])
    # 转换完成后
    # 文件移动到translateOriginalMusic
    filename = musicFilePath.split("\\")[-1].split(".")[0]
    os.path.join(getResourcesPath("splitMusic"), "mdx_extra", filename)
    no_vocals_path = os.path.join(getResourcesPath("splitMusic"), "mdx_extra", filename, "no_vocals.flac")
    vocals_path = os.path.join(getResourcesPath("splitMusic"), "mdx_extra", filename, "vocals.flac")
    # 移动文件
    targetFolder = getResourcesPath("translateOriginalMusic")
    shutil.move(no_vocals_path, f"{targetFolder}/{filename + '_beat.flac'}")
    shutil.move(vocals_path, f"{targetFolder}/{filename + '_vocals.flac'}")
    shutil.rmtree(os.path.join(getResourcesPath("splitMusic"), "mdx_extra", filename))  # 删除子文件夹
