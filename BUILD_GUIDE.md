# Windows可执行文件构建指南

## 概述
本指南将帮助您将Python弹窗处理程序打包成Windows可执行文件(.exe)。

## 方法一：使用Python脚本构建（推荐）

### 1. 环境准备
确保您的系统已安装：
- Python 3.7 或更高版本
- 所有依赖包（在requirements.txt中列出）

### 2. 运行构建脚本
```bash
# 方法1：使用简化脚本
python build_simple.py

# 方法2：使用完整脚本
python build_windows.py
```

### 3. 构建过程
脚本会自动：
- 检查必要文件
- 安装PyInstaller（如果需要）
- 清理之前的构建文件
- 执行打包命令
- 生成可执行文件

## 方法二：使用批处理文件构建（Windows）

### 1. 在Windows环境下
双击运行 `build.bat` 文件

### 2. 批处理文件会自动：
- 检查Python环境
- 安装PyInstaller
- 执行打包命令
- 显示构建结果

## 方法三：手动使用PyInstaller

### 1. 安装PyInstaller
```bash
pip install pyinstaller
```

### 2. 执行打包命令
```bash
pyinstaller --onefile --console --add-data "imgs;imgs" --add-data "utils.py;." --hidden-import cv2 --hidden-import pyautogui --hidden-import numpy --hidden-import PIL --hidden-import PIL._tkinter_finder --hidden-import tkinter --hidden-import pyscreeze --hidden-import pytweening --hidden-import mouseinfo --hidden-import keyboard --hidden-import pygetwindow --hidden-import pyrect --name dialog_handler dialog_handler.py
```

## 构建结果

### 生成的文件
- `dist/dialog_handler.exe` - 主程序可执行文件
- `dist/README.txt` - 使用说明

### 文件大小
通常生成的exe文件大小在50-100MB之间，具体取决于依赖包的大小。

## 部署说明

### 1. 文件结构
```
目标Windows机器/
├── dialog_handler.exe    # 主程序
├── imgs/                 # 弹窗模板图片文件夹
│   └── img1.jpg         # 模板图片
└── README.txt           # 使用说明
```

### 2. 运行程序
- 双击 `dialog_handler.exe` 运行程序
- 程序会自动监控屏幕上的弹窗
- 按 `Ctrl+C` 停止程序

### 3. 注意事项
- 确保 `imgs` 文件夹与exe文件在同一目录
- 程序可能需要管理员权限才能进行屏幕截图
- 某些杀毒软件可能会误报，需要添加信任
- 如果遇到问题，请检查防火墙设置

## 故障排除

### 常见问题

1. **构建失败**
   - 检查Python版本是否为3.7+
   - 确保所有依赖包已正确安装
   - 检查文件路径是否正确

2. **运行时错误**
   - 确保imgs文件夹存在且包含图片
   - 检查是否有足够的磁盘空间
   - 尝试以管理员身份运行

3. **杀毒软件误报**
   - 将程序添加到杀毒软件的白名单
   - 或临时关闭实时保护

4. **权限问题**
   - 以管理员身份运行程序
   - 检查Windows Defender设置

### 调试方法

1. **查看详细错误信息**
   - 在命令行中运行exe文件
   - 查看错误输出

2. **检查依赖**
   - 确保所有必要的DLL文件存在
   - 检查Python环境变量

3. **重新构建**
   - 清理build和dist目录
   - 重新运行构建脚本

## 优化建议

### 减小文件大小
- 使用 `--exclude-module` 排除不需要的模块
- 使用UPX压缩（PyInstaller默认启用）

### 提高启动速度
- 使用 `--onedir` 而不是 `--onefile`
- 优化导入语句

### 增强兼容性
- 在目标Windows版本上测试
- 检查依赖包的兼容性

## 技术支持

如果遇到问题，请：
1. 查看错误日志
2. 检查系统环境
3. 尝试重新构建
4. 联系技术支持 