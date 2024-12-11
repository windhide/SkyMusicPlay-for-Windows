echo  %~dp0
echo 打包前端
cd %~dp0sky-music-web
npm run electron:build
echo 前端打包完成

echo 打包后端
cd %~dp0sky-music-server
pyinstaller --uac-admin -w sky-music-server.py --distpath %~dp0sky-music-web\dist_electron\win-unpacked\backend_dist --hidden-import=main
copy %~dp0ffmpeg.exe %~dp0sky-music-web\dist_electron\win-unpacked\backend_dist\sky-music-server\ffmpeg.exe
echo 后端打包完成

echo 打包资源文件
@echo off
set source="%~dp0template-resources"
set destination="%~dp0sky-music-web\dist_electron\win-unpacked\resources"
xcopy %source% %destination% /E /H /C /I /Q /Y
echo 打包资源文件打包完成
pause