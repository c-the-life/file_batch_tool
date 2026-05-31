# 📖 完整教程

> **学习目标**：本教程将帮助您从零基础开始，掌握 file_batch_tool 的所有功能，包括图形界面使用、作为 Python 库开发、依赖管理、以及发布自己的库。

---

## 目录
1. [快速入门](#1-快速入门)
2. [作为库使用](#2-作为库使用)
3. [依赖其他项目](#3-依赖其他项目)
4. [发布自己的库](#4-发布自己的库)
5. [让其他项目依赖你](#5-让其他项目依赖你)
6. [最佳实践](#6-最佳实践)

---

## 1. 快速入门

### 1.1 图形界面使用

```bash
# 克隆项目
git clone https://github.com/c-the-life/file_batch_tool.git
cd file_batch_tool

# 安装依赖
pip install -r requirements.txt

# 运行程序
python file-batch-tool.py
```

### 1.2 项目结构

```
file_batch_tool/
├── src/
│   ├── core/              # 核心模块
│   │   └── worker.py      # 工作线程
│   ├── ui/                # 界面模块
│   │   └── main_window.py # 主窗口
│   ├── utils/             # 工具模块
│   │   └── file_operations.py  # 文件操作函数
│   └── __init__.py        # 包导出
├── examples/              # 示例代码
├── API.md                 # API 文档
├── DEPENDENCIES.md        # 依赖管理指南
├── README.md              # 项目说明
├── requirements.txt       # 依赖列表
└── setup.py               # 打包配置
```

---

## 2. 作为库使用

### 2.1 安装

```bash
# 从源码安装（开发模式）
pip install -e .

# 或使用 requirements.txt
pip install -r requirements.txt
```

### 2.2 基本导入

```python
# 导入所有功能
from file_batch_tool import (
    batch_rename,
    batch_convert_image,
    batch_compress,
    batch_classify,
    batch_watermark,
    batch_modify_file_time,
    batch_extract_exif,
    batch_copy_move,
    FileToolMainWindow,
    WorkerThread
)
```

### 2.3 实际例子

#### 例子1：批量处理图片

```python
"""
图片批量处理脚本
1. 转换格式
2. 添加水印
3. 重命名
"""
from file_batch_tool import batch_convert_image, batch_watermark, batch_rename
from pathlib import Path

def process_photo_album(input_dir):
    # 1. 转换为 WebP 格式
    print("步骤1：转换格式...")
    batch_convert_image(input_dir, to_format="webp")
    
    # 2. 添加水印
    print("\n步骤2：添加水印...")
    batch_watermark(
        input_dir,
        type_="text",
        content="My Photo Album",
        size=30,
        opacity=100
    )
    
    # 3. 重命名
    print("\n步骤3：重命名...")
    batch_rename(input_dir, prefix="photo_", suffix="_processed")
    
    print("\n✅ 处理完成！")

if __name__ == "__main__":
    process_photo_album("./my_photos")
```

#### 例子2：自动化备份脚本

```python
"""
自动化备份脚本
每周备份重要文件
"""
from file_batch_tool import batch_compress, batch_copy_move
from datetime import datetime
import os

def backup_files(source_dir, backup_dir):
    # 创建带日期的备份目录
    date_str = datetime.now().strftime("%Y%m%d")
    backup_path = f"{backup_dir}/backup_{date_str}"
    
    # 复制文件
    print(f"复制文件到 {backup_path}...")
    batch_copy_move(
        source_dir,
        target_dir=backup_path,
        mode="copy",
        exclude="tmp,log"
    )
    
    # 压缩备份
    print("压缩备份...")
    batch_compress(
        backup_path,
        output=f"{backup_path}.zip"
    )
    
    print("✅ 备份完成！")

if __name__ == "__main__":
    backup_files("./important_files", "./backups")
```

#### 例子3：带进度回调

```python
"""
带进度显示的处理
"""
from file_batch_tool import batch_rename, batch_compress

def progress_callback(msg):
    if msg.startswith("progress:"):
        progress = int(msg.split(":")[1])
        bar_length = 40
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\r处理中: [{bar}] {progress}%", end="", flush=True)
    else:
        print(f"\n{msg}")

def process_with_progress(directory):
    print("开始处理...")
    batch_rename(
        directory,
        prefix="final_",
        log_callback=progress_callback
    )
    
    print("\n压缩文件...")
    batch_compress(
        directory,
        output="result.zip",
        log_callback=progress_callback
    )

if __name__ == "__main__":
    process_with_progress("./files_to_process")
```

---

## 3. 依赖其他项目

### 3.1 在 requirements.txt 中添加依赖

```txt
# file_batch_tool 的依赖（已有）
Pillow>=10.0.0
PyQt5>=5.15.0

# 添加新的依赖
requests>=2.31.0          # HTTP 请求
numpy>=1.24.0             # 数值计算
pandas>=2.0.0             # 数据处理
```

### 3.2 在 setup.py 中添加依赖

```python
# setup.py
setup(
    name="file-batch-tool",
    version="1.1.0",
    # ... 其他配置
    install_requires=[
        "Pillow>=10.0.0",
        "PyQt5>=5.15.0",
        "requests>=2.31.0",  # 新增依赖
        "numpy>=1.24.0",     # 新增依赖
    ],
    # 可选依赖
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
        ],
        "full": [
            "requests>=2.31.0",
            "numpy>=1.24.0",
            "pandas>=2.0.0",
        ]
    }
)
```

### 3.3 使用新加的依赖

```python
# 在您的代码中使用新依赖
import requests
import numpy as np
from PIL import Image

def download_image(url, save_path):
    """使用 requests 下载图片"""
    response = requests.get(url)
    with open(save_path, "wb") as f:
        f.write(response.content)

def process_with_numpy(image_path):
    """使用 numpy 处理图片"""
    img = Image.open(image_path)
    img_array = np.array(img)
    # 处理...
    return img_array
```

---

## 4. 发布自己的库

### 4.1 准备工作

```bash
# 1. 安装必要的工具
pip install --upgrade build twine

# 2. 清理旧的构建
rm -rf dist/ build/ *.egg-info/
```

### 4.2 构建包

```bash
# 构建
python -m build
```

这会在 `dist/` 目录下生成：
- `.tar.gz` - 源码分发包
- `.whl` - 二进制分发包

### 4.3 上传到 TestPyPI（测试）

```bash
# 注册账号：https://test.pypi.org/account/register/

# 上传
twine upload --repository testpypi dist/*
```

测试安装：
```bash
pip install --index-url https://test.pypi.org/simple/ file-batch-tool
```

### 4.4 上传到 PyPI（正式）

```bash
# 注册账号：https://pypi.org/account/register/

# 上传
twine upload dist/*
```

正式安装：
```bash
pip install file-batch-tool
```

---

## 5. 让其他项目依赖你

### 5.1 场景1：另一个 Python 项目依赖你

假设 Alice 在做一个项目叫 `photo-manager`，她想使用你的库。

#### Alice 的项目结构

```
photo-manager/
├── requirements.txt
├── setup.py
└── photo_manager/
    ├── __init__.py
    └── main.py
```

#### Alice 的 requirements.txt

```txt
# 依赖你的库
file-batch-tool>=1.1.0

# 她项目的其他依赖
Pillow>=10.0.0
requests>=2.31.0
```

#### Alice 的代码

```python
# photo_manager/main.py
from file_batch_tool import batch_convert_image, batch_watermark

class PhotoManager:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
    
    def process(self):
        # 使用你的库
        batch_convert_image(self.input_dir, to_format="webp")
        batch_watermark(
            self.input_dir,
            type_="text",
            content="© Photo Manager"
        )
        print("✅ 处理完成！")

if __name__ == "__main__":
    manager = PhotoManager("./photos", "./output")
    manager.process()
```

### 5.2 场景2：从 Git 仓库依赖

如果 Alice 想直接用 GitHub 上的最新版本：

```txt
# Alice 的 requirements.txt
git+https://github.com/c-the-life/file_batch_tool.git@main#egg=file-batch-tool
```

或者指定版本：

```txt
git+https://github.com/c-the-life/file_batch_tool.git@v1.1.0#egg=file-batch-tool
```

### 5.3 场景3：作为子模块

```bash
# Alice 把你的项目作为子模块
git submodule add https://github.com/c-the-life/file_batch_tool.git libs/file_batch_tool
```

然后在她的代码中：

```python
import sys
sys.path.append("libs/file_batch_tool/src")

from file_batch_tool import batch_rename
```

---

## 6. 最佳实践

### 6.1 版本管理

使用语义化版本：
- `1.0.0` - 初始版本
- `1.0.1` - Bug 修复
- `1.1.0` - 新功能（向后兼容）
- `2.0.0` - 重大变更（不兼容）

### 6.2 文档

- ✅ 保持 README 最新
- ✅ 提供 API 文档
- ✅ 提供示例代码
- ✅ 维护变更日志

### 6.3 测试

```python
# 为您的库编写测试
import pytest
from file_batch_tool import batch_rename
from pathlib import Path

def test_batch_rename(tmp_path):
    # 创建测试文件
    test_file = tmp_path / "test.txt"
    test_file.touch()
    
    # 执行重命名
    batch_rename(str(tmp_path), prefix="new_")
    
    # 验证
    assert (tmp_path / "new_test.txt").exists()
```

---

## 7. 常见错误处理

### 7.1 文件操作错误

#### 错误1：PermissionError（权限不足）

**错误信息：**
```
PermissionError: [WinError 5] 拒绝访问: 'xxx.jpg'
```

**解决方案：**
```python
from file_batch_tool import batch_rename

# 方法1：关闭占用文件的程序
# 先确保文件没有被打开

# 方法2：以管理员权限运行程序（Windows）
# 右键点击命令行 → 以管理员身份运行

# 方法3：在代码中添加异常处理
try:
    batch_rename("./photos", prefix="new_")
except PermissionError as e:
    print(f"权限错误：{e}")
    print("请关闭占用文件的程序，或以管理员身份运行")
```

#### 错误2：FileNotFoundError（文件不存在）

**错误信息：**
```
FileNotFoundError: [WinError 2] 系统找不到指定的文件: 'xxx.jpg'
```

**解决方案：**
```python
from file_batch_tool import batch_rename
from pathlib import Path

def safe_batch_rename(dir_path, **kwargs):
    """安全的批量重命名"""
    if not Path(dir_path).exists():
        print(f"错误：目录不存在 - {dir_path}")
        return False
    
    # 检查目录中是否有文件
    files = list(Path(dir_path).iterdir())
    if not files:
        print(f"警告：目录为空 - {dir_path}")
        return False
    
    batch_rename(dir_path, **kwargs)
    return True

# 使用
safe_batch_rename("./photos", prefix="new_")
```

#### 错误3：UnicodeEncodeError（编码错误）

**错误信息：**
```
UnicodeEncodeError: 'gbk' codec can't encode character
```

**解决方案：**
```python
# 方法1：在代码开头设置编码
import sys
if sys.platform == 'win32':
    # 尝试设置标准输出编码
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 方法2：使用项目内置的安全日志函数
from file_batch_tool import safe_log

safe_log("处理包含特殊字符的文件名: 📷照片.jpg")
```

### 7.2 图片处理错误

#### 错误1：UnidentifiedImageError（无法识别图片）

**错误信息：**
```
PIL.UnidentifiedImageError: cannot identify image file
```

**解决方案：**
```python
from file_batch_tool import batch_convert_image

try:
    batch_convert_image("./images", to_format="webp")
except Exception as e:
    print(f"图片处理错误：{e}")
    print("提示：请确保所有文件都是有效的图片格式")
```

#### 错误2：OSError（文件损坏）

**错误信息：**
```
OSError: image file is truncated
```

**解决方案：**
```python
from PIL import Image, ImageFile
import os
from pathlib import Path

# 启用损坏文件处理
ImageFile.LOAD_TRUNCATED_IMAGES = True

def repair_images(dir_path):
    """尝试修复损坏的图片"""
    for img_path in Path(dir_path).glob("*.jpg"):
        try:
            with Image.open(img_path) as img:
                img.save(img_path)  # 重新保存以修复
                print(f"已修复: {img_path.name}")
        except Exception as e:
            print(f"无法修复: {img_path.name}, 错误: {e}")
```

### 7.3 依赖安装错误

#### 错误1：PyQt5 安装失败

**错误信息：**
```
ERROR: Could not build wheels for PyQt5
```

**解决方案：**
```bash
# 方法1：尝试安装预编译版本
pip install PyQt5==5.15.9

# 方法2：使用 conda 安装（推荐）
conda install pyqt

# 方法3：Linux用户安装系统依赖
sudo apt-get install libgl1-mesa-glx libegl1
```

#### 错误2：Pillow 安装失败

**解决方案：**
```bash
# 升级 pip 和 setuptools
pip install --upgrade pip setuptools wheel

# 重新安装 Pillow
pip install --force-reinstall Pillow>=10.0.0
```

### 7.4 最佳实践：统一错误处理

```python
"""
完整的错误处理示例
"""
from file_batch_tool import (
    batch_rename,
    batch_convert_image,
    safe_log
)
from pathlib import Path
from typing import Callable, Optional

def robust_process(
    dir_path: str,
    process_func: Callable,
    func_name: str = "处理",
    **kwargs
) -> bool:
    """
    健壮的文件处理函数
    
    Args:
        dir_path: 目录路径
        process_func: 处理函数
        func_name: 函数名称（用于日志）
        **kwargs: 传递给处理函数的参数
    
    Returns:
        是否成功
    """
    dir_p = Path(dir_path)
    
    # 前置检查
    if not dir_p.exists():
        safe_log(f"❌ 错误：目录不存在 - {dir_path}")
        return False
    
    if not dir_p.is_dir():
        safe_log(f"❌ 错误：不是目录 - {dir_path}")
        return False
    
    # 检查是否有文件
    file_count = len(list(dir_p.iterdir()))
    if file_count == 0:
        safe_log(f"⚠️ 警告：目录为空 - {dir_path}")
        return False
    
    safe_log(f"📂 开始{func_name}，共 {file_count} 个文件")
    
    # 执行处理
    try:
        process_func(dir_path, **kwargs)
        safe_log(f"✅ {func_name}完成！")
        return True
    except PermissionError as e:
        safe_log(f"❌ 权限错误：{e}")
        safe_log("💡 请关闭占用文件的程序，或以管理员身份运行")
        return False
    except Exception as e:
        safe_log(f"❌ {func_name}失败：{e}")
        return False

# 使用示例
if __name__ == "__main__":
    # 批量重命名
    robust_process(
        "./photos",
        batch_rename,
        "批量重命名",
        prefix="processed_"
    )
    
    # 格式转换
    robust_process(
        "./photos",
        batch_convert_image,
        "格式转换",
        to_format="webp"
    )
```

---

## 总结

现在您已经知道：

1. ✅ 如何使用图形界面
2. ✅ 如何作为 Python 库使用
3. ✅ 如何依赖其他项目
4. ✅ 如何发布自己的库
5. ✅ 如何让其他项目依赖你
6. ✅ 如何处理常见错误
7. ✅ 最佳实践和代码规范

开始编码吧！🚀

