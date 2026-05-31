"""
示例 2：图片格式转换
演示如何批量转换图片格式

本示例展示了：
1. 批量将图片转换为 WebP 格式（推荐用于网页，体积小）
2. 批量将图片转换为 JPG 格式（兼容性好）
3. 转换单个文件的用法

支持的格式：
- jpg/jpeg - 联合图像专家组格式
- png - 便携式网络图形（支持透明）
- webp - Google 推出的现代图片格式（推荐）
"""
# 导入所需的函数
from file_batch_tool import batch_convert_image


def example_convert_to_webp():
    """
    转换为 WebP 格式（推荐用于网页）
    
    WebP 格式的优势：
    - 比 JPEG 小 25-35%
    - 比 PNG 小 26%
    - 支持透明度和动画
    - 现代浏览器广泛支持
    
    适用场景：
    - 网站图片优化
    - 移动应用图片
    - 节省存储空间
    """
    print("=" * 60)
    print("示例：批量转换为 WebP 格式")
    print("=" * 60)
    print("\n说明：WebP 是现代图片格式，能显著减小文件大小")
    
    # 执行批量转换
    batch_convert_image(
        dir_path="./photos",
        to_format="webp"
    )
    
    print("\n✅ 转换完成！生成的文件带有 _converted.webp 后缀")


def example_convert_to_jpg():
    """
    转换为 JPG 格式
    
    JPG 格式的特点：
    - 兼容性最好，几乎所有设备都支持
    - 不支持透明度
    - 有损压缩，文件较小
    
    适用场景：
    - 照片和复杂图像
    - 需要广泛兼容性
    - 不需要透明背景
    """
    print("\n" + "=" * 60)
    print("示例：批量转换为 JPG 格式")
    print("=" * 60)
    print("\n说明：JPG 是最通用的图片格式")
    
    # 执行批量转换
    batch_convert_image(
        dir_path="./photos",
        to_format="jpg"
    )
    
    print("\n✅ 转换完成！生成的文件带有 _converted.jpg 后缀")


def example_convert_to_png():
    """
    转换为 PNG 格式
    
    PNG 格式的特点：
    - 支持透明度（alpha 通道）
    - 无损压缩
    - 文件通常比 JPG 大
    
    适用场景：
    - 需要透明背景
    - Logo 和图标
    - 简单图形
    """
    print("\n" + "=" * 60)
    print("示例：批量转换为 PNG 格式")
    print("=" * 60)
    print("\n说明：PNG 支持透明背景，适合图标和 Logo")
    
    # 执行批量转换
    batch_convert_image(
        dir_path="./photos",
        to_format="png"
    )
    
    print("\n✅ 转换完成！生成的文件带有 _converted.png 后缀")


def example_single_file():
    """
    转换单个文件
    
    除了批量处理整个目录，
    也可以只转换单个文件。
    """
    print("\n" + "=" * 60)
    print("示例：转换单个文件")
    print("=" * 60)
    print("\n说明：可以指定单个文件路径进行转换")
    
    # 转换单个文件
    batch_convert_image(
        dir_path="./photos/photo.png",
        to_format="jpg"
    )
    
    print("\n✅ 单个文件转换完成！")


def main():
    """
    主函数：运行所有示例
    
    会先检查测试目录是否存在，
    如果不存在会创建并提示用户添加图片。
    """
    import os
    from pathlib import Path
    
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "图片格式转换示例" + " " * 30 + "║")
    print("╚" + "=" * 58 + "╝")
    
    test_dir = Path("./photos")
    
    # 检查测试目录
    if not test_dir.exists():
        test_dir.mkdir(exist_ok=True)
        print(f"\n📁 已创建测试目录: {test_dir.absolute()}")
        print("💡 请在该目录中放入一些图片后运行示例")
        print("   支持的格式：JPG, PNG, WebP")
    else:
        # 检查目录中是否有图片文件
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        has_images = any(
            file.suffix.lower() in image_extensions
            for file in test_dir.iterdir()
            if file.is_file()
        )
        
        if has_images:
            # 运行示例
            print(f"\n✅ 在 {test_dir} 中找到图片文件")
            
            # 运行所有转换示例
            example_convert_to_webp()
            example_convert_to_jpg()
            example_convert_to_png()
            
            print("\n" + "=" * 60)
            print("🎉 所有示例运行完成！")
            print("=" * 60)
        else:
            print(f"\n⚠️  在 {test_dir} 中未找到图片文件")
            print("💡 请先添加一些图片到该目录")


if __name__ == "__main__":
    main()
