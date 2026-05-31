# -*- coding: utf-8 -*-
"""错误处理和异常定义模块"""

from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(Enum):
    """错误代码枚举"""
    SUCCESS = 0
    FILE_NOT_FOUND = 1001
    PERMISSION_DENIED = 1002
    INVALID_PATH = 1003
    FILE_IN_USE = 1004
    DISK_FULL = 1005
    UNSUPPORTED_FORMAT = 2001
    CONVERSION_FAILED = 2002
    INVALID_IMAGE = 2003
    WATERMARK_FAILED = 2004
    CONFIG_ERROR = 3001
    UNKNOWN_ERROR = 9999


class FileBatchToolError(Exception):
    """文件批量处理工具异常基类"""

    def __init__(self, message: str, code: ErrorCode = ErrorCode.UNKNOWN_ERROR, details: Optional[Dict[str, Any]] = None):
        """初始化异常

        Args:
            message: 错误消息
            code: 错误代码
            details: 错误详情
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self) -> str:
        """返回错误字符串表示"""
        return f"[{self.code.name}] {self.message}"


class FileNotFoundError_(FileBatchToolError):
    """文件未找到异常"""

    def __init__(self, file_path: str):
        super().__init__(
            message=f"文件未找到: {file_path}",
            code=ErrorCode.FILE_NOT_FOUND,
            details={"file_path": file_path}
        )


class PermissionDeniedError(FileBatchToolError):
    """权限不足异常"""

    def __init__(self, file_path: str):
        super().__init__(
            message=f"权限不足，无法访问: {file_path}",
            code=ErrorCode.PERMISSION_DENIED,
            details={"file_path": file_path}
        )


class UnsupportedFormatError(FileBatchToolError):
    """不支持的格式异常"""

    def __init__(self, format_: str):
        super().__init__(
            message=f"不支持的格式: {format_}",
            code=ErrorCode.UNSUPPORTED_FORMAT,
            details={"format": format_}
        )


class ConversionError(FileBatchToolError):
    """格式转换异常"""

    def __init__(self, source: str, target: str, reason: str = ""):
        super().__init__(
            message=f"转换失败: {source} -> {target}" + (f" ({reason})" if reason else ""),
            code=ErrorCode.CONVERSION_FAILED,
            details={"source": source, "target": target, "reason": reason}
        )


def handle_error(error: Exception, log_callback: Optional[callable] = None) -> ErrorCode:
    """统一错误处理

    Args:
        error: 异常对象
        log_callback: 日志回调函数

    Returns:
        错误代码
    """
    if isinstance(error, FileBatchToolError):
        code = error.code
        message = str(error)
    else:
        code = ErrorCode.UNKNOWN_ERROR
        message = f"未知错误: {str(error)}"

    if log_callback:
        log_callback(f"❌ {message}")

    return code


def get_error_suggestion(code: ErrorCode) -> str:
    """获取错误处理建议

    Args:
        code: 错误代码

    Returns:
        建议文本
    """
    suggestions = {
        ErrorCode.FILE_NOT_FOUND: "请检查文件路径是否正确，文件是否存在",
        ErrorCode.PERMISSION_DENIED: "请尝试以管理员身份运行，或检查文件权限",
        ErrorCode.INVALID_PATH: "请检查路径格式是否正确",
        ErrorCode.FILE_IN_USE: "请关闭可能占用该文件的程序后重试",
        ErrorCode.DISK_FULL: "请清理磁盘空间后重试",
        ErrorCode.UNSUPPORTED_FORMAT: "请确认文件格式是否支持",
        ErrorCode.CONVERSION_FAILED: "请检查源文件是否损坏，或尝试其他格式",
        ErrorCode.INVALID_IMAGE: "请确保图片文件完整且未被损坏",
        ErrorCode.WATERMARK_FAILED: "请检查水印参数是否正确，或图片是否支持",
        ErrorCode.CONFIG_ERROR: "请检查配置文件是否正确",
        ErrorCode.UNKNOWN_ERROR: "请查看详细错误信息或联系开发者",
    }
    return suggestions.get(code, "请查看错误详情")
