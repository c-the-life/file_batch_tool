# 📚 API 文档

> **API 说明**：本页面提供了 file_batch_tool 库的完整 API 参考文档，包括所有核心功能函数的使用方法、参数说明和示例代码。

---

## 目录
- [安装](#安装)
- [快速开始](#快速开始)
- [API 参考](#api-参考)

---

## 安装

```bash
# 从 PyPI 安装
pip install file-batch-tool

# 或从源码安装（开发模式）
git clone https://github.com/c-the-life/file_batch_tool.git
cd file_batch_tool
pip install -e .
```

## 快速开始

```python
from file_batch_tool import (
    batch_rename,
    batch_convert_image,
    batch_compress,
    batch_classify,
    batch_watermark,
    batch_modify_file_time,
    batch_extract_exif,
    batch_copy_move
)
```

---

## API 参考

### 1. 批量重命名 (batch_rename)

**功能说明**：批量重命名文件，支持添加前缀、后缀、替换字符串等操作。

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dir_path | str | 是 | 目录路径或文件路径 |
| prefix | str | 否 | 文件名前缀（默认：""） |
| suffix | str | 否 | 文件名后缀（默认：""） |
| find_str | str | 否 | 要查找并替换的字符串（默认：""） |
| replace_str | str | 否 | 替换后的字符串（默认：""） |
| log_callback | Callable | 否 | 日志回调函数（默认：None） |

**返回值**：None

**使用示例**：
```python
from file_batch_tool import batch_rename

# 重命名整个目录，添加前缀
batch_rename(
    dir_path="/path/to/folder",
    prefix="processed_",
)

# 替换文件名中的特定字符串
batch_rename(
    dir_path="/path/to/folder",
    find_str="photo",
    replace_str="image"
)

# 同时使用前缀和后缀
batch_rename(
    dir_path="/path/to/folder",
    prefix="new_",
    suffix="_v2"
)

# 带自定义日志回调
def my_log(msg):
    if msg.startswith("progress:"):
        progress = int(msg.split(":")[1])
        print(f"进度: {progress}%")
    else:
        print(msg)

batch_rename(
    dir_path="/path/to/folder",
    prefix="processed_",
    log_callback=my_log
)
```

---

### 2. 图片格式转换 (batch_convert_image)

**功能说明**：批量转换图片格式，支持 JPG、PNG、WebP 等格式互转。

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dir_path | str | 是 | 图片目录路径 |
| to_format | str | 否 | 目标格式（默认："webp"） |
| quality | int | 否 | 图片质量 0-100（默认：85） |
| log_callback | Callable | 否 | 日志回调函数（默认：None） |

**支持格式**：jpg、jpeg、png、webp、bmp、gif

**返回值**：None

**使用示例**：
```python
from file_batch_tool import batch_convert_image

# 转换为 WebP 格式（推荐，占用空间小）
batch_convert_image(
    dir_path="/path/to/images",
    to_format="webp",
    quality=90
)

# 转换为 PNG 格式（保持透明）
batch_convert_image(
    dir_path="/path/to/images",
    to_format="png"
)

# 转换为 JPG 格式
batch_convert_image(
    dir_path="/path/to/images",
    to_format="jpg",
    quality=85
)
```

---

### 3. 文件压缩 (batch_compress)

**功能说明**：将目录中的文件批量压缩为 ZIP 格式。

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dir_path | str | 是 | 源目录路径 |
| output | str | 否 | 输出 ZIP 文件路径（默认：自动生成） |
| exclude | str | 否 | 要排除的文件扩展名，逗号分隔（默认：""） |
| log_callback | Callable | 否 | 日志回调函数（默认：None） |

**返回值**：None

**使用示例**：
```python
from file_batch_tool import batch_compress

# 压缩整个目录
batch_compress(
    dir_path="/path/to/files"
)

# 指定输出文件
batch_compress(
    dir_path="/path/to/files",
    output="/path/to/backup.zip"
)

# 排除特定文件类型
batch_compress(
    dir_path="/path/to/files",
    output="/path/to/backup.zip",
    exclude="txt,md,log"
)
```

---

### 4. 文件分类 (batch_classify)

**功能说明**：按文件扩展名或创建日期自动分类整理文件。

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dir_path | str | 是 | 源目录路径 |
| mode | str | 否 | 分类模式："ext"（按扩展名）或 "date"（按日期）（默认："ext"） |
| log_callback | Callable | 否 | 日志回调函数（默认：None） |

**返回值**：None

**使用示例**：
```python
from file_batch_tool import batch_classify

# 按扩展名分类（创建 jpg、png、txt 等子目录）
batch_classify(
    dir_path="/path/to/files",
    mode="ext"
)

# 按日期分类（创建 2024-01、2024-02 等子目录）
batch_classify(
    dir_path="/path/to/files",
    mode="date"
)
```

---

### 5. 添加水印 (batch_watermark)

**功能说明**：为图片批量添加文字水印或图片水印。

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dir_path | str | 是 | 图片目录路径 |
| type_ | str | 是 | 水印类型："text"（文字）或 "image"（图片） |
| content | str | 否 | 文字水印内容（文字模式必填） |
| watermark_path | str | 否 | 水印图片路径（图片模式必填） |
| size | int | 否 | 水印大小（文字模式：字体大小，图片模式：缩放比例）（默认：36） |
| color | str | 否 | 文字颜色，格式："(R,G,B,A)" 0-255（默认："(255,255,255,128)"） |
| opacity | int | 否 | 水印透明度 0-255（默认：128） |
| position | str | 否 | 水印位置："bottom-right"、"top-right"、"bottom-left"、"top-left"、"center"（默认："bottom-right"） |
| log_callback | Callable | 否 | 日志回调函数（默认：None） |

**返回值**：None

**使用示例**：
```python
from file_batch_tool import batch_watermark

# 文字水印 - 右下角半透明白色
batch_watermark(
    dir_path="/path/to/images",
    type_="text",
    content="© 2024 My Photos",
    size=36,
    color="(255,255,255,180)",
    opacity=180,
    position="bottom-right"
)

# 文字水印 - 居中灰色防伪水印
batch_watermark(
    dir_path="/path/to/images",
    type_="text",
    content="CONFIDENTIAL",
    size=80,
    color="(128,128,128,80)",
    opacity=80,
    position="center"
)

# 图片水印 - Logo 水印
batch_watermark(
    dir_path="/path/to/images",
    type_="image",
    watermark_path="/path/to/logo.png",
    size=100,
    opacity=150,
    position="top-right"
)
```

---

### 6. 修改文件时间 (batch_modify_file_time)

**功能说明**：批量修改文件的创建时间、修改时间或访问时间。

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dir_path | str | 是 | 目录路径 |
| target_time | datetime | 是 | 目标时间 |
| time_type | str | 否 | 要修改的时间类型："create"、"modify"、"access"、"both"（默认："both"） |
| log_callback | Callable | 否 | 日志回调函数（默认：None） |

**返回值**：None

**使用示例**：
```python
from file_batch_tool import batch_modify_file_time
from datetime import datetime

# 设置目标时间
target_time = datetime(2024, 1, 1, 12, 0, 0)

# 修改创建和修改时间
batch_modify_file_time(
    dir_path="/path/to/files",
    target_time=target_time,
    time_type="both"
)

# 只修改创建时间
batch_modify_file_time(
    dir_path="/path/to/files",
    target_time=target_time,
    time_type="create"
)

# 只修改修改时间
batch_modify_file_time(
    dir_path="/path/to/files",
    target_time=target_time,
    time_type="modify"
)
```

---

### 7. 提取 EXIF (batch_extract_exif)

**功能说明**：批量提取图片的 EXIF 信息并导出为 CSV 文件。

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dir_path | str | 是 | 图片目录路径 |
| output_csv | str | 否 | 输出 CSV 文件路径（默认：自动生成） |
| log_callback | Callable | 否 | 日志回调函数（默认：None） |

**提取信息**：文件名、文件路径、尺寸、拍摄时间、相机型号、GPS 信息等

**返回值**：None

**使用示例**：
```python
from file_batch_tool import batch_extract_exif

# 提取并默认保存
batch_extract_exif(
    dir_path="/path/to/images"
)

# 指定输出文件
batch_extract_exif(
    dir_path="/path/to/images",
    output_csv="/path/to/exif_data.csv"
)
```

---

### 8. 复制/移动 (batch_copy_move)

**功能说明**：批量复制或移动文件到目标目录。

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dir_path | str | 是 | 源目录路径 |
| target_dir | str | 是 | 目标目录路径 |
| mode | str | 是 | 操作模式："copy"（复制）或 "move"（移动） |
| exclude | str | 否 | 要排除的文件扩展名，逗号分隔（默认：""） |
| log_callback | Callable | 否 | 日志回调函数（默认：None） |

**返回值**：None

**使用示例**：
```python
from file_batch_tool import batch_copy_move

# 批量复制文件
batch_copy_move(
    dir_path="/path/to/source",
    target_dir="/path/to/destination",
    mode="copy"
)

# 批量移动文件
batch_copy_move(
    dir_path="/path/to/source",
    target_dir="/path/to/destination",
    mode="move"
)

# 复制时排除特定文件
batch_copy_move(
    dir_path="/path/to/source",
    target_dir="/path/to/destination",
    mode="copy",
    exclude="log,txt,md"
)
```

---

### 9. 辅助函数

#### safe_log
**功能说明**：安全的日志输出函数，处理 Unicode 编码问题。

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| msg | str | 是 | 日志消息 |
| log_callback | Callable | 否 | 自定义日志回调（默认：None） |

**使用示例**：
```python
from file_batch_tool import safe_log

# 简单使用
safe_log("处理完成！")

# 结合自定义回调
def my_logger(msg):
    print(f"[LOG] {msg}")

safe_log("处理中...", log_callback=my_logger)
```

---

## 常见用例组合

### 完整的图片处理流程
```python
from file_batch_tool import (
    batch_convert_image,
    batch_watermark,
    batch_rename,
    batch_compress
)

# 1. 转换为 WebP 格式
batch_convert_image("/path/to/images", to_format="webp")

# 2. 添加水印
batch_watermark(
    "/path/to/images",
    type_="text",
    content="© My Photos",
    size=36
)

# 3. 重命名
batch_rename("/path/to/images", prefix="processed_")

# 4. 压缩备份
batch_compress("/path/to/images", output="processed_images.zip")
```

### 自动归档工作流
```python
from file_batch_tool import (
    batch_classify,
    batch_compress,
    batch_copy_move
)
from datetime import datetime

# 1. 按日期分类
batch_classify("/path/to/files", mode="date")

# 2. 复制到备份目录
date_str = datetime.now().strftime("%Y%m%d")
batch_copy_move(
    "/path/to/files",
    f"/path/to/backup/{date_str}",
    mode="copy"
)

# 3. 压缩备份
batch_compress(f"/path/to/backup/{date_str}")
```
