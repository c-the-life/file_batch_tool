#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""单元测试文件"""

import unittest
import tempfile
import os
from pathlib import Path
from src.utils.file_operations import safe_log


class TestFileOperations(unittest.TestCase):
    """文件操作测试"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.temp_dir.name)

    def tearDown(self):
        """测试后清理"""
        self.temp_dir.cleanup()

    def test_safe_log(self):
        """测试安全日志函数"""
        # 测试正常日志
        log_output = []
        
        def log_callback(msg):
            log_output.append(msg)
        
        safe_log("测试消息", log_callback)
        self.assertEqual(len(log_output), 1)
        self.assertEqual(log_output[0], "测试消息")
    
    def test_safe_log_unicode(self):
        """测试Unicode日志"""
        # 测试Emoji
        log_output = []
        
        def log_callback(msg):
            log_output.append(msg)
        
        safe_log("📁 文件处理测试", log_callback)
        self.assertEqual(len(log_output), 1)
        self.assertTrue("文件处理" in log_output[0])


class TestPathOperations(unittest.TestCase):
    """路径操作测试"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)

    def tearDown(self):
        """测试后清理"""
        self.temp_dir.cleanup()

    def test_directory_creation(self):
        """测试目录创建"""
        test_dir = self.test_dir / "test_subdir"
        test_dir.mkdir(exist_ok=True)
        self.assertTrue(test_dir.exists())
        self.assertTrue(test_dir.is_dir())

    def test_file_creation(self):
        """测试文件创建"""
        test_file = self.test_dir / "test.txt"
        test_file.write_text("测试内容")
        self.assertTrue(test_file.exists())
        self.assertTrue(test_file.is_file())
        self.assertEqual(test_file.read_text(), "测试内容")


if __name__ == '__main__':
    unittest.main()
