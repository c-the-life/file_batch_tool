"""文件批量处理工具 - 工具模块
包含文件操作和AI助手功能

这个模块提供了项目的核心功能实现，包括：
- 文件操作工具函数
- 批量处理函数
- AI智能助手类

所有函数都支持自定义日志回调和进度显示。
"""

from .file_operations import (
    safe_log,
    parse_input_path,
    get_unique_path,
    batch_rename,
    batch_convert_image,
    batch_compress,
    batch_classify,
    batch_watermark,
    batch_modify_file_time,
    batch_extract_exif,
    batch_copy_move,
)

from .ai_assistant import AIAssistant

__all__ = [
    "safe_log",
    "parse_input_path",
    "get_unique_path",
    "batch_rename",
    "batch_convert_image",
    "batch_compress",
    "batch_classify",
    "batch_watermark",
    "batch_modify_file_time",
    "batch_extract_exif",
    "batch_copy_move",
    "AIAssistant",
]

# 模块元数据
__module_version__ = "1.0.0"
__module_author__ = "File Batch Tool Team"

