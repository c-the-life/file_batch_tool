"""
示例 3：批量添加水印
演示如何使用 file_batch_tool 为图片批量添加水印

本示例展示了：
1. 为图片添加文字水印
2. 为图片添加图片水印
3. 自定义水印样式（大小、颜色、透明度、位置）

水印类型：
- 文字水印：使用自定义文字作为水印
- 图片水印：使用图片作为水印（如Logo）

适用场景：
- 为照片添加版权信息
- 为产品图片添加品牌Logo
- 为文档添加保密标识
- 批量处理产品图片
"""
from file_batch_tool import batch_watermark
from pathlib import Path


def example_text_watermark():
    """
    文字水印示例
    
    这个示例演示如何：
    1. 为图片添加文字水印
    2. 自定义水印文字、大小、颜色
    3. 调整水印透明度
    
    参数说明：
    - type_: 水印类型，"text" 表示文字水印
    - content: 水印文字内容
    - size: 水印大小（文字大小或图片缩放）
    - color: 文字颜色（支持 RGB/RGBA）
    - opacity: 透明度（0-255）
    - position: 水印位置（top-left/top-right/bottom-left/bottom-right/center）
    """
    print("=" * 60)
    print("示例：文字水印")
    print("=" * 60)
    print("\n说明：为图片添加自定义文字水印")
    
    # 取消下面的注释来运行示例
    """
    print("🖼️  添加文字水印...")
    batch_watermark(
        dir_path="./test_images",              # 图片目录
        type_="text",                          # 文字水印
        content="© My Photos",                 # 水印文字
        size=50,                               # 字体大小
        color="(255,255,255,180)",             # 半透明白色
        opacity=180,                           # 透明度
        position="bottom-right"                # 右下角位置
    )
    print("\n✅ 文字水印添加完成！")
    """
    
    print("💡 提示：请准备图片目录后取消注释运行此示例")


def example_image_watermark():
    """
    图片水印示例
    
    这个示例演示如何：
    1. 为图片添加图片水印（Logo）
    2. 自定义水印大小和透明度
    3. 选择水印位置
    
    参数说明：
    - type_: 水印类型，"image" 表示图片水印
    - watermark_path: 水印图片路径（支持 PNG、JPG 等）
    - size: 水印大小（缩放尺寸）
    - opacity: 透明度（0-255）
    - position: 水印位置
    """
    print("\n" + "=" * 60)
    print("示例：图片水印")
    print("=" * 60)
    print("\n说明：为图片添加图片水印（如Logo）")
    
    # 取消下面的注释来运行示例
    """
    print("🖼️  添加图片水印...")
    batch_watermark(
        dir_path="./test_images",              # 图片目录
        type_="image",                         # 图片水印
        watermark_path="./logo.png",           # 水印图片路径
        size=150,                              # 水印大小
        opacity=150,                           # 透明度
        position="top-right"                   # 右上角位置
    )
    print("\n✅ 图片水印添加完成！")
    """
    
    print("💡 提示：请准备图片和水印图片后取消注释运行此示例")


def example_center_watermark():
    """
    居中水印示例
    
    这个示例演示如何：
    1. 在图片中心添加大水印
    2. 使用低透明度作为防伪标识
    """
    print("\n" + "=" * 60)
    print("示例：居中防伪水印")
    print("=" * 60)
    print("\n说明：在图片中心添加低透明度的大水印")
    
    # 取消下面的注释来运行示例
    """
    print("🖼️  添加居中水印...")
    batch_watermark(
        dir_path="./test_images",
        type_="text",
        content="CONFIDENTIAL",
        size=80,
        color="(128,128,128,80)",           # 低透明度灰色
        opacity=80,
        position="center"                    # 居中
    )
    print("\n✅ 居中水印添加完成！")
    """
    
    print("💡 提示：请准备图片目录后取消注释运行此示例")


def main():
    """
    主函数：运行所有水印示例
    """
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "批量添加水印示例" + " " * 32 + "║")
    print("╚" + "=" * 58 + "╝")
    
    test_dir = Path("./test_images")
    if not test_dir.exists():
        test_dir.mkdir(exist_ok=True)
        print(f"\n📁 创建测试目录: {test_dir.absolute()}")
        print("💡 请在该目录中放入一些图片后运行示例")
    
    # 运行所有示例
    example_text_watermark()
    example_image_watermark()
    example_center_watermark()
    
    print("\n" + "=" * 60)
    print("🎉 所有水印示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()