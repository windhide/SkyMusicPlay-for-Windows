import os

import demucs.separate
import shlex

if __name__ == '__main__':
    # demucs.separate.main(shlex.split(
    #     '--flac --two-stems vocals -n mdx_extra "D:\\Desktop\\Josh Fudge - Second Date.flac"'
    #     '-o "D:\\Desktop"'
    # ))
    os.environ['TORCH_HOME'] = r'D:\\Desktop\\SkyMusicPlay-for-Windows\\template-resources\\systemTools\\modelData'
    demucs.separate.main([
        "--flac",
        "--two-stems",
        "vocals",
        "-o", "D:\\Desktop",
        "-n", "mdx_extra",
        "D:\\Desktop\\Josh Fudge - Second Date.flac"
    ])
