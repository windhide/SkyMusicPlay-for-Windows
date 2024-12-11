@echo off
setlocal enabledelayedexpansion

:: 显示当前目录
echo %~dp0

:: 构建 Electron 应用
cd %~dp0sky-music-web
call npm run electron:build

:: 构建 Python 服务器
cd %~dp0sky-music-server
call .venv\Scripts\activate
call pyinstaller --uac-admin -w sky-music-server.py --distpath %~dp0sky-music-web\dist_electron\win-unpacked\backend_dist --hidden-import=main
call deactivate

:: 复制 ffmpeg 可执行文件
copy %~dp0ffmpeg.exe %~dp0sky-music-web\dist_electron\win-unpacked\backend_dist\sky-music-server\ffmpeg.exe

:: 设置源路径和目标路径
set source="%~dp0template-resources"
set destination="%~dp0sky-music-web\dist_electron\win-unpacked\resources"

echo 正在复制文件夹...
robocopy %source% %destination% /E /Z /COPYALL /R:3 /W:5
:: 删除目标文件夹下所有的 .gitkeep 文件
echo 正在删除目标文件夹中的 .gitkeep 文件...
for /r %destination% %%f in (*.gitkeep) do (
    del /f /q "%%f"
)
echo 文件夹复制并清理完成！


echo.
echo 文件复制完成！
pause
