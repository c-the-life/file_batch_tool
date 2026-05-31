"""文件批量处理工具 - 安装配置文件
用于打包和发布到 PyPI

这个配置文件定义了项目的元数据、依赖关系、
入口点等信息，用于支持 pip 安装和打包。

项目特点：
- 图形化界面，操作简单直观
- 支持多种批量文件操作
- 支持AI智能助手（可选）
- 跨平台支持（Windows/Linux/macOS）
- 完整的API文档和示例代码
"""
from setuptools import setup, find_packages

# 读取README.md作为长描述
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="file-batch-tool",
    version="1.2.0",
    author="the-life",
    author_email="3331648097@qq.com",
    maintainer="the-life",
    maintainer_email="3331648097@qq.com",
    description="功能强大的文件批量处理工具，支持重命名、图片转换、压缩、分类、加水印、AI助手等",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/c-the-life/file_batch_tool",
    download_url="https://github.com/c-the-life/file_batch_tool/releases",
    project_urls={
        "Bug Tracker": "https://github.com/c-the-life/file_batch_tool/issues",
        "Documentation": "https://github.com/c-the-life/file_batch_tool/blob/master/README.md",
        "Source Code": "https://github.com/c-the-life/file_batch_tool",
        "Changelog": "https://github.com/c-the-life/file_batch_tool/blob/master/CHANGELOG.md",
        "Examples": "https://github.com/c-the-life/file_batch_tool/tree/master/examples",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Pillow>=10.0.0",
        "PyQt5>=5.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "ai": [
            "openai>=1.0.0",
        ],
        "all": [
            "openai>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "file-batch-tool=file_batch_tool.main_window:run",
            "fbt=file_batch_tool.main_window:run",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
        "Topic :: Desktop Environment",
        "Topic :: File Formats",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
    ],
    python_requires=">=3.8",
    keywords=[
        "file batch",
        "rename",
        "image convert",
        "watermark",
        "compress",
        "file management",
        "batch processing",
        "GUI",
        "PyQt5",
        "EXIF",
        "image processing",
        "file organizer",
        "photo management",
        "utility",
        "tool",
    ],
    zip_safe=False,
    include_package_data=True,
    platforms=["Windows", "Linux", "macOS"],
)
