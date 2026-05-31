# -*- coding: utf-8 -*-
"""配置管理模块"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file: str = "config.json"):
        """初始化配置管理器

        Args:
            config_file: 配置文件名
        """
        self.config_file = Path(config_file)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件

        Returns:
            配置字典
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_default_config()
        return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置

        Returns:
            默认配置字典
        """
        return {
            "theme": "light",
            "language": "zh_CN",
            "auto_save": True,
            "log_level": "INFO",
            "max_file_size": 100 * 1024 * 1024,  # 100MB
            "supported_formats": [".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"],
            "output_directory": "./output",
            "backup_before_operation": False,
            "show_notifications": True,
            "parallel_processing": False,
            "max_workers": 4
        }

    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Failed to save config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """设置配置值

        Args:
            key: 配置键
            value: 配置值
        """
        self.config[key] = value
        self.save_config()

    def reset(self):
        """重置为默认配置"""
        self.config = self._get_default_config()
        self.save_config()


config = ConfigManager()
