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
rmdir /S /Q "%script_dir%sky-music-web\backend_dist"

:: 构建 Python 服务器
cd "%script_dir%sky-music-server"
call .venv\Scripts\activate
call pyinstaller --uac-admin -w sky-music-server.py --distpath "%script_dir%sky-music-web\backend_dist" --hidden-import=main --collect-all=sklearn --collect-all=demucs
call deactivate

:: 构建 Electron 应用
cd "%script_dir%sky-music-web"
call npm run build:win

:: 完成提示
echo.
echo All tasks completed successfully!
pause
