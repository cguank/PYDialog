@echo off
chcp 65001 >nul
title Windows可执行文件构建工具

echo ================================================
echo 弹窗处理程序 - Windows可执行文件构建工具
echo ================================================
echo.

REM 检查Python
echo [1/5] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python环境正常

REM 安装依赖
echo.
echo [2/5] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 安装PyInstaller
echo.
echo [3/5] 安装PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ❌ PyInstaller安装失败
    pause
    exit /b 1
)

REM 清理旧文件
echo.
echo [4/5] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
if exist *.spec del *.spec

REM 构建可执行文件
echo.
echo [5/5] 构建可执行文件...
echo 这可能需要几分钟时间，请耐心等待...
echo.

pyinstaller ^
    --onefile ^
    --console ^
    --add-data "imgs;imgs" ^
    --add-data "utils.py;." ^
    --hidden-import cv2 ^
    --hidden-import pyautogui ^
    --hidden-import numpy ^
    --hidden-import PIL ^
    --hidden-import PIL._tkinter_finder ^
    --hidden-import tkinter ^
    --hidden-import pyscreeze ^
    --hidden-import pytweening ^
    --hidden-import mouseinfo ^
    --hidden-import keyboard ^
    --hidden-import pygetwindow ^
    --hidden-import pyrect ^
    --name dialog_handler ^
    dialog_handler.py

if errorlevel 1 (
    echo.
    echo ❌ 构建失败！
    echo 请检查错误信息并重试
    pause
    exit /b 1
)

echo.
echo ================================================
echo ✅ 构建成功！
echo ================================================
echo.

REM 检查生成的文件
if exist dist\dialog_handler.exe (
    for %%A in (dist\dialog_handler.exe) do (
        set /a size=%%~zA/1024/1024
        echo 📁 生成的文件:
        echo    - dist\dialog_handler.exe (主程序)
        echo    - 文件大小: !size! MB
    )
    
    echo.
    echo 📋 使用说明:
    echo 1. 将 dist 文件夹中的所有文件复制到目标机器
    echo 2. 确保 imgs 文件夹包含弹窗模板图片
    echo 3. 双击 dialog_handler.exe 运行程序
    echo 4. 按 Ctrl+C 停止程序
    echo.
    echo ⚠️  注意事项:
    echo - 程序可能需要管理员权限
    echo - 某些杀毒软件可能会误报
    echo - 确保防火墙允许程序运行
    echo.
    
    REM 询问是否打开文件夹
    set /p choice="是否打开dist文件夹？(y/n): "
    if /i "!choice!"=="y" (
        explorer dist
    )
) else (
    echo ❌ 可执行文件未生成
)

echo.
echo 按任意键退出...
pause >nul 