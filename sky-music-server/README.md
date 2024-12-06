打包指令
```shell
# 有命令调试打包
pyinstaller --uac-admin sky_windows_music.py --distpath D:\Desktop\SkyMusicPlay-for-Windows\sky-music-web\dist_electron\win-unpacked\backend_dist --hidden-import=main
# 无命令调试打包
pyinstaller --uac-admin -w sky_windows_music.py --distpath D:\Desktop\SkyMusicPlay-for-Windows\sky-music-web\dist_electron\win-unpacked\backend_dist --hidden-import=main
```

> ffmpeg.exe 放在和 sky_windows_music.exe平级