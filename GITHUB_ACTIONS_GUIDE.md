# GitHub Actions 自动构建指南

## 概述
使用GitHub Actions可以自动构建Windows可执行文件，无需本地Windows环境。这解决了跨平台构建的问题。

## 🚀 快速开始

### 1. 准备工作
确保您的项目包含以下文件：
```
项目根目录/
├── .github/workflows/
│   ├── build-windows.yml          # Windows构建工作流
│   └── build-multi-platform.yml   # 多平台构建工作流
├── dialog_handler.py              # 主程序
├── utils.py                       # 工具模块
├── requirements.txt               # 依赖列表
└── imgs/                          # 图片文件夹
```

### 2. 推送代码
将代码推送到GitHub仓库：
```bash
git add .
git commit -m "Add GitHub Actions workflows"
git push origin main
```

### 3. 查看构建结果
- 进入GitHub仓库页面
- 点击 "Actions" 标签页
- 查看构建进度和结果

## 📋 工作流说明

### 单平台构建 (build-windows.yml)
**触发条件：**
- 推送到 main/master 分支
- 创建 Pull Request
- 发布 Release
- 手动触发

**功能：**
- 仅在Windows环境下构建
- 生成Windows可执行文件
- 自动上传构建产物
- 创建发布包（Release时）

### 多平台构建 (build-multi-platform.yml)
**触发条件：**
- 推送到 main/master 分支
- 创建 Pull Request
- 发布 Release
- 手动触发（可选择平台）

**功能：**
- 支持Windows、macOS、Linux构建
- 可选择构建特定平台或全部平台
- 自动创建多平台发布包
- 生成统一的发布说明

## 🎯 使用方法

### 自动构建
1. **推送触发** - 每次推送到主分支时自动构建
2. **PR触发** - 创建Pull Request时进行构建测试
3. **Release触发** - 发布新版本时自动构建并上传

### 手动构建
1. 进入GitHub仓库的Actions页面
2. 选择要运行的工作流
3. 点击 "Run workflow"
4. 选择目标分支和平台（多平台构建）
5. 点击 "Run workflow" 开始构建

### 下载构建产物
1. 构建完成后，进入Actions页面
2. 点击成功的构建任务
3. 在 "Artifacts" 部分下载文件
4. 解压到本地使用

## 📦 构建产物

### Windows构建产物
```
dialog-handler-windows/
├── dialog_handler.exe    # Windows可执行文件
├── imgs/                 # 模板图片文件夹
├── README.txt           # 使用说明
└── dialog_handler_windows.zip  # 完整发布包
```

### 多平台构建产物
```
dialog-handler-windows/   # Windows版本
dialog-handler-macos/     # macOS版本
dialog-handler-linux/     # Linux版本
```

## 🔧 配置说明

### 环境变量
工作流使用以下环境变量：
- `GITHUB_TOKEN` - 自动提供的GitHub令牌
- `PYTHON_VERSION` - Python版本（默认3.9）

### 缓存配置
- **pip缓存** - 加速依赖安装
- **构建缓存** - 减少重复构建时间

### 构建参数
```yaml
pyinstaller参数:
  --onefile: 打包成单个文件
  --console: 显示控制台窗口
  --add-data: 包含数据文件
  --hidden-import: 包含隐式导入模块
  --name: 指定输出文件名
```

## 🚨 故障排除

### 常见问题

**Q: 构建失败怎么办？**
A: 
1. 检查Actions日志中的错误信息
2. 确保所有依赖文件存在
3. 验证requirements.txt格式正确
4. 检查Python版本兼容性

**Q: 构建产物下载失败？**
A:
1. 构建产物保留30天
2. 检查网络连接
3. 尝试重新运行构建

**Q: 文件大小异常？**
A:
1. 检查是否包含了不必要的依赖
2. 使用--exclude-module排除不需要的模块
3. 考虑使用--onedir而不是--onefile

### 调试方法

1. **查看详细日志**
   - 在Actions页面点击失败的步骤
   - 查看完整的错误输出

2. **本地测试**
   - 在本地Windows环境测试构建命令
   - 确保所有依赖正确安装

3. **简化构建**
   - 先使用简单的构建参数
   - 逐步添加复杂配置

## 📈 优化建议

### 构建速度优化
1. **使用缓存** - 充分利用pip和构建缓存
2. **并行构建** - 多平台构建可以并行执行
3. **精简依赖** - 只包含必要的Python包

### 文件大小优化
1. **排除模块** - 使用--exclude-module排除不需要的模块
2. **UPX压缩** - 启用UPX压缩（默认启用）
3. **分离构建** - 使用--onedir减少单个文件大小

### 兼容性优化
1. **Python版本** - 使用稳定的Python版本
2. **依赖版本** - 固定依赖包版本
3. **系统兼容** - 在目标系统上测试

## 🔄 持续集成

### 自动化流程
1. **代码推送** → 自动构建 → 生成产物
2. **PR创建** → 构建测试 → 验证功能
3. **Release发布** → 构建发布包 → 上传资源

### 质量保证
1. **构建测试** - 确保代码可以正常构建
2. **功能验证** - 在构建环境中测试基本功能
3. **兼容性检查** - 验证多平台兼容性

## 📝 最佳实践

### 代码管理
1. **版本控制** - 使用语义化版本号
2. **分支策略** - 使用main分支作为稳定版本
3. **提交信息** - 使用清晰的提交信息

### 构建管理
1. **定期构建** - 定期触发构建确保代码可用
2. **产物管理** - 及时清理过期的构建产物
3. **文档更新** - 保持构建说明文档的更新

### 发布管理
1. **Release策略** - 使用GitHub Release管理版本
2. **变更日志** - 维护详细的变更日志
3. **用户反馈** - 收集用户反馈并持续改进

## 🆘 获取帮助

### 官方资源
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [PyInstaller文档](https://pyinstaller.readthedocs.io/)
- [Python打包指南](https://packaging.python.org/)

### 社区支持
- GitHub Issues - 报告问题
- GitHub Discussions - 讨论功能
- Stack Overflow - 技术问答

### 联系支持
如果遇到问题：
1. 查看Actions日志
2. 搜索相似问题
3. 创建Issue报告
4. 联系项目维护者 