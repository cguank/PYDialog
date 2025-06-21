#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的Windows可执行文件打包脚本
"""

import os
import sys
import subprocess
import shutil

def main():
    """主函数"""
    print("=" * 50)
    print("Windows可执行文件打包工具")
    print("=" * 50)
    
    # 检查必要文件
    required_files = ['dialog_handler.py', 'utils.py', 'imgs']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            return
    
    # 安装PyInstaller（如果需要）
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 清理之前的构建
    for dir_name in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 构建命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # 打包成单个文件
        "--console",  # 显示控制台窗口
        "--add-data", "imgs:imgs",  # 包含图片文件夹
        "--add-data", "utils.py:.",  # 包含utils模块
        "--hidden-import", "cv2",
        "--hidden-import", "pyautogui",
        "--hidden-import", "numpy",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL._tkinter_finder",
        "--hidden-import", "tkinter",
        "--hidden-import", "pyscreeze",
        "--hidden-import", "pytweening",
        "--hidden-import", "mouseinfo",
        "--hidden-import", "keyboard",
        "--hidden-import", "pygetwindow",
        "--hidden-import", "pyrect",
        "--name", "dialog_handler",
        "dialog_handler.py"
    ]
    
    print("开始构建...")
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ 构建成功!")
        
        # 检查生成的文件
        exe_path = "dist/dialog_handler.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"可执行文件位置: {exe_path}")
            print(f"文件大小: {size_mb:.1f} MB")
            
            # 创建使用说明
            readme_content = """弹窗处理程序 - Windows版本

使用说明:
1. 双击 dialog_handler.exe 运行程序
2. 程序会自动监控屏幕上的弹窗
3. 按 Ctrl+C 停止程序

注意事项:
- 确保 imgs 文件夹与 exe 文件在同一目录
- 程序需要管理员权限才能进行屏幕截图
- 如果遇到问题，请检查防火墙设置

文件结构:
dialog_handler.exe  - 主程序
imgs/              - 弹窗模板图片文件夹
"""
            
            with open("dist/README.txt", "w", encoding="utf-8") as f:
                f.write(readme_content)
            
            print("\n📁 生成的文件:")
            print("  - dist/dialog_handler.exe (主程序)")
            print("  - dist/README.txt (使用说明)")
            
            print("\n🚀 部署说明:")
            print("1. 将 dist 文件夹中的所有文件复制到Windows机器")
            print("2. 确保 imgs 文件夹包含弹窗模板图片")
            print("3. 双击 dialog_handler.exe 运行程序")
            
        else:
            print("❌ 可执行文件未生成")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main() 