from setuptools import setup

# 读取README.md作为长描述
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="file-batch-tool",          # PyPI项目名（必须唯一，小写无空格）
    version="1.0.0",                 # 版本号（语义化：x.y.z）
    author="the-life",               # 作者名
    author_email="3331648097@qq.com", # 替换为你的真实邮箱（PyPI公开）
    description="轻量文件批量处理工具，支持重命名、图片转换、压缩、分类、加水印",
    long_description=long_description,       # 长描述（README内容）
    long_description_content_type="text/markdown", # 长描述格式
    url="https://gitee.com/the-life/file_batch_tool", # 项目仓库地址
    py_modules=["file_batch_tool"],  # 指定主模块文件名（不含.py）
    install_requires=[               # 项目依赖
        "Pillow>=10.0.0",
        "tqdm>=4.65.0"
    ],
    entry_points={                   # 生成系统可执行命令
        "console_scripts": [
            "file-batch-tool = file_batch_tool:main" # 命令名 = 模块名:函数名
        ]
    },
    classifiers=[                    # 分类标签（帮助PyPI分类）
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",          # 新增：项目状态
        "Intended Audience :: End Users/Desktop",  # 新增：目标用户
        "Topic :: Utilities",                      # 新增：工具分类
    ],
    python_requires=">=3.7",         # 支持的Python版本
    keywords=["file batch", "rename", "image convert", "watermark"], # 新增：搜索关键词
    zip_safe=False,                  # 新增：避免导入问题（非必需，但推荐）
)