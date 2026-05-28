from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="file-batch-tool",
    version="1.2.0",
    author="the-life",
    author_email="3331648097@qq.com",
    description="轻量文件批量处理工具，支持重命名、图片转换、压缩、分类、加水印等",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/c-the-life/file_batch_tool",
    project_urls={
        "Bug Tracker": "https://github.com/c-the-life/file_batch_tool/issues",
        "Documentation": "https://github.com/c-the-life/file_batch_tool/blob/master/README.md",
        "Source Code": "https://github.com/c-the-life/file_batch_tool",
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
            "black>=23.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "file-batch-tool=file_batch_tool.main_window:run"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
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
        "Topic :: Utilities",
        "Topic :: Desktop Environment",
        "Topic :: File Formats",
        "Topic :: Multimedia :: Graphics",
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
    ],
    zip_safe=False,
    include_package_data=True,
)
