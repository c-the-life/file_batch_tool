from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="file-batch-tool",
    version="1.0.0",
    author="the-life",
    author_email="your-email@example.com", # 替换为你的邮箱
    description="轻量文件批量处理工具，支持重命名、图片转换、压缩、分类、加水印",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/the-life/file-batch-tool",
    packages=find_packages(),
    install_requires=[
        "Pillow>=10.0.0",
        "tqdm>=4.65.0"
    ],
    entry_points={
        "console_scripts": [
            "file-batch-tool = file_batch_tool:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
