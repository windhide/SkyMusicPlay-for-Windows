@echo off

:: 保存脚本的原始路径
set script_dir=%~dp0

:: 检查是否以管理员身份运行
powershell -Command "if (-not ([Security.Principal.WindowsPrincipal]([Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { exit 1 }"
if %errorlevel% neq 0 (
    echo This script requires administrator privileges.
    echo Attempting to restart with administrator rights...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

:: 设置环境变量以支持延迟变量扩展
setlocal enabledelayedexpansion

:: 如果已是管理员权限，则继续执行脚本
echo Script successfully running as administrator!

:: 切换到脚本所在目录
cd /d "%script_dir%"

:: 显示当前目录
echo Current script directory: %script_dir%

:: 删除旧的 Electron 构建目录
rmdir /S /Q "%script_dir%sky-music-web\dist"
:: 删除python的构建目录
rmdir /S /Q "%script_dir%sky-music-server\build"

:: 构建 Electron 应用
cd "%script_dir%sky-music-web"
call npm run build:win

:: 构建 Python 服务器
cd "%script_dir%sky-music-server"
call .venv\Scripts\activate
call pyinstaller --uac-admin -w sky-music-server.py --distpath "%script_dir%sky-music-web\dist\win-unpacked\backend_dist" --hidden-import=main
call deactivate

:: 复制 ffmpeg 可执行文件
copy "%script_dir%ffmpeg.exe" "%script_dir%sky-music-web\dist\win-unpacked\backend_dist\sky-music-server\ffmpeg.exe"

:: 设置源路径和目标路径
set source="%script_dir%template-resources"
set destination="%script_dir%sky-music-web\dist\win-unpacked\resources"

:: 使用 robocopy 复制文件并保留属性
echo Copying files with robocopy...
robocopy %source% %destination% /E /Z /COPYALL /R:3 /W:5

:: 删除目标文件夹下的所有 .gitkeep 文件
echo Cleaning up .gitkeep files...
for /r "%destination%" %%f in (*.gitkeep) do (
    del /f /q "%%f"
)

echo File copy and cleanup completed!

:: 完成提示
echo.
echo All tasks completed successfully!
pause
