#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件批量处理工具
支持功能：
1. 批量重命名（正则替换、前缀/后缀）
2. 批量转换图片格式（jpg/png/webp）
3. 批量压缩文件（ZIP）
4. 批量文件分类（按扩展名/日期归档）
5. 图片批量加水印（文字/图片水印）
6. 批量修改文件时间
7. 批量提取图片EXIF信息
8. 批量复制/移动文件
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.ui.main_window import FileToolMainWindow


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    window = FileToolMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()