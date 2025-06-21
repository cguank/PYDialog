@echo off
chcp 65001 >nul
echo ================================================
echo Windows可执行文件打包工具
echo ================================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 安装PyInstaller
echo 正在安装PyInstaller...
pip install pyinstaller

REM 清理之前的构建
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

REM 构建可执行文件
echo 开始构建Windows可执行文件...
pyinstaller --onefile --console --add-data "imgs;imgs" --add-data "utils.py;." --hidden-import cv2 --hidden-import pyautogui --hidden-import numpy --hidden-import PIL --hidden-import PIL._tkinter_finder --hidden-import tkinter --hidden-import pyscreeze --hidden-import pytweening --hidden-import mouseinfo --hidden-import keyboard --hidden-import pygetwindow --hidden-import pyrect --name dialog_handler dialog_handler.py

if errorlevel 1 (
    echo ❌ 构建失败
    pause
    exit /b 1
)

echo.
echo ✅ 构建成功！
echo.
echo 📁 生成的文件:
echo   - dist\dialog_handler.exe (主程序)
echo.
echo 🚀 部署说明:
echo 1. 将 dist 文件夹中的所有文件复制到目标Windows机器
echo 2. 确保 imgs 文件夹包含弹窗模板图片
echo 3. 双击 dialog_handler.exe 运行程序
echo.

REM 显示文件大小
if exist dist\dialog_handler.exe (
    for %%A in (dist\dialog_handler.exe) do echo 文件大小: %%~zA 字节
)

pause 