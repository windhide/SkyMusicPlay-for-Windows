import os

import demucs.separate

if __name__ == '__main__':
    # demucs.separate.main(shlex.split(
    #     '--flac --two-stems vocals -n mdx_extra "D:\\Desktop\\Josh Fudge - Second Date.flac"'
    #     '-o "D:\\Desktop"'
    # ))
    os.environ['TORCH_HOME'] = r'D:\\Desktop\\SkyMusicPlay-for-Windows\\template-resources\\systemTools\\modelData'
    demucs.separate.main([
        "D:\\Desktop\\Josh Fudge - Second Date.flac"
    ])
