打包指令
```shell
# 有命令调试打包
pyinstaller --uac-admin sky_music_server.py -i icon.ico --upx-dir D:\Desktop\upx-4.2.2-win64\ --distpath D:\Desktop\SkyMusicPlay-for-Windows\sky-music-web\dist\win-unpacked\backend_dist --hidden-import=main --collect-all=sklearn --collect-all=basic_pitch
# 无命令调试打包
pyinstaller --uac-admin -w sky_music_server.py -i icon.ico --upx-dir D:\Desktop\upx-4.2.2-win64\ --distpath D:\Desktop\SkyMusicPlay-for-Windows\sky-music-web\dist\win-unpacked\backend_dist --hidden-import=main --collect-all=sklearn --collect-all=basic_pitch
```
> ffmpeg.exe 放在和 sky_windows_music.exe平级