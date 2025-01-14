打包指令
```shell
# 有命令调试打包
pyinstaller --uac-admin sky-music-server.py --distpath D:\Desktop\SkyMusicPlay-for-Windows\sky-music-web\dist\win-unpacked\backend_dist --hidden-import=main --collect-all=sklearn
# 无命令调试打包
pyinstaller --uac-admin -w sky-music-server.py --distpath D:\Desktop\SkyMusicPlay-for-Windows\sky-music-web\dist\win-unpacked\backend_dist --hidden-import=main --collect-all=sklearn
```
> ffmpeg.exe 放在和 sky_windows_music.exe平级