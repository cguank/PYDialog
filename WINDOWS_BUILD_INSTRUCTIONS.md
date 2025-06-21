# Windows可执行文件构建详细说明

## 重要说明
⚠️ **注意**: 在macOS/Linux上无法直接生成Windows可执行文件。您需要在Windows环境下进行构建。

## 构建方法

### 方法一：在Windows环境下构建（推荐）

#### 1. 环境准备
在Windows机器上安装：
- Python 3.7 或更高版本
- 所有依赖包

```cmd
# 安装依赖
pip install -r requirements.txt
pip install pyinstaller
```

#### 2. 文件准备
将以下文件复制到Windows机器：
- `dialog_handler.py`
- `utils.py`
- `imgs/` 文件夹
- `build_simple.py` 或 `build.bat`

#### 3. 执行构建

**使用Python脚本：**
```cmd
python build_simple.py
```

**使用批处理文件：**
```cmd
build.bat
```

**手动构建：**
```cmd
pyinstaller --onefile --console --add-data "imgs;imgs" --add-data "utils.py;." --hidden-import cv2 --hidden-import pyautogui --hidden-import numpy --hidden-import PIL --hidden-import PIL._tkinter_finder --hidden-import tkinter --hidden-import pyscreeze --hidden-import pytweening --hidden-import mouseinfo --hidden-import keyboard --hidden-import pygetwindow --hidden-import pyrect --name dialog_handler dialog_handler.py
```

### 方法二：使用Docker构建（跨平台）

#### 1. 创建Dockerfile
```dockerfile
FROM python:3.9-windowsservercore

WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install -r requirements.txt
RUN pip install pyinstaller

# 构建可执行文件
RUN pyinstaller --onefile --console --add-data "imgs;imgs" --add-data "utils.py;." --hidden-import cv2 --hidden-import pyautogui --hidden-import numpy --hidden-import PIL --hidden-import PIL._tkinter_finder --hidden-import tkinter --hidden-import pyscreeze --hidden-import pytweening --hidden-import mouseinfo --hidden-import keyboard --hidden-import pygetwindow --hidden-import pyrect --name dialog_handler dialog_handler.py

# 输出目录
VOLUME /app/dist
```

#### 2. 构建Docker镜像
```bash
docker build -t dialog-handler-builder .
```

#### 3. 运行容器并复制文件
```bash
docker run --rm -v $(pwd)/dist:/app/dist dialog-handler-builder
```

### 方法三：使用虚拟机

#### 1. 安装Windows虚拟机
- 下载Windows 10/11 ISO
- 使用VirtualBox或VMware创建虚拟机
- 安装Python和依赖

#### 2. 在虚拟机中构建
按照方法一的步骤在虚拟机中执行构建。

## 构建参数说明

### 主要参数
- `--onefile`: 打包成单个exe文件
- `--console`: 显示控制台窗口
- `--add-data`: 添加数据文件
- `--hidden-import`: 包含隐式导入的模块
- `--name`: 指定输出文件名

### 可选参数
- `--icon=icon.ico`: 添加程序图标
- `--windowed`: 不显示控制台窗口（GUI应用）
- `--onedir`: 打包成文件夹而不是单个文件
- `--exclude-module`: 排除不需要的模块

## 常见问题解决

### 1. 缺少依赖模块
如果遇到模块找不到的错误，添加 `--hidden-import` 参数：
```cmd
--hidden-import 模块名
```

### 2. 文件路径问题
确保使用正确的路径分隔符：
- Windows: `;`
- Linux/macOS: `:`

### 3. 权限问题
以管理员身份运行命令提示符。

### 4. 杀毒软件误报
- 将构建目录添加到白名单
- 或临时关闭实时保护

## 优化建议

### 减小文件大小
```cmd
pyinstaller --onefile --console --strip --upx-dir=upx --add-data "imgs;imgs" --add-data "utils.py;." --exclude-module matplotlib --exclude-module scipy dialog_handler.py
```

### 提高启动速度
```cmd
pyinstaller --onedir --console --add-data "imgs;imgs" --add-data "utils.py;." dialog_handler.py
```

## 测试部署

### 1. 本地测试
```cmd
cd dist
dialog_handler.exe
```

### 2. 目标机器测试
- 复制 `dist` 文件夹到目标Windows机器
- 确保 `imgs` 文件夹包含模板图片
- 双击 `dialog_handler.exe` 运行

### 3. 功能验证
- 检查屏幕截图功能
- 验证弹窗检测
- 测试鼠标点击功能

## 发布准备

### 1. 文件清单
```
发布包/
├── dialog_handler.exe    # 主程序
├── imgs/                 # 模板图片
│   └── *.jpg/png
├── README.txt           # 使用说明
└── install.bat          # 安装脚本（可选）
```

### 2. 压缩打包
```cmd
# 使用7-Zip压缩
7z a dialog_handler_windows.zip dist/*

# 或使用WinRAR
winrar a dialog_handler_windows.rar dist/*
```

### 3. 数字签名（可选）
```cmd
# 使用代码签名证书
signtool sign /f certificate.pfx /p password dialog_handler.exe
```

## 技术支持

如果遇到构建问题：
1. 检查Python版本和依赖
2. 查看PyInstaller日志
3. 尝试简化构建参数
4. 在干净的虚拟环境中测试 