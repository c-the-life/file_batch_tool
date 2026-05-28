# 文件批量处理工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-green.svg)](https://github.com/)
[![PyPI](https://img.shields.io/pypi/v/file-batch-tool.svg)](https://pypi.org/project/file-batch-tool/)

> 一款基于 PyQt5 的图形化文件批量处理工具，同时也可作为 Python 库被其他项目引用！

## 功能清单

| 功能模块 | 说明 |
|---------|------|
| **批量重命名** | 前缀/后缀、自动编号、单文件独立设置 |
| **图片格式转换** | JPG/PNG/WebP 互转，透明通道自动处理 |
| **文件压缩** | ZIP批量压缩，可排除指定类型 |
| **文件分类** | 按扩展名/日期自动归档 |
| **图片水印** | 文字水印/图片水印，自定义样式 |
| **批量改时间** | 修改创建/修改时间 |
| **提取EXIF** | 导出图片元数据到CSV |
| **复制/移动** | 批量文件操作 |

---

## 安装指南

### 系统要求

| 项目 | 要求 |
|------|------|
| Python | 3.8 或更高版本 |
| 操作系统 | Windows / Linux / macOS |
| 内存 | 建议 4GB 以上 |
| 磁盘 | 至少 100MB 可用空间 |

### 依赖说明

| 依赖包 | 版本要求 | 用途 | 必需 |
|--------|----------|------|------|
| **Pillow** | >= 10.0.0 | 图片处理（格式转换、水印、EXIF提取） | 是 |
| **PyQt5** | >= 5.15.0 | GUI图形界面 | 是 |

---

## 安装方法

### 方法一：从 PyPI 安装（推荐）

```bash
# 直接安装
pip install file-batch-tool

# 安装完成后，在命令行运行
file-batch-tool
```

### 方法二：从源码安装

#### 步骤 1：克隆项目

```bash
# 从 GitHub 克隆
git clone https://github.com/c-the-life/file_batch_tool.git

# 或从 Gitee 克隆（国内更快）
git clone https://gitee.com/the-life/file_batch_tool.git

# 进入项目目录
cd file_batch_tool
```

#### 步骤 2：创建虚拟环境（推荐）

**Windows:**
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 确认 Python 版本
python --version
```

**Linux / macOS:**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 确认 Python 版本
python --version
```

#### 步骤 3：安装依赖

```bash
# 升级 pip 到最新版本
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

**依赖安装详解：**

```bash
# 安装 Pillow（图片处理库）
pip install Pillow>=10.0.0

# 安装 PyQt5（GUI框架）
pip install PyQt5>=5.15.0
```

#### 步骤 4：运行程序

```bash
# 运行图形界面
python file-batch-tool.py
```

### 方法三：开发模式安装

```bash
# 克隆项目
git clone https://github.com/c-the-life/file_batch_tool.git
cd file_batch_tool

# 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# 以开发模式安装（修改代码后无需重新安装）
pip install -e .

# 运行程序
python file-batch-tool.py
```

---

## 详细安装步骤（Windows 用户）

### 1. 安装 Python

1. 访问 [Python 官网](https://www.python.org/downloads/) 下载 Python 3.8+
2. 运行安装程序，**勾选 "Add Python to PATH"**
3. 打开命令提示符，验证安装：
   ```bash
   python --version
   pip --version
   ```

### 2. 下载项目

```bash
# 方式1：使用 git
git clone https://gitee.com/the-life/file_batch_tool.git

# 方式2：直接下载 ZIP
# 访问 https://gitee.com/the-life/file_batch_tool
# 点击 "克隆/下载" -> "下载 ZIP"
```

### 3. 安装依赖

```bash
cd file_batch_tool
pip install -r requirements.txt
```

### 4. 运行程序

```bash
python file-batch-tool.py
```

---

## 详细安装步骤（Linux 用户）

### 1. 安装系统依赖

**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
# PyQt5 系统依赖
sudo apt install libgl1-mesa-glx libegl1 libxkbcommon-x11-0
```

**Fedora / CentOS:**
```bash
sudo dnf install python3 python3-pip python3-venv
sudo dnf install mesa-libGL mesa-libEGL libxkbcommon-x11
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装项目

```bash
git clone https://github.com/c-the-life/file_batch_tool.git
cd file_batch_tool
pip install -r requirements.txt
```

### 4. 运行程序

```bash
python file-batch-tool.py
```

---

## 详细安装步骤（macOS 用户）

### 1. 安装 Python（如未安装）

```bash
# 使用 Homebrew 安装
brew install python3
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装项目

```bash
git clone https://github.com/c-the-life/file_batch_tool.git
cd file_batch_tool
pip install -r requirements.txt
```

### 4. 运行程序

```bash
python file-batch-tool.py
```

---

## 常见安装问题

### 问题 1：pip 安装速度慢

**解决方案：使用国内镜像源**

```bash
# 临时使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久配置镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**常用国内镜像：**

| 镜像源 | 地址 |
|--------|------|
| 清华 | https://pypi.tuna.tsinghua.edu.cn/simple |
| 阿里云 | https://mirrors.aliyun.com/pypi/simple |
| 豆瓣 | https://pypi.douban.com/simple |
| 中科大 | https://pypi.mirrors.ustc.edu.cn/simple |

### 问题 2：PyQt5 安装失败

**Windows:**
```bash
# 尝试指定版本
pip install PyQt5==5.15.9

# 或使用 conda
conda install pyqt
```

**Linux:**
```bash
# 安装系统依赖后再试
sudo apt install libgl1-mesa-glx libegl1
pip install PyQt5
```

### 问题 3：Permission denied（权限不足）

```bash
# 使用 --user 参数安装到用户目录
pip install -r requirements.txt --user

# 或使用 sudo（Linux/macOS）
sudo pip install -r requirements.txt
```

### 问题 4：Python 版本不兼容

```bash
# 检查 Python 版本
python --version

# 如果版本低于 3.8，请升级 Python
# 或使用 pyenv 管理多版本 Python
```

---

## 作为 Python 库使用

### 安装

```bash
pip install file-batch-tool
```

### 使用示例

```python
from file_batch_tool import batch_rename, batch_convert_image, batch_compress

# 批量重命名
batch_rename("/path/to/files", prefix="processed_")

# 图片格式转换
batch_convert_image("/path/to/images", to_format="webp")

# 文件压缩
batch_compress("/path/to/files", output="archive.zip")
```

更多 API 文档请查看 [API.md](API.md)

---

## 技术栈

| 分类 | 技术 | 用途 |
|------|------|------|
| 界面 | PyQt5 | GUI开发 |
| 图片 | Pillow | 格式转换/水印/EXIF |
| 文件 | pathlib, shutil | 跨平台文件操作 |
| 压缩 | zipfile | ZIP打包 |
| 时间 | datetime | 文件时间处理 |

---

## 注意事项

1. **重要文件先备份**，虽然我们有保护机制，但备份更安全
2. **支持拖拽**，直接将文件/文件夹拖入输入框
3. **批量处理**时，界面会显示处理进度
4. **权限问题**：确保程序有文件读写权限
5. **水印/转换**后的文件会自动添加标识前缀/后缀

---

## 开源协议

MIT License - 可以自由使用、修改和分发

---

**如果这个项目对你有帮助，请给个 Star！**
