"""
高级用法示例
演示如何使用回调函数、多任务处理等

本示例展示了：
1. 使用自定义日志回调函数
2. 带进度条的文件处理
3. 为图片添加文字水印
4. 批量提取图片EXIF信息

适用于需要更精细控制和反馈的场景。
"""
# 导入所需的函数和模块
from file_batch_tool import batch_rename, batch_watermark, batch_extract_exif
from datetime import datetime
from pathlib import Path


def custom_log_callback(msg):
    """
    自定义日志回调函数
    
    这个函数会被 file_batch_tool 中的函数调用，
    用于处理日志消息和进度更新。
    
    参数:
        msg: 日志消息字符串
        
    消息类型:
        - 普通日志: 直接输出
        - 进度消息: 以 "progress:" 开头，后面跟百分比
    """
    if msg.startswith("progress:"):
        # 处理进度消息，显示进度条
        try:
            progress = int(msg.split(":")[1])
            bar_length = 50
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"\r处理进度: [{bar}] {progress}%", end="", flush=True)
        except (ValueError, IndexError):
            print(f"\r[进度] {msg}", end="", flush=True)
    else:
        # 处理普通日志消息
        print(f"\n{msg}")


def example_with_progress():
    """
    带进度回调的示例
    
    这个示例演示如何：
    1. 使用自定义回调函数
    2. 显示实时处理进度
    3. 提供更好的用户体验
    """
    print("=" * 60)
    print("示例：带进度回调的批量处理")
    print("=" * 60)
    print("\n说明：使用自定义回调函数显示处理进度")
    
    test_dir = Path("test_files")
    
    # 确保测试目录存在并有文件
    if not test_dir.exists():
        test_dir.mkdir(exist_ok=True)
        print(f"\n📁 创建测试目录: {test_dir.absolute()}")
        # 创建一些测试文件
        for i in range(5):
            (test_dir / f"file_{i:02d}.txt").touch()
        print("📄 测试文件创建完成！")
    
    # 执行带进度回调的重命名
    batch_rename(
        dir_path=str(test_dir),
        prefix="processed_",
        log_callback=custom_log_callback
    )
    
    print("\n✅ 处理完成！")


def example_watermark():
    """
    添加水印示例
    
    这个示例演示如何：
    1. 为图片添加文字水印
    2. 自定义水印样式（大小、颜色、透明度）
    
    支持两种水印类型:
        - "text": 文字水印
        - "image": 图片水印
        
    文字水印参数:
        - content: 水印文字内容
        - size: 字体大小
        - color: 文字颜色（支持 RGB/RGBA 格式）
        - opacity: 透明度（0-255）
        - font: 字体文件路径（可选）
    """
    print("\n" + "=" * 60)
    print("示例：批量添加水印")
    print("=" * 60)
    print("\n说明：为图片添加文字或图片水印")
    
    # 取消下面的注释来运行示例
    """
    # 文字水印示例
    print("🖼️  添加文字水印...")
    batch_watermark(
        dir_path="/path/to/your/images",  # 修改为您的图片目录
        type_="text",
        content="© My Photo",             # 水印文字
        size=40,                           # 字体大小
        color="(255,255,255,128)",         # 半透明白色
        opacity=128,                       # 透明度
        log_callback=custom_log_callback   # 使用自定义日志
    )
    
    # 图片水印示例
    print("🖼️  添加图片水印...")
    batch_watermark(
        dir_path="/path/to/your/images",
        type_="image",
        watermark_path="/path/to/logo.png",  # 水印图片路径
        size=100,                            # 水印大小
        opacity=100,                         # 透明度
        log_callback=custom_log_callback
    )
    """
    
    print("💡 提示：请准备图片目录后取消注释运行此示例")


def example_extract_exif():
    """
    提取EXIF示例
    
    这个示例演示如何：
    1. 批量提取图片EXIF信息
    2. 将信息导出为CSV文件
    3. 包含图片尺寸、拍摄时间、设备型号等信息
    
    提取的信息包括:
        - 文件名和路径
        - 图片尺寸（宽度、高度）
        - 拍摄时间
        - 相机/手机型号
        - GPS信息（如果有）
    """
    print("\n" + "=" * 60)
    print("示例：批量提取EXIF信息")
    print("=" * 60)
    print("\n说明：从图片中提取EXIF信息并导出为CSV")
    
    # 取消下面的注释来运行示例
    """
    print("📊 正在提取EXIF信息...")
    output_file = Path("exif_data.csv")
    
    batch_extract_exif(
        dir_path="/path/to/your/images",  # 修改为您的图片目录
        output_csv=str(output_file),
        log_callback=custom_log_callback
    )
    
    print(f"\n✅ EXIF信息已导出到: {output_file.absolute()}")
    print("📋 CSV文件包含：文件名、尺寸、拍摄时间、设备型号等信息")
    """
    
    print("💡 提示：请准备图片目录后取消注释运行此示例")


def example_multiple_tasks():
    """
    多任务处理示例
    
    这个示例演示如何：
    1. 按顺序执行多个处理任务
    2. 每个任务都有独立的日志回调
    3. 实现完整的图片处理工作流
    """
    print("\n" + "=" * 60)
    print("示例：组合多个处理任务")
    print("=" * 60)
    print("\n说明：按顺序执行多个文件处理任务")
    
    print("\n📋 完整工作流示例:")
    print("   1. 批量重命名文件")
    print("   2. 添加水印")
    print("   3. 提取EXIF信息")
    print("\n💡 您可以根据需要组合不同的功能！")


def main():
    """
    主函数：运行所有高级用法示例
    """
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "高级用法示例" + " " * 36 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # 运行所有示例
    example_with_progress()
    example_watermark()
    example_extract_exif()
    example_multiple_tasks()
    
    print("\n" + "=" * 60)
    print("🎉 所有高级示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
