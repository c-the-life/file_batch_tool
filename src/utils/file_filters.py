# -*- coding: utf-8 -*-
"""文件过滤器模块"""

import re
from pathlib import Path
from typing import List, Callable, Optional
from datetime import datetime, timedelta


class FileFilter:
    """文件过滤器基类"""

    def matches(self, file_path: Path) -> bool:
        """检查文件是否匹配

        Args:
            file_path: 文件路径

        Returns:
            是否匹配
        """
        raise NotImplementedError


class ExtensionFilter(FileFilter):
    """扩展名过滤器"""

    def __init__(self, extensions: List[str]):
        """初始化扩展名过滤器

        Args:
            extensions: 扩展名列表，如 ['.jpg', '.png']
        """
        self.extensions = [ext.lower() for ext in extensions]

    def matches(self, file_path: Path) -> bool:
        """检查文件扩展名是否匹配"""
        return file_path.suffix.lower() in self.extensions


class NamePatternFilter(FileFilter):
    """文件名模式过滤器"""

    def __init__(self, pattern: str, use_regex: bool = False):
        """初始化文件名模式过滤器

        Args:
            pattern: 文件名模式
            use_regex: 是否使用正则表达式
        """
        self.pattern = pattern
        self.use_regex = use_regex
        if use_regex:
            self.regex = re.compile(pattern)

    def matches(self, file_path: Path) -> bool:
        """检查文件名是否匹配"""
        name = file_path.name
        if self.use_regex:
            return bool(self.regex.search(name))
        return self.pattern.lower() in name.lower()


class SizeFilter(FileFilter):
    """文件大小过滤器"""

    def __init__(self, min_size: int = 0, max_size: Optional[int] = None):
        """初始化文件大小过滤器

        Args:
            min_size: 最小文件大小（字节）
            max_size: 最大文件大小（字节），None表示无限制
        """
        self.min_size = min_size
        self.max_size = max_size

    def matches(self, file_path: Path) -> bool:
        """检查文件大小是否在范围内"""
        if not file_path.is_file():
            return False
        size = file_path.stat().st_size
        if size < self.min_size:
            return False
        if self.max_size is not None and size > self.max_size:
            return False
        return True


class DateFilter(FileFilter):
    """日期过滤器"""

    def __init__(self, days: int, before: bool = True):
        """初始化日期过滤器

        Args:
            days: 天数
            before: True表示days天之前的文件，False表示days天之内的文件
        """
        self.days = days
        self.before = before
        self.cutoff_date = datetime.now() - timedelta(days=days)

    def matches(self, file_path: Path) -> bool:
        """检查文件修改日期是否匹配"""
        if not file_path.is_file():
            return False
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        if self.before:
            return mtime < self.cutoff_date
        return mtime >= self.cutoff_date


class CompositeFilter(FileFilter):
    """组合过滤器"""

    def __init__(self, filters: List[FileFilter], match_all: bool = True):
        """初始化组合过滤器

        Args:
            filters: 过滤器列表
            match_all: True表示所有过滤器都匹配，False表示任一匹配
        """
        self.filters = filters
        self.match_all = match_all

    def matches(self, file_path: Path) -> bool:
        """检查文件是否匹配组合条件"""
        if self.match_all:
            return all(f.matches(file_path) for f in self.filters)
        return any(f.matches(file_path) for f in self.filters)


def filter_files(files: List[Path], filter_func: Callable[[Path], bool]) -> List[Path]:
    """根据过滤函数过滤文件

    Args:
        files: 文件列表
        filter_func: 过滤函数

    Returns:
        过滤后的文件列表
    """
    return [f for f in files if filter_func(f)]
