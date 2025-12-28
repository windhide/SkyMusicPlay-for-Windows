# =========================
# 自动管理员提权
# =========================
$principal = New-Object Security.Principal.WindowsPrincipal(
    [Security.Principal.WindowsIdentity]::GetCurrent()
)

if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "This script requires administrator privileges."
    Write-Host "Attempting to restart with administrator rights..."

    Start-Process powershell `
        -Verb RunAs `
        -ArgumentList "-NoExit -ExecutionPolicy Bypass -File `"$PSCommandPath`""

    exit
}

# =========================
# 脚本所在目录
# =========================
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

Write-Host "Current script directory: $ScriptDir"

# =========================
# 删除旧构建目录
# =========================
$pathsToRemove = @(
    "$ScriptDir\sky-music-web\dist",
    "$ScriptDir\sky-music-server\build",
    "$ScriptDir\sky-music-web\backend_dist"
)

foreach ($path in $pathsToRemove) {
    if (Test-Path $path) {
        Write-Host "Removing: $path"
        Remove-Item -Recurse -Force -Path $path
    }
}

# =========================
# 构建 Python 服务器
# =========================
Write-Host "`n=== Building Python Server ==="

Set-Location "$ScriptDir\sky-music-server"

& ".\.venv\Scripts\python.exe" -m PyInstaller `
    -i icon.ico `
    sky_music_server.py `
    --distpath "$ScriptDir\sky-music-web\backend_dist" `
    --version-file "$ScriptDir\sky-music-server\version.txt" `
    --hidden-import main `
    --collect-all sklearn `
    --collect-all basic_pitch `
    --collect-all plyer `
    --uac-admin

if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller build failed."
    exit 1
}

# =========================
# 复制 ffmpeg.exe
# =========================
Write-Host "`nCopying ffmpeg.exe"

$ffmpegSrc = "$ScriptDir\ffmpeg.exe"
$ffmpegDst = "$ScriptDir\sky-music-web\backend_dist\sky_music_server\ffmpeg.exe"

if (Test-Path $ffmpegSrc) {
    Copy-Item $ffmpegSrc $ffmpegDst -Force
} else {
    Write-Warning "ffmpeg.exe not found: $ffmpegSrc"
}

# =========================
# 构建 Electron 应用
# =========================
Write-Host "`n=== Building Electron App ==="

Set-Location "$ScriptDir\sky-music-web"

& npm run build:win

if ($LASTEXITCODE -ne 0) {
    Write-Error "Electron build failed."
    exit 1
}

# =========================
# 完成提示
# =========================
Write-Host "`nAll tasks completed successfully!"
Pause
