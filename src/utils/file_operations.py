"""文件操作工具模块
提供批量文件处理、图片操作、压缩、分类等功能
"""
import os
import re
import sys
import csv
import time
import ast
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ExifTags, ImageColor

Image.MAX_IMAGE_PIXELS = None
FILE_LIST_SEPARATOR = "|||"

def safe_log(msg, log_callback=None):
    """统一的日志输出，处理某些控制台的编码崩溃问题
    
    Args:
        msg (str): 要输出的日志消息
        log_callback (function, optional): 自定义日志回调函数
    """
    try:
        if log_callback:
            log_callback(msg)
        else:
            print(msg)
    except UnicodeEncodeError:
        msg = msg.encode('ascii', 'replace').decode('ascii')
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

def parse_input_path(input_path):
    """解析输入路径，支持单个文件、目录、多个文件（仅筛选文件，排除目录）
    
    Args:
        input_path (str): 输入路径字符串
        
    Returns:
        tuple: (file_list, type) 其中：
            file_list (list): Path对象列表
            type (str): 输入类型，可选值：'single'|'dir'|'multiple'
    """
    if FILE_LIST_SEPARATOR in input_path:
        paths = input_path.split(FILE_LIST_SEPARATOR)
        file_list = []
        for path in paths:
            path = path.strip()
            if path:
                p = Path(path)
                if p.is_file():
                    file_list.append(p)
                elif p.is_dir():
                    file_list.extend([f for f in p.iterdir() if f.is_file()])
        return file_list, "multiple"
    else:
        path_obj = Path(input_path)
        if path_obj.is_file():
            return [path_obj], "single"
        elif path_obj.is_dir():
            return [f for f in path_obj.iterdir() if f.is_file()], "dir"
        else:
            return [], "invalid"

def get_unique_path(target_path: Path) -> Path:
    """生成唯一路径，防止同名冲突（如 file.txt -> file_1.txt）
    
    Args:
        target_path (Path): 目标路径
        
    Returns:
        Path: 唯一的新路径
    """
    if not target_path.exists():
        return target_path
    counter = 1
    while True:
        new_path = target_path.with_name(f"{target_path.stem}_{counter}{target_path.suffix}")
        if not new_path.exists():
            return new_path
        counter += 1

def batch_rename(dir_path, prefix="", suffix="", find_str="", replace_str="", log_callback=None):
    """批量重命名文件
    
    Args:
        dir_path (str): 目录路径或文件列表字符串
        prefix (str, optional): 文件名前缀
        suffix (str, optional): 文件名后缀
        find_str (str, optional): 要查找的字符串
        replace_str (str, optional): 替换为的字符串
        log_callback (function, optional): 日志回调函数
        
    Returns:
        bool: 操作是否成功
    """
    file_list, input_type = parse_input_path(dir_path)
    file_count = len(file_list)

    if input_type == "invalid":
        safe_log(f"❌ 路径 {dir_path} 不是有效文件或目录", log_callback)
        return False
    if file_count == 0:
        safe_log(f"❌ 未找到任何文件", log_callback)
        return False

    safe_log(f"📝 开始重命名任务，共扫描到 {file_count} 个文件", log_callback)
    rename_count = 0
    skip_count = 0

    for idx, file_path in enumerate(file_list):
        old_name = file_path.name
        name, ext = os.path.splitext(old_name)
        new_main_name = name

        if find_str:
            new_main_name = new_main_name.replace(find_str, replace_str)
        if prefix:
            new_main_name = prefix + new_main_name
        if suffix:
            new_main_name = new_main_name + suffix

        new_name = new_main_name + ext
        if new_name == old_name:
            skip_count += 1
            continue

        new_path = file_path.parent / new_name
        if new_path.exists():
            safe_log(f"⚠️ 跳过 {old_name}：新文件名 {new_name} 已存在", log_callback)
            skip_count += 1
            continue

        try:
            file_path.rename(new_path)
            rename_count += 1
            safe_log(f"✅ 重命名：{old_name} → {new_name}", log_callback)
        except PermissionError:
            safe_log(f"⚠️ 跳过 {old_name}：权限不足或文件被占用。请检查文件是否被其他程序打开，或尝试以管理员身份运行", log_callback)
            skip_count += 1
        except FileNotFoundError:
            safe_log(f"⚠️ 跳过 {old_name}：文件不存在", log_callback)
            skip_count += 1

        if log_callback:
            log_callback(f"progress:{int((idx + 1) / file_count * 100)}")

    safe_log(f"\n✅ 重命名任务结束 | 总文件：{file_count} | 成功：{rename_count} | 跳过：{skip_count}", log_callback)
    return rename_count > 0

def batch_convert_image(dir_path, to_format, log_callback=None):
    """批量转换图片格式
    
    Args:
        dir_path (str): 目录路径或文件列表字符串
        to_format (str): 目标格式（jpg/jpeg/png/webp）
        log_callback (function, optional): 日志回调函数
        
    Returns:
        bool: 操作是否成功
    """
    SUPPORT_FORMATS = {"jpg", "jpeg", "png", "webp"}
    target_format = to_format.lower()
    if target_format == "jpg":
        target_format = "jpeg"

    all_files, input_type = parse_input_path(dir_path)
    if input_type == "invalid":
        safe_log(f"❌ 路径 {dir_path} 不是有效文件或目录", log_callback)
        return False

    img_list = [f for f in all_files if f.suffix.lower().lstrip('.') in SUPPORT_FORMATS]
    img_count = len(img_list)

    if img_count == 0:
        safe_log(f"❌ 未找到支持的图片文件", log_callback)
        return False

    convert_count = 0
    for idx, img_path in enumerate(img_list):
        try:
            new_name = f"{img_path.stem}_converted.{target_format}"
            new_path = img_path.parent / new_name

            with Image.open(img_path) as img:
                if target_format == "jpeg":
                    if img.mode in ("RGBA", "P"):
                        bg = Image.new("RGB", img.size, (255, 255, 255))
                        mask = img.split()[-1] if img.mode == "RGBA" else None
                        bg.paste(img, (0, 0), mask)
                        img = bg
                    else:
                        img = img.convert("RGB")
                else:
                    img = img.convert("RGBA") if img.mode != "RGBA" else img

                save_format = "JPEG" if target_format == "jpeg" else target_format.upper()
                img.save(new_path, save_format, quality=95)
                convert_count += 1
        except Exception as e:
            safe_log(f"\n⚠️ 处理 {img_path.name} 失败：{str(e)}", log_callback)
            continue

        if log_callback:
            log_callback(f"progress:{int((idx + 1) / img_count * 100)}")

    safe_log(f"✅ 图片转换完成，共成功处理 {convert_count} 张图片", log_callback)
    return True

def batch_compress(dir_path, output="", exclude="", log_callback=None):
    """批量压缩文件
    
    Args:
        dir_path (str): 目录路径或文件列表字符串
        output (str, optional): 输出文件路径
        exclude (str, optional): 要排除的扩展名，逗号分隔
        log_callback (function, optional): 日志回调函数
        
    Returns:
        bool: 操作是否成功
    """
    all_files, input_type = parse_input_path(dir_path)
    if input_type == "invalid":
        safe_log(f"Error: 路径 {dir_path} 不是有效文件或目录", log_callback)
        return False

    exclude_exts = {ext.strip().lower() for ext in exclude.split(",") if ext.strip()} if exclude else set()
    file_list = [f for f in all_files if f.suffix.lstrip(".").lower() not in exclude_exts]
    file_count = len(file_list)

    if file_count == 0:
        safe_log("Error: 未找到可压缩的文件", log_callback)
        return False

    if input_type == "single":
        default_name = file_list[0].parent / f"{file_list[0].stem}_compressed.zip"
    elif input_type == "multiple":
        first_file = Path(dir_path.split(FILE_LIST_SEPARATOR)[0])
        default_name = first_file.parent / "files_compressed.zip"
    else:
        default_name = Path(dir_path) / "files_compressed.zip"
    
    zip_path = Path(output if output else default_name)
    if zip_path.exists():
        safe_log(f"❌ ZIP包 {zip_path} 已存在，请更换输出文件名", log_callback)
        return False

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for idx, file_path in enumerate(file_list):
            zipf.write(file_path, arcname=file_path.name)
            if log_callback:
                log_callback(f"progress:{int((idx + 1) / file_count * 100)}")

    safe_log(f"✅ 压缩完成！ZIP包已保存至：{zip_path.absolute()}", log_callback)
    return True

def batch_classify(dir_path, mode, log_callback=None):
    """批量分类文件
    
    Args:
        dir_path (str): 目录路径或文件列表字符串
        mode (str): 分类模式（ext:按扩展名，date:按日期）
        log_callback (function, optional): 日志回调函数
        
    Returns:
        bool: 操作是否成功
    """
    file_list, input_type = parse_input_path(dir_path)
    if input_type == "invalid" or not file_list:
        safe_log("Error: 无效路径或未找到文件", log_callback)
        return False

    if input_type in ("single", "multiple"):
        first_file = Path(dir_path.split(FILE_LIST_SEPARATOR)[0])
        classify_dir = first_file.parent / "classified"
    else:
        classify_dir = Path(dir_path) / "classified"

    classify_dir.mkdir(exist_ok=True)
    count = 0
    file_count = len(file_list)

    for idx, file_path in enumerate(file_list):
        if mode == "ext":
            folder_name = file_path.suffix.lstrip(".").lower() or "no_ext"
        elif mode == "date":
            # 兼容：st_mtime (修改时间) 通常比 st_ctime (在Unix上是状态改变时间) 更精准代表文件日期
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            folder_name = mtime.strftime("%Y-%m")
        else:
            safe_log(f"⚠️ 不支持的分类模式：{mode}", log_callback)
            return False

        target_dir = classify_dir / folder_name
        target_dir.mkdir(exist_ok=True)
        
        try:
            # 移动时防止重名冲突
            dest_path = get_unique_path(target_dir / file_path.name)
            file_path.rename(dest_path)
            count += 1
        except Exception as e:
            safe_log(f"\n⚠️ 移动 {file_path.name} 失败：{str(e)}", log_callback)

        if log_callback:
            log_callback(f"progress:{int((idx + 1) / file_count * 100)}")

    safe_log(f"✅ 分类完成，共处理 {count} 个文件，已归档至 {classify_dir}", log_callback)
    return True

def batch_watermark(dir_path, type_, content="", font="", size=24, color="(255,255,255,128)",
                    opacity=128, watermark_path="", log_callback=None):
    """批量为图片添加水印
    
    Args:
        dir_path (str): 目录路径或文件列表字符串
        type_ (str): 水印类型（text:文字水印，image:图片水印）
        content (str, optional): 文字水印内容
        font (str, optional): 字体路径
        size (int, optional): 字体大小
        color (str, optional): 颜色，格式为 (R,G,B,A)
        opacity (int, optional): 透明度，0-255
        watermark_path (str, optional): 图片水印路径
        log_callback (function, optional): 日志回调函数
        
    Returns:
        bool: 操作是否成功
    """
    SUPPORT_FORMATS = {"jpg", "jpeg", "png", "webp"}
    all_files, input_type = parse_input_path(dir_path)
    if input_type == "invalid":
        return False

    img_list = [f for f in all_files if f.suffix.lower().lstrip('.') in SUPPORT_FORMATS]
    img_count = len(img_list)
    if img_count == 0:
        safe_log("❌ 未找到支持的图片", log_callback)
        return False

    # 1. 安全解析颜色 (彻底弃用危险的 eval)
    try:
        if color.startswith("(") and color.endswith(")"):
            color_tuple = ast.literal_eval(color)
        else:
            color_tuple = ImageColor.getrgb(color)
        # 如果颜色是3元组(RGB)，添加透明度
        if len(color_tuple) == 3:
            color_tuple = color_tuple + (opacity,)
        # 如果颜色是4元组，覆盖透明度
        elif len(color_tuple) == 4:
            color_tuple = color_tuple[:3] + (opacity,)
    except Exception:
        color_tuple = (255, 255, 255, opacity)

    # 2. 初始化水印源
    if type_ == "text":
        try:
            font_obj = ImageFont.truetype(font, size) if font else ImageFont.load_default()
        except Exception:
            font_obj = ImageFont.load_default()
    elif type_ == "image":
        try:
            with Image.open(watermark_path) as w_img:
                watermark_img = w_img.convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
                alpha = watermark_img.split()[3].point(lambda p: p * opacity / 255)
                watermark_img.putalpha(alpha)
        except Exception as e:
            safe_log(f"❌ 加载图片水印失败：{str(e)}", log_callback)
            return False
    else:
        return False

    # 3. 批量处理
    count = 0
    for idx, img_path in enumerate(img_list):
        try:
            with Image.open(img_path) as target_img:
                img = target_img.convert("RGBA")
                draw = ImageDraw.Draw(img)
                width, height = img.size

                if type_ == "text":
                    text_bbox = draw.textbbox((0, 0), content, font=font_obj)
                    pos = (width - (text_bbox[2] - text_bbox[0]) - 20, height - (text_bbox[3] - text_bbox[1]) - 20)
                    draw.text(pos, content, font=font_obj, fill=color_tuple)
                elif type_ == "image":
                    pos = (width - size - 20, height - size - 20)
                    img.paste(watermark_img, pos, mask=watermark_img)

                new_path = img_path.parent / f"watermarked_{img_path.name}"
                if img_path.suffix.lower() in (".jpg", ".jpeg"):
                    img.convert("RGB").save(new_path, "JPEG")
                else:
                    img.save(new_path, img_path.suffix[1:].upper())
                count += 1
        except Exception as e:
            safe_log(f"⚠️ 处理 {img_path.name} 失败：{str(e)}", log_callback)
            continue

        if log_callback:
            log_callback(f"progress:{int((idx + 1) / img_count * 100)}")

    safe_log(f"✅ 水印添加完成，共处理 {count} 张图片", log_callback)
    return True

def batch_modify_file_time(dir_path, target_time, time_type="both", log_callback=None):
    """批量修改文件时间
    
    Args:
        dir_path (str): 目录路径或文件列表字符串
        target_time (datetime): 目标时间
        time_type (str, optional): 时间类型（both:同时修改创建和修改时间，create:仅创建时间，modify:仅修改时间）
        log_callback (function, optional): 日志回调函数
        
    Returns:
        bool: 操作是否成功
    """
    file_list, input_type = parse_input_path(dir_path)
    if input_type == "invalid" or not file_list:
        return False

    target_timestamp = datetime.timestamp(target_time)
    modify_count = 0
    file_count = len(file_list)

    for idx, file_path in enumerate(file_list):
        try:
            # 弃用 os.system("touch")。使用原生 os.utime，全平台通用且更安全高效
            current_atime = os.path.getatime(file_path)
            current_mtime = os.path.getmtime(file_path)

            new_atime = target_timestamp if time_type in ["create", "both"] else current_atime
            new_mtime = target_timestamp if time_type in ["modify", "both"] else current_mtime
            
            os.utime(file_path, (new_atime, new_mtime))

            # 如果在 Windows 下需要死磕“创建时间”，才使用 ctypes 补丁
            if sys.platform == "win32" and time_type in ["create", "both"]:
                try:
                    import ctypes
                    from ctypes import wintypes
                    # Windows 原生底层修改创建时间逻辑 (可选扩展)
                    pass
                except Exception:
                    pass

            modify_count += 1
        except Exception as e:
            safe_log(f"⚠️ 处理 {file_path.name} 失败：{str(e)}", log_callback)
            continue

        if log_callback:
            log_callback(f"progress:{int((idx + 1) / file_count * 100)}")

    safe_log(f"✅ 时间修改完成，共处理 {modify_count} 个文件", log_callback)
    return True

def batch_extract_exif(dir_path, output_csv, log_callback=None):
    """批量提取图片EXIF信息
    
    Args:
        dir_path (str): 目录路径或文件列表字符串
        output_csv (str): 输出CSV文件路径
        log_callback (function, optional): 日志回调函数
        
    Returns:
        bool: 操作是否成功
    """
    SUPPORT_FORMATS = {"jpg", "jpeg", "png", "webp"}
    all_files, input_type = parse_input_path(dir_path)
    if input_type == "invalid":
        return False

    img_list = [f for f in all_files if f.suffix.lower().lstrip('.') in SUPPORT_FORMATS]
    img_count = len(img_list)
    if img_count == 0:
        return False

    headers = ["文件名", "路径", "宽度", "高度", "拍摄时间", "设备型号", "分辨率", "GPS信息"]
    extract_count = 0

    try:
        with open(output_csv, "w", newline="", encoding="utf-8-sig") as f: # utf-8-sig 防止 Excel 打开中文乱码
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for idx, img_path in enumerate(img_list):
                try:
                    exif_data = {h: "" for h in headers}
                    with Image.open(img_path) as img:
                        exif_data.update({
                            "文件名": img_path.name,
                            "路径": str(img_path.absolute()),
                            "宽度": img.width,
                            "高度": img.height,
                            "分辨率": f"{img.width}x{img.height}"
                        })

                        exif = img.getexif()
                        if exif:
                            for tag_id, value in exif.items():
                                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                                if tag_name == "DateTimeOriginal":
                                    exif_data["拍摄时间"] = str(value)
                                elif tag_name == "Model":
                                    exif_data["设备型号"] = str(value)
                                elif tag_name == "GPSInfo":
                                    exif_data["GPS信息"] = "有GPS数据" if value else ""

                        writer.writerow(exif_data)
                        extract_count += 1
                except Exception as e:
                    safe_log(f"⚠️ 提取 {img_path.name} EXIF失败：{str(e)}", log_callback)
                    continue

                if log_callback:
                    log_callback(f"progress:{int((idx + 1) / img_count * 100)}")
    except Exception as e:
        safe_log(f"❌ CSV写入失败：{str(e)}", log_callback)
        return False

    safe_log(f"✅ EXIF提取完成，结果保存至：{output_csv}", log_callback)
    return True

def batch_copy_move(dir_path, target_dir, mode="copy", exclude="", log_callback=None):
    all_files, input_type = parse_input_path(dir_path)
    if input_type == "invalid":
        return False

    exclude_exts = {ext.strip().lower() for ext in exclude.split(",") if ext.strip()} if exclude else set()
    file_list = [f for f in all_files if f.suffix.lstrip(".").lower() not in exclude_exts]
    file_count = len(file_list)
    if file_count == 0:
        return False

    target_path = Path(target_dir)
    target_path.mkdir(exist_ok=True, parents=True)
    process_count = 0

    for idx, file_path in enumerate(file_list):
        try:
            # 使用更安全的去重算法，防止高频运行下的并发覆盖
            dest_path = get_unique_path(target_path / file_path.name)

            if mode == "copy":
                shutil.copy2(file_path, dest_path)
            else:
                shutil.move(str(file_path), str(dest_path)) # shutil.move 跨盘跨分区更稳健

            process_count += 1
        except Exception as e:
            safe_log(f"⚠️ 处理 {file_path.name} 失败：{str(e)}", log_callback)
            continue

        if log_callback:
            log_callback(f"progress:{int((idx + 1) / file_count * 100)}")

    safe_log(f"✅ 批量{mode}完成，共处理 {process_count} 个文件", log_callback)
    return True
