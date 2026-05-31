"""
示例 1：基础批量重命名
演示如何使用 file_batch_tool 进行简单的批量重命名操作

本示例展示了：
1. 简单的批量重命名（添加前缀和替换字符串）
2. 使用自定义日志回调函数
3. 如何处理进度消息和普通日志消息

适用场景：
- 整理杂乱的文件名
- 统一命名规范
- 批量添加标识前缀/后缀
- 批量替换文件名中的特定字符串
"""
# 导入批量重命名函数
from file_batch_tool import batch_rename


def example_simple_rename():
    """
    简单重命名示例
    
    这个示例演示如何：
    1. 为所有文件添加统一前缀
    2. 批量替换文件名中的特定字符串
    
    参数说明：
    - prefix: 添加到文件名前面的前缀
    - suffix: 添加到文件名后面的后缀（扩展名前）
    - find_str: 要查找并替换的字符串
    - replace_str: 替换后的字符串
    """
    print("=" * 60)
    print("示例：简单批量重命名")
    print("=" * 60)
    print("\n说明：为文件添加前缀并替换特定字符串")
    
    # 重命名文件夹中的所有文件
    batch_rename(
        dir_path="./test_images",
        prefix="vacation_",          # 添加前缀 "vacation_"
        find_str="img",              # 查找 "img" 字符串
        replace_str="photo"          # 替换为 "photo"
    )
    
    print("\n✅ 重命名完成！")
    print("   文件名变化示例: img_001.jpg -> vacation_photo_001.jpg")


def example_with_logger():
    """
    带自定义日志回调的示例
    
    这个示例演示如何：
    1. 创建自定义日志回调函数
    2. 区分处理进度消息和普通日志消息
    3. 自定义日志输出格式
    
    日志消息格式：
    - 普通消息: 直接输出内容
    - 进度消息: 以 "progress:" 开头，后面跟进度百分比
    """
    print("\n" + "=" * 60)
    print("示例：自定义日志回调")
    print("=" * 60)
    print("\n说明：使用自定义函数处理日志和进度")
    
    def custom_log(msg):
        """
        自定义日志回调函数
        
        参数:
            msg: 日志消息字符串
        """
        if msg.startswith("progress:"):
            # 处理进度消息
            try:
                progress = int(msg.split(":")[1])
                # 创建进度条
                bar_length = 40
                filled = int(bar_length * progress / 100)
                bar = "█" * filled + "░" * (bar_length - filled)
                print(f"\r处理进度: [{bar}] {progress}%", end="", flush=True)
            except (ValueError, IndexError):
                print(f"\r[进度] {msg}", end="", flush=True)
        else:
            # 处理普通日志消息
            print(f"\n[LOG] {msg}")
    
    # 执行带日志回调的重命名
    batch_rename(
        dir_path="./test_images",
        suffix="_processed",          # 添加后缀 "_processed"
        log_callback=custom_log       # 使用自定义日志回调
    )
    
    print("\n✅ 带日志的重命名完成！")


def example_add_prefix_only():
    """
    仅添加前缀的示例
    
    适用于需要为一组文件统一添加标识的场景，
    比如按日期、项目名、分类等组织文件。
    """
    print("\n" + "=" * 60)
    print("示例：仅添加前缀")
    print("=" * 60)
    print("\n说明：只为文件添加前缀，不做其他修改")
    
    batch_rename(
        dir_path="./test_images",
        prefix="2024_",               # 添加年份前缀
        find_str="",                  # 不进行字符串替换
        replace_str=""
    )
    
    print("\n✅ 前缀添加完成！")


def example_add_suffix_only():
    """
    仅添加后缀的示例
    
    适用于标记文件状态，比如标记为已处理、备份、临时等。
    """
    print("\n" + "=" * 60)
    print("示例：仅添加后缀")
    print("=" * 60)
    print("\n说明：只为文件添加后缀，不做其他修改")
    
    batch_rename(
        dir_path="./test_images",
        suffix="_backup",             # 添加备份后缀
        find_str="",                  # 不进行字符串替换
        replace_str=""
    )
    
    print("\n✅ 后缀添加完成！")


def main():
    """
    主函数：运行所有示例
    
    会先检查测试目录是否存在，
    如果不存在会创建并提示用户添加文件。
    """
    import os
    from pathlib import Path
    
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "基础批量重命名示例" + " " * 28 + "║")
    print("╚" + "=" * 58 + "╝")
    
    test_dir = Path("./test_images")
    
    # 检查测试目录
    if not test_dir.exists():
        test_dir.mkdir(exist_ok=True)
        print(f"\n📁 已创建测试目录: {test_dir.absolute()}")
        print("💡 请在该目录中放入一些测试文件后运行示例")
        
        # 创建一些示例文件供测试
        print("\n📄 正在创建示例文件...")
        for i in range(3):
            sample_file = test_dir / f"img_{i:03d}.txt"
            sample_file.touch()
            print(f"   - 创建: {sample_file.name}")
        print("✅ 示例文件创建完成！")
        
        # 现在运行示例
        example_simple_rename()
        example_with_logger()
    else:
        # 检查目录中是否有文件
        has_files = any(
            file.is_file()
            for file in test_dir.iterdir()
        )
        
        if has_files:
            print(f"\n✅ 在 {test_dir} 中找到文件")
            
            # 运行所有示例
            example_simple_rename()
            example_with_logger()
            example_add_prefix_only()
            example_add_suffix_only()
            
            print("\n" + "=" * 60)
            print("🎉 所有示例运行完成！")
            print("=" * 60)
        else:
            print(f"\n⚠️  在 {test_dir} 中未找到文件")
            print("💡 请先添加一些文件到该目录，或运行程序自动创建示例文件")


if __name__ == "__main__":
    main()
