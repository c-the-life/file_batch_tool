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
"""

import os
import re
import argparse
import zipfile
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont

# 解决PIL处理大图片的DecompressionBombWarning
Image.MAX_IMAGE_PIXELS = None

# --- 批量重命名 ---
def batch_rename(args):
    file_list = [f for f in Path(args.dir).glob("*") if f.is_file()]
    if not file_list:
        print(f"❌ 目录 {args.dir} 下未找到文件")
        return

    pattern = re.compile(args.pattern) if args.pattern else None
    rename_count = 0

    print(f"📝 开始批量重命名，共找到 {len(file_list)} 个文件")
    for file_path in tqdm(file_list):
        old_name = file_path.name
        new_name = old_name

        if pattern:
            new_name = pattern.sub(args.replace, new_name)
        if args.prefix:
            new_name = args.prefix + new_name
        if args.suffix:
            name, ext = os.path.splitext(new_name)
            new_name = f"{name}{args.suffix}{ext}"

        if new_name == old_name:
            continue

        new_path = file_path.parent / new_name
        if new_path.exists():
            print(f"\n⚠️ 文件 {new_path} 已存在，跳过")
            continue

        file_path.rename(new_path)
        rename_count += 1

    print(f"✅ 重命名完成，共处理 {rename_count} 个文件")

# --- 批量转换图片格式（终极修复版）---
def batch_convert_image(args):
    """批量转换图片格式（全兼容版）"""
    # 支持的图片格式
    SUPPORT_FORMATS = ["jpg", "jpeg", "png", "webp"]
    # 目标格式统一为小写
    target_format = args.to_format.lower()
    
    # 获取目标目录下的图片文件
    img_list = []
    for ext in SUPPORT_FORMATS:
        img_list.extend(Path(args.dir).glob(f"*.{ext}"))
        img_list.extend(Path(args.dir).glob(f"*.{ext.upper()}"))  # 兼容大写扩展名
    img_list = [f for f in img_list if f.is_file()]

    if not img_list:
        print(f"❌ 目录 {args.dir} 下未找到支持的图片文件（{SUPPORT_FORMATS}）")
        return

    convert_count = 0
    print(f"🖼️ 开始批量转换图片格式，共找到 {len(img_list)/2} 张图片")
    
    for img_path in tqdm(img_list):
        try:
            # 打开图片并处理模式
            with Image.open(img_path) as img:
                # 1. 处理JPG不支持透明通道的问题
                if target_format in ["jpg", "jpeg"]:
                    # 转换为RGB模式，透明区域填充白色
                    if img.mode in ("RGBA", "P"):
                        bg = Image.new("RGB", img.size, (255, 255, 255))
                        # 处理mask兼容问题
                        mask = img.split()[-1] if img.mode == "RGBA" else None
                        bg.paste(img, (0, 0), mask)
                        img = bg
                    else:
                        img = img.convert("RGB")
                else:
                    # PNG/WebP保留透明通道
                    img = img.convert("RGBA") if img.mode != "RGBA" else img

                # 2. 拼接新文件名（避免重复）
                new_name = f"{img_path.stem}_converted.{target_format}"
                new_path = img_path.parent / new_name
                
                # 3. 兼容Pillow的格式参数
                format_map = {
                    "jpg": "JPEG",
                    "jpeg": "JPEG",
                    "png": "PNG",
                    "webp": "WEBP"
                }
                save_format = format_map.get(target_format, target_format.upper())

                # 4. 保存图片（处理权限问题）
                img.save(new_path, save_format, quality=95)
                convert_count += 1
                
        except PermissionError:
            print(f"\n⚠️ 无权限写入 {new_path}，请关闭该文件后重试")
        except Exception as e:
            print(f"\n⚠️ 处理 {img_path.name} 失败：{str(e)}")
            continue

    print(f"✅ 图片转换完成，共成功处理 {convert_count/2} 张图片")

# --- 批量压缩文件 ---
def batch_compress(args):
    file_list = [f for f in Path(args.dir).glob("*") if f.is_file()]
    if args.exclude:
        exclude_exts = [ext.strip() for ext in args.exclude.split(",")]
        file_list = [f for f in file_list if f.suffix.lstrip(".") not in exclude_exts]

    if not file_list:
        print(f"❌ 目录 {args.dir} 下未找到可压缩的文件")
        return

    zip_name = args.output if args.output else f"{args.dir}_compressed.zip"
    zip_path = Path(zip_name)
    if zip_path.exists():
        print(f"❌ ZIP包 {zip_path} 已存在，请更换输出文件名")
        return

    print(f"📦 开始批量压缩文件，共找到 {len(file_list)} 个文件")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in tqdm(file_list):
            zipf.write(file_path, arcname=file_path.name)

    print(f"✅ 压缩完成！ZIP包已保存至：{zip_path.absolute()}")

# --- 批量文件分类 ---
def batch_classify(args):
    file_list = [f for f in Path(args.dir).glob("*") if f.is_file()]
    if not file_list:
        print(f"❌ 目录 {args.dir} 下无文件")
        return

    classify_dir = Path(args.dir) / "classified"
    classify_dir.mkdir(exist_ok=True)
    count = 0

    print(f"📂 开始批量分类，共 {len(file_list)} 个文件")
    for file_path in tqdm(file_list):
        if args.mode == "ext":
            ext = file_path.suffix.lstrip(".").lower() or "no_ext"
            target_dir = classify_dir / ext
        elif args.mode == "date":
            ctime = datetime.fromtimestamp(file_path.stat().st_ctime)
            date_str = ctime.strftime("%Y-%m")
            target_dir = classify_dir / date_str
        else:
            print(f"⚠️ 不支持的分类模式：{args.mode}")
            return

        target_dir.mkdir(exist_ok=True)
        try:
            file_path.rename(target_dir / file_path.name)
            count += 1
        except Exception as e:
            print(f"\n⚠️ 移动 {file_path.name} 失败：{str(e)}")
            continue

    print(f"✅ 分类完成，共处理 {count} 个文件，已归档至 {classify_dir}")

# --- 图片批量加水印 ---
def batch_watermark(args):
    SUPPORT_FORMATS = ["jpg", "jpeg", "png", "webp"]
    img_list = []
    for ext in SUPPORT_FORMATS:
        img_list.extend(Path(args.dir).glob(f"*.{ext}"))
    img_list = [f for f in img_list if f.is_file()]

    if not img_list:
        print(f"❌ 目录 {args.dir} 下无支持的图片")
        return

    count = 0
    print(f"🔖 开始批量添加水印，共 {len(img_list)} 张图片")

    if args.type == "text":
        color = eval(args.color) if args.color else (255, 255, 255, 128)
        try:
            font = ImageFont.truetype(args.font, args.size) if args.font else ImageFont.load_default()
        except:
            font = ImageFont.load_default()
    elif args.type == "image":
        try:
            watermark_img = Image.open(args.watermark_path).convert("RGBA")
            watermark_img = watermark_img.resize((args.size, args.size), Image.Resampling.LANCZOS)
            alpha = watermark_img.split()[3]
            alpha = alpha.point(lambda p: p * args.opacity / 255)
            watermark_img.putalpha(alpha)
        except Exception as e:
            print(f"❌ 加载图片水印失败：{str(e)}")
            return
    else:
        print(f"⚠️ 不支持的水印类型：{args.type}")
        return

    for img_path in tqdm(img_list):
        try:
            img = Image.open(img_path).convert("RGBA")
            draw = ImageDraw.Draw(img)
            width, height = img.size

            if args.type == "text":
                text_bbox = draw.textbbox((0, 0), args.content, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                pos = (width - text_width - 20, height - text_height - 20)
                draw.text(pos, args.content, font=font, fill=color)
            elif args.type == "image":
                pos = (width - args.size - 20, height - args.size - 20)
                img.paste(watermark_img, pos, mask=watermark_img)

            new_path = img_path.parent / f"watermarked_{img_path.name}"
            if img_path.suffix.lower() in (".jpg", ".jpeg"):
                img.convert("RGB").save(new_path, "JPEG")
            else:
                img.save(new_path, img_path.suffix[1:].upper())
            count += 1
        except Exception as e:
            print(f"\n⚠️ 处理 {img_path.name} 失败：{str(e)}")
            continue

    print(f"✅ 水印添加完成，共处理 {count} 张图片")

# --- 主函数 ---
def main():
    parser = argparse.ArgumentParser(
        description="📁 文件批量处理工具 | 支持重命名/图片转换/压缩/分类/加水印",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令（必选）")

    # 1. 重命名子命令（修复转义字符警告）
    parser_rename = subparsers.add_parser("rename", help="批量重命名文件")
    parser_rename.add_argument("-d", "--dir", required=True, help="目标目录（如 ./test）")
    parser_rename.add_argument("-p", "--pattern", help=r"正则匹配模式（如 'img_(\d+)'）")
    parser_rename.add_argument("-r", "--replace", help="正则替换内容（如 'photo_\\1'）")
    parser_rename.add_argument("--prefix", help="添加前缀（如 '2024_'）")
    parser_rename.add_argument("--suffix", help="添加后缀（如 '_v1'）")

    # 2. 图片转换子命令
    parser_img = subparsers.add_parser("convert-img", help="批量转换图片格式")
    parser_img.add_argument("-d", "--dir", required=True, help="目标目录（如 ./images）")
    parser_img.add_argument("-f", "--to-format", required=True, help="目标格式（jpg/png/webp）")

    # 3. 压缩子命令
    parser_zip = subparsers.add_parser("compress", help="批量压缩文件为ZIP")
    parser_zip.add_argument("-d", "--dir", required=True, help="目标目录（如 ./files）")
    parser_zip.add_argument("-o", "--output", help="输出ZIP文件名（默认：{dir}_compressed.zip）")
    parser_zip.add_argument("--exclude", help="排除的扩展名（逗号分隔，如 'zip,log'）")

    # 4. 分类子命令
    parser_classify = subparsers.add_parser("classify", help="批量分类文件（按扩展名/日期）")
    parser_classify.add_argument("-d", "--dir", required=True, help="目标目录")
    parser_classify.add_argument("-m", "--mode", required=True, choices=["ext", "date"], help="分类模式：ext（扩展名）/ date（日期）")

    # 5. 水印子命令
    parser_watermark = subparsers.add_parser("watermark", help="批量添加图片水印（文字/图片）")
    parser_watermark.add_argument("-d", "--dir", required=True, help="图片目录")
    parser_watermark.add_argument("-t", "--type", required=True, choices=["text", "image"], help="水印类型")
    parser_watermark.add_argument("-c", "--content", help="文字水印内容（type=text时必填）")
    parser_watermark.add_argument("-f", "--font", help="文字水印字体路径（可选，默认系统字体）")
    parser_watermark.add_argument("-s", "--size", type=int, default=24, help="水印大小（文字字号/图片尺寸，默认24）")
    parser_watermark.add_argument("-color", "--color", default="(255,255,255,128)", help="文字水印颜色（RGBA，默认白色半透明：(255,255,255,128)）")
    parser_watermark.add_argument("-o", "--opacity", type=int, default=128, help="水印透明度（0-255，默认128）")
    parser_watermark.add_argument("-w", "--watermark-path", help="图片水印路径（type=image时必填）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return
    if hasattr(args, "dir") and not Path(args.dir).exists():
        print(f"❌ 目录 {args.dir} 不存在")
        return
    if args.command == "watermark":
        if args.type == "text" and not args.content:
            print(f"❌ type=text时，必须指定 --content 文字内容")
            return
        if args.type == "image" and not args.watermark_path:
            print(f"❌ type=image时，必须指定 --watermark-path 图片路径")
            return

    try:
        if args.command == "rename":
            batch_rename(args)
        elif args.command == "convert-img":
            batch_convert_image(args)
        elif args.command == "compress":
            batch_compress(args)
        elif args.command == "classify":
            batch_classify(args)
        elif args.command == "watermark":
            batch_watermark(args)
    except Exception as e:
        print(f"\n❌ 执行失败：{str(e)}")

if __name__ == "__main__":
    main()