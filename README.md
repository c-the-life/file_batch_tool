# 📁 文件批量处理工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-green.svg)](https://github.com/)

> 🎯 一款基于 PyQt5 的图形化文件批量处理工具，界面美观，操作简单，效率翻倍！

## ✨ 为什么选择我们？

⭐ **零学习成本** - 纯图形界面，无需命令行  
⚡ **效率提升 10 倍** - 一键批量处理 hundreds of files  
🔒 **安全可靠** - 原文件保护，处理结果生成新文件  
🎨 **界面美观** - 现代简约设计，视觉舒适  
📦 **功能全面** - 8大核心功能，覆盖办公高频场景  

## 📋 功能清单

| 功能模块 | 说明 |
|---------|------|
| 🏷️ **批量重命名** | 前缀/后缀、自动编号、单文件独立设置 |
| 🖼️ **图片格式转换** | JPG/PNG/WebP 互转，透明通道自动处理 |
| 📦 **文件压缩** | ZIP批量压缩，可排除指定类型 |
| 📂 **文件分类** | 按扩展名/日期自动归档 |
| 💧 **图片水印** | 文字水印/图片水印，自定义样式 |
| ⏰ **批量改时间** | 修改创建/修改时间 |
| 📊 **提取EXIF** | 导出图片元数据到CSV |
| 📥 **复制/移动** | 批量文件操作 |

## 🚀 快速开始

### 🎯 方式一：下载即用（推荐）
```bash
1. 下载最新 Release 版本
2. 双击运行，无需安装
3. 开始批量处理！
```

### 💻 方式二：源码运行
```bash
# 克隆项目
git clone https://gitee.com/the-life/file_batch_tool.git
cd file_batch_tool

# 安装依赖
pip install -r requirements.txt

# 运行程序
python file-batch-tool.py
```

## 📸 界面预览

![主界面](screenshots/main.png)

## 💡 使用示例

### 🏷️ 批量重命名
```
1. 选择文件/文件夹（拖拽也支持）
2. 设置前缀、后缀、自动编号
3. 点击"应用"完成
```

### 🖼️ 图片格式转换
```
1. 选择图片目录
2. 选择目标格式（JPG/PNG/WebP）
3. 一键转换，透明区域自动处理
```

## 🎯 核心优势

### 🔒 安全优先
- ✅ 原文件完全不修改、不覆盖
- ✅ 所有操作生成新文件
- ✅ 操作日志完整记录
- ✅ 异常操作自动跳过

### 🎨 用户体验
- ✅ 拖拽文件/文件夹直接处理
- ✅ 每个文件独立设置
- ✅ 批量选择多文件
- ✅ 实时日志反馈

### ⚡ 性能卓越
- ✅ 多线程后台处理
- ✅ 界面流畅不卡顿
- ✅ 支持大文件处理
- ✅ 智能跳过已存在文件

## 🛠️ 技术栈

| 分类 | 技术 | 用途 |
|------|------|------|
| 界面 | PyQt5 | GUI开发 |
| 图片 | Pillow | 格式转换/水印/EXIF |
| 文件 | pathlib, shutil | 跨平台文件操作 |
| 压缩 | zipfile | ZIP打包 |
| 时间 | datetime | 文件时间处理 |

## ⚠️ 注意事项

1. 💾 **重要文件先备份**，虽然我们有保护机制，但备份更安全
2. 📁 **支持拖拽**，直接将文件/文件夹拖入输入框
3. 🎯 **批量处理**时，界面会显示处理进度
4. 🔒 **权限问题**：确保程序有文件读写权限
5. 📦 **水印/转换**后的文件会自动添加标识前缀/后缀

## 🤝 贡献代码

欢迎提交 Issue 和 Pull Request！

## 📄 开源协议

MIT License - 可以自由使用、修改和分发

## 🎯 问题反馈

- 🐛 发现Bug？[提交Issue](https://gitee.com/the-life/file_batch_tool/issues)
- 💡 有好建议？[功能提议](https://gitee.com/the-life/file_batch_tool/issues)
- 📖 查看更新：[版本历史](https://gitee.com/the-life/file_batch_tool/releases)

---

**如果这个项目对你有帮助，请给个 ⭐ Star！**

