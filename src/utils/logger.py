# -*- coding: utf-8 -*-
"""日志配置模块"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "file_batch_tool", level: int = logging.INFO) -> logging.Logger:
    """设置日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别

    Returns:
        配置好的Logger实例
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


def get_logger(name: str = "file_batch_tool") -> logging.Logger:
    """获取日志记录器

    Args:
        name: 日志记录器名称

    Returns:
        Logger实例
    """
    return logging.getLogger(name)
