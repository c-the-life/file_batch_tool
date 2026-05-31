"""
快速入门示例
演示如何使用 file_batch_tool 库

本示例展示了 file_batch_tool 库的基本用法，
包括批量重命名、图片格式转换和文件压缩等功能。

运行前请确保已安装依赖：
    pip install file-batch-tool

或者从源码安装：
    pip install -e .
"""
# 标准库导入
import os
from pathlib import Path

# 项目库导入
from file_batch_tool import batch_rename, batch_convert_image, batch_compress


def example_1_rename():
    """
    示例1：批量重命名文件
    
    功能说明：
    - 自动创建测试目录和测试文件
    - 为所有文件添加前缀和后缀
    - 演示基本的重命名功能
    
    参数说明：
    - prefix: 文件名前缀
    - suffix: 文件名后缀
    - find_str: 要查找替换的字符串（可选）
    - replace_str: 替换为的字符串（可选）
    """
    print("=" * 60)
    print("示例1：批量重命名文件")
    print("=" * 60)
    
    # Step 1: 创建测试目录（如果不存在）
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    print(f"✅ 创建测试目录: {test_dir.absolute()}")
    
    # Step 2: 创建一些测试文件用于演示
    print("📝 创建测试文件...")
    for i in range(3):
        file_path = test_dir / f"test_{i}.txt"
        file_path.touch()
        print(f"  - 创建: {file_path.name}")
    
    # Step 3: 执行批量重命名
    print("\n🔄 开始批量重命名...")
    batch_rename(
        dir_path=str(test_dir),
        prefix="processed_",  # 添加前缀
        suffix="_v1"         # 添加后缀
    )
    
    print("✅ 重命名完成！文件将具有类似 'processed_test_0_v1.txt' 的格式")


def example_2_convert():
    """
    示例2：图片格式转换
    
    功能说明：
    - 支持 JPG/PNG/WebP 等格式互转
    - 自动处理透明通道
    - 保持图片质量
    
    支持的格式：
    - jpg / jpeg
    - png
    - webp
    """
    print("\n" + "=" * 60)
    print("示例2：图片格式转换")
    print("=" * 60)
    
    # 注意：需要准备图片目录才能运行此示例
    # 取消下面的注释并修改路径以运行实际转换
    """
    # 示例：将图片转换为 WebP 格式（更小的文件体积）
    image_dir = Path("/path/to/your/images")  # 请修改为实际路径
    if image_dir.exists():
        print("🔄 开始图片格式转换...")
        batch_convert_image(
            dir_path=str(image_dir),
            to_format="webp"  # 目标格式
        )
        print("✅ 图片格式转换完成！")
    else:
        print(f"⚠️  目录不存在: {image_dir}")
    """
    print("💡 提示：请准备图片目录后取消注释运行此示例")


def example_3_compress():
    """
    示例3：文件压缩
    
    功能说明：
    - 将多个文件打包为 ZIP 压缩包
    - 支持排除指定类型的文件
    - 自定义输出文件名
    
    参数说明：
    - output: 输出文件名（可选）
    - exclude: 要排除的扩展名（可选，逗号分隔）
    """
    print("\n" + "=" * 60)
    print("示例3：文件压缩")
    print("=" * 60)
    
    # 检查测试目录是否存在
    test_dir = Path("test_files")
    if test_dir.exists():
        print("📦 开始文件压缩...")
        
        # 执行压缩操作
        batch_compress(
            dir_path=str(test_dir),
            output="test_files.zip"  # 输出文件名
        )
        
        print("✅ 压缩完成！")
        print(f"📄 压缩包位置: {Path('test_files.zip').absolute()}")
    else:
        print("⚠️  测试目录不存在，请先运行示例1")


def main():
    """
    主函数：运行所有示例
    
    按顺序执行三个示例，演示库的主要功能
    """
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "file_batch_tool 快速入门示例" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # 运行所有示例
    example_1_rename()
    example_2_convert()
    example_3_compress()
    
    print("\n" + "=" * 60)
    print("🎉 所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
