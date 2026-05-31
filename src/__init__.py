"""文件批量处理工具 - 源文件包
包含所有源代码模块

这个项目提供了一个功能强大的文件批量处理工具，支持：
- 批量重命名文件（添加前缀/后缀、替换字符）
- 图片格式转换（支持 JPG、PNG、WebP、BMP、GIF 等）
- 文件压缩（ZIP 格式）
- 文件分类整理（按扩展名、日期、大小分类）
- 图片水印添加（文字水印和图片水印）
- 文件时间修改（修改创建时间、修改时间、访问时间）
- EXIF信息提取（批量提取并导出为CSV）
- 文件复制/移动
- AI智能助手（自然语言命令处理，支持OpenAI GPT）

模块结构：
- utils: 工具函数模块（文件操作、AI助手等）
- core: 核心功能模块（工作线程、任务处理等）
- ui: 用户界面模块（PyQt5 GUI）

使用示例：
    from file_batch_tool import batch_rename
    batch_rename(dir_path="./images", prefix="vacation_")
"""

__version__ = "1.2.0"
__author__ = "the-life"
__description__ = "一个功能强大的文件批量处理工具"
__license__ = "MIT"
__url__ = "https://github.com/the-life/file_batch_tool"
__keywords__ = ["file", "batch", "tool", "pyqt5", "image", "processing", "watermark", "exif", "rename"]

