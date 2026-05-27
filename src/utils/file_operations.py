import os
import re
import sys
import csv
import time
import zipfile
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ExifTags

Image.MAX_IMAGE_PIXELS = None

FILE_LIST_SEPARATOR = "|||"


def parse_input_path(input_path):
    """解析输入路径，支持单个文件、目录、多个文件"""
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
                    file_list.extend([f for f in p.glob("*") if f.is_file()])
        return file_list, "multiple"
    else:
        path_obj = Path(input_path)
        if path_obj.is_file():
            return [path_obj], "single"
        elif path_obj.is_dir():
            return [f for f in path_obj.glob("*") if f.is_file()], "dir"
        else:
            return [], "invalid"


def batch_rename(dir_path, prefix="", suffix="", find_str="", replace_str="", log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

    file_list, input_type = parse_input_path(dir_path)
    file_count = len(file_list)

    if input_type == "invalid":
        log(f"❌ 路径 {dir_path} 不是有效文件或目录")
        return False

    if file_count == 0:
        log(f"❌ 未找到任何文件")
        return False

    if input_type == "single":
        log(f"📝 处理单个文件：{file_list[0].name}")
    elif input_type == "multiple":
        log(f"📝 开始批量重命名，共处理 {file_count} 个文件")
    else:
        log(f"📝 开始批量重命名，共扫描到 {file_count} 个有效文件")

    rename_count = 0
    skip_count = 0

    for idx, file_path in enumerate(file_list):
        old_name = file_path.name
        name, ext = os.path.splitext(old_name)
        new_main_name = name
        new_ext = ext

        if find_str.strip():
            new_main_name = new_main_name.replace(find_str, replace_str)

        if prefix:
            new_main_name = prefix + new_main_name
        if suffix:
            new_main_name = new_main_name + suffix

        new_name = new_main_name + new_ext
        if new_name == old_name:
            skip_count += 1
            continue

        new_path = file_path.parent / new_name
        if new_path.exists():
            log(f"⚠️ 跳过 {old_name}：新文件名 {new_name} 已存在")
            skip_count += 1
            continue

        try:
            file_path.rename(new_path)
            rename_count += 1
            log(f"✅ 重命名：{old_name} → {new_name}")
        except PermissionError:
            log(f"⚠️ 跳过 {old_name}：无操作权限/文件被占用")
            skip_count += 1
        except Exception as e:
            log(f"⚠️ 跳过 {old_name}：重命名失败 - {str(e)}")
            skip_count += 1

        if log_callback:
            progress = int((idx + 1) / file_count * 100)
            log(f"progress:{progress}")

    log(f"\n✅ 重命名任务结束 | 总文件：{file_count} | 成功重命名：{rename_count} | 跳过：{skip_count}")
    return rename_count > 0


def batch_convert_image(dir_path, to_format, log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

    SUPPORT_FORMATS = ["jpg", "jpeg", "png", "webp"]
    target_format = to_format.lower()

    all_files, input_type = parse_input_path(dir_path)
    
    if input_type == "invalid":
        log(f"❌ 路径 {dir_path} 不是有效文件或目录")
        return False

    img_list = []
    for f in all_files:
        ext = f.suffix.lower().lstrip('.')
        if ext in SUPPORT_FORMATS:
            img_list.append(f)

    img_count = len(img_list)

    if img_count == 0:
        log(f"❌ 未找到支持的图片文件（{SUPPORT_FORMATS}）")
        return False

    if input_type == "single":
        log(f"🖼️ 处理单个文件：{img_list[0].name}")
    elif input_type == "multiple":
        log(f"🖼️ 开始批量转换图片格式，共找到 {img_count} 张图片")
    else:
        log(f"🖼️ 开始批量转换图片格式，共找到 {img_count} 张图片")

    convert_count = 0

    for idx, img_path in enumerate(img_list):
        try:
            with Image.open(img_path) as img:
                if target_format in ["jpg", "jpeg"]:
                    if img.mode in ("RGBA", "P"):
                        bg = Image.new("RGB", img.size, (255, 255, 255))
                        mask = img.split()[-1] if img.mode == "RGBA" else None
                        bg.paste(img, (0, 0), mask)
                        img = bg
                    else:
                        img = img.convert("RGB")
                else:
                    img = img.convert("RGBA") if img.mode != "RGBA" else img

                new_name = f"{img_path.stem}_converted.{target_format}"
                new_path = img_path.parent / new_name

                format_map = {
                    "jpg": "JPEG",
                    "jpeg": "JPEG",
                    "png": "PNG",
                    "webp": "WEBP"
                }
                save_format = format_map.get(target_format, target_format.upper())
                img.save(new_path, save_format, quality=95)
                convert_count += 1

        except PermissionError:
            log(f"\n⚠️ 无权限写入 {new_path}，请关闭该文件后重试")
        except Exception as e:
            log(f"\n⚠️ 处理 {img_path.name} 失败：{str(e)}")
            continue

        if log_callback:
            progress = int((idx + 1) / img_count * 100)
            log(f"progress:{progress}")

    log(f"✅ 图片转换完成，共成功处理 {convert_count} 张图片")
    return True


def batch_compress(dir_path, output="", exclude="", log_callback=None):
    def log(msg):
        try:
            if log_callback:
                log_callback(msg)
            else:
                print(msg)
        except UnicodeEncodeError:
            if log_callback:
                log_callback(msg.encode('ascii', 'replace').decode('ascii'))
            else:
                print(msg.encode('ascii', 'replace').decode('ascii'))

    all_files, input_type = parse_input_path(dir_path)
    
    if input_type == "invalid":
        log(f"Error: 路径 {dir_path} 不是有效文件或目录")
        return False

    if exclude:
        exclude_exts = [ext.strip().lower() for ext in exclude.split(",") if ext.strip()]
        file_list = [f for f in all_files if f.suffix.lstrip(".").lower() not in exclude_exts]
    else:
        file_list = all_files

    file_count = len(file_list)
    if file_count == 0:
        log(f"Error: 未找到可压缩的文件")
        return False

    if input_type == "single":
        log(f"Info: 处理单个文件：{file_list[0].name}")
        default_name = f"{file_list[0].parent / file_list[0].stem}_compressed.zip"
    elif input_type == "multiple":
        log(f"Info: 开始批量压缩文件，共找到 {file_count} 个文件")
        first_file = Path(dir_path.split(FILE_LIST_SEPARATOR)[0])
        default_name = f"{first_file.parent / 'files_compressed'}.zip"
    else:
        log(f"Info: 开始批量压缩文件，共找到 {file_count} 个文件")
        default_name = f"{dir_path}_compressed.zip"
    
    zip_name = output if output else default_name
    zip_path = Path(zip_name)
    if zip_path.exists():
        log(f"❌ ZIP包 {zip_path} 已存在，请更换输出文件名")
        return False
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for idx, file_path in enumerate(file_list):
            zipf.write(file_path, arcname=file_path.name)
            if log_callback:
                progress = int((idx + 1) / file_count * 100)
                log(f"progress:{progress}")

    log(f"✅ 压缩完成！ZIP包已保存至：{zip_path.absolute()}")
    return True


def batch_classify(dir_path, mode, log_callback=None):
    def log(msg):
        try:
            if log_callback:
                log_callback(msg)
            else:
                print(msg)
        except UnicodeEncodeError:
            if log_callback:
                log_callback(msg.encode('ascii', 'replace').decode('ascii'))
            else:
                print(msg.encode('ascii', 'replace').decode('ascii'))

    file_list, input_type = parse_input_path(dir_path)
    
    if input_type == "invalid":
        log(f"Error: 路径 {dir_path} 不是有效文件或目录")
        return False

    file_count = len(file_list)
    if file_count == 0:
        log(f"Error: 未找到文件")
        return False

    if input_type == "single":
        log(f"Info: 处理单个文件：{file_list[0].name}")
        classify_dir = file_list[0].parent / "classified"
    elif input_type == "multiple":
        log(f"Info: 开始批量分类，共 {file_count} 个文件")
        first_file = Path(dir_path.split(FILE_LIST_SEPARATOR)[0])
        classify_dir = first_file.parent / "classified"
    else:
        log(f"Info: 开始批量分类，共 {file_count} 个文件")
        classify_dir = Path(dir_path) / "classified"

    classify_dir.mkdir(exist_ok=True)
    count = 0
    for idx, file_path in enumerate(file_list):
        if mode == "ext":
            ext = file_path.suffix.lstrip(".").lower() or "no_ext"
            target_dir = classify_dir / ext
        elif mode == "date":
            ctime = datetime.fromtimestamp(file_path.stat().st_ctime)
            date_str = ctime.strftime("%Y-%m")
            target_dir = classify_dir / date_str
        else:
            log(f"⚠️ 不支持的分类模式：{mode}")
            return False

        target_dir.mkdir(exist_ok=True)
        try:
            file_path.rename(target_dir / file_path.name)
            count += 1
        except Exception as e:
            log(f"\n⚠️ 移动 {file_path.name} 失败：{str(e)}")
            continue

        if log_callback:
            progress = int((idx + 1) / file_count * 100)
            log(f"progress:{progress}")

    log(f"✅ 分类完成，共处理 {count} 个文件，已归档至 {classify_dir}")
    return True


def batch_watermark(dir_path, type_, content="", font="", size=24, color="(255,255,255,128)",
                    opacity=128, watermark_path="", log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

    SUPPORT_FORMATS = ["jpg", "jpeg", "png", "webp"]
    
    all_files, input_type = parse_input_path(dir_path)
    
    if input_type == "invalid":
        log(f"❌ 路径 {dir_path} 不是有效文件或目录")
        return False

    img_list = []
    for f in all_files:
        ext = f.suffix.lower().lstrip('.')
        if ext in SUPPORT_FORMATS:
            img_list.append(f)

    img_count = len(img_list)
    if img_count == 0:
        log(f"❌ 未找到支持的图片（{SUPPORT_FORMATS}）")
        return False

    if input_type == "single":
        log(f"🔖 处理单个文件：{img_list[0].name}")
    elif input_type == "multiple":
        log(f"🔖 开始批量添加水印，共 {img_count} 张图片")
    else:
        log(f"🔖 开始批量添加水印，共 {img_count} 张图片")

    count = 0

    if type_ == "text":
        color_tuple = eval(color) if color else (255, 255, 255, 128)
        try:
            font_obj = ImageFont.truetype(font, size) if font else ImageFont.load_default()
        except:
            font_obj = ImageFont.load_default()
    elif type_ == "image":
        try:
            watermark_img = Image.open(watermark_path).convert("RGBA")
            watermark_img = watermark_img.resize((size, size), Image.Resampling.LANCZOS)
            alpha = watermark_img.split()[3]
            alpha = alpha.point(lambda p: p * opacity / 255)
            watermark_img.putalpha(alpha)
        except Exception as e:
            log(f"❌ 加载图片水印失败：{str(e)}")
            return False
    else:
        log(f"⚠️ 不支持的水印类型：{type_}")
        return False

    for idx, img_path in enumerate(img_list):
        try:
            img = Image.open(img_path).convert("RGBA")
            draw = ImageDraw.Draw(img)
            width, height = img.size

            if type_ == "text":
                text_bbox = draw.textbbox((0, 0), content, font=font_obj)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                pos = (width - text_width - 20, height - text_height - 20)
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
            log(f"\n⚠️ 处理 {img_path.name} 失败：{str(e)}")
            continue

        if log_callback:
            progress = int((idx + 1) / img_count * 100)
            log(f"progress:{progress}")

    log(f"✅ 水印添加完成，共处理 {count} 张图片")
    return True


def batch_modify_file_time(dir_path, target_time, time_type="both", log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

    file_list, input_type = parse_input_path(dir_path)
    
    if input_type == "invalid":
        log(f"❌ 路径 {dir_path} 不是有效文件或目录")
        return False

    file_count = len(file_list)
    if file_count == 0:
        log(f"❌ 未找到文件")
        return False

    if input_type == "single":
        log(f"🕒 处理单个文件：{file_list[0].name}")
    elif input_type == "multiple":
        log(f"🕒 开始批量修改文件时间，共找到 {file_count} 个文件")
    else:
        log(f"🕒 开始批量修改文件时间，共找到 {file_count} 个文件")

    target_timestamp = datetime.timestamp(target_time)
    modify_count = 0

    for idx, file_path in enumerate(file_list):
        try:
            if time_type in ["create", "both"]:
                if sys.platform == "win32":
                    os.utime(file_path, (target_timestamp, target_timestamp))
                else:
                    os.system(f"touch -t {target_time.strftime('%Y%m%d%H%M.%S')} {file_path}")

            if time_type in ["modify", "both"]:
                os.utime(file_path, (os.path.getatime(file_path), target_timestamp))

            modify_count += 1
        except PermissionError:
            log(f"\n⚠️ 无权限修改 {file_path.name} 时间，请关闭该文件后重试")
        except Exception as e:
            log(f"\n⚠️ 处理 {file_path.name} 失败：{str(e)}")
            continue

        if log_callback:
            progress = int((idx + 1) / file_count * 100)
            log(f"progress:{progress}")

    log(f"✅ 时间修改完成，共处理 {modify_count} 个文件")
    return True


def batch_extract_exif(dir_path, output_csv, log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

    SUPPORT_FORMATS = ["jpg", "jpeg", "png", "webp"]
    
    all_files, input_type = parse_input_path(dir_path)
    
    if input_type == "invalid":
        log(f"❌ 路径 {dir_path} 不是有效文件或目录")
        return False

    img_list = []
    for f in all_files:
        ext = f.suffix.lower().lstrip('.')
        if ext in SUPPORT_FORMATS:
            img_list.append(f)

    img_count = len(img_list)
    if img_count == 0:
        log(f"❌ 未找到支持的图片文件（{SUPPORT_FORMATS}）")
        return False

    if input_type == "single":
        log(f"📷 处理单个文件：{img_list[0].name}")
    elif input_type == "multiple":
        log(f"📷 开始提取EXIF信息，共找到 {img_count} 张图片")
    else:
        log(f"📷 开始提取EXIF信息，共找到 {img_count} 张图片")

    headers = ["文件名", "路径", "宽度", "高度", "拍摄时间", "设备型号", "分辨率", "GPS信息"]
    extract_count = 0

    try:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for idx, img_path in enumerate(img_list):
                try:
                    exif_data = {}
                    with Image.open(img_path) as img:
                        exif_data["文件名"] = img_path.name
                        exif_data["路径"] = str(img_path.absolute())
                        exif_data["宽度"] = img.width
                        exif_data["高度"] = img.height
                        exif_data["分辨率"] = f"{img.width}x{img.height}"
                        exif_data["拍摄时间"] = ""
                        exif_data["设备型号"] = ""
                        exif_data["GPS信息"] = ""

                        exif = img.getexif()
                        if exif:
                            exif_tag_map = {v: k for k, v in ExifTags.TAGS.items()}
                            for tag_id, value in exif.items():
                                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                                if tag_name == "DateTimeOriginal":
                                    exif_data["拍摄时间"] = value
                                elif tag_name == "Model":
                                    exif_data["设备型号"] = value
                                elif tag_name == "GPSInfo":
                                    exif_data["GPS信息"] = "有GPS数据" if value else ""

                        writer.writerow(exif_data)
                        extract_count += 1
                except Exception as e:
                    log(f"\n⚠️ 提取 {img_path.name} EXIF失败：{str(e)}")
                    continue

                if log_callback:
                    progress = int((idx + 1) / img_count * 100)
                    log(f"progress:{progress}")

    except PermissionError:
        log(f"\n❌ 无权限写入CSV文件：{output_csv}")
        return False
    except Exception as e:
        log(f"\n❌ CSV写入失败：{str(e)}")
        return False

    log(f"✅ EXIF提取完成，共处理 {extract_count} 张图片，结果已保存至：{output_csv}")
    return True


def batch_copy_move(dir_path, target_dir, mode="copy", exclude="", log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

    all_files, input_type = parse_input_path(dir_path)
    
    if input_type == "invalid":
        log(f"❌ 路径 {dir_path} 不是有效文件或目录")
        return False

    if exclude:
        exclude_exts = [ext.strip().lower() for ext in exclude.split(",") if ext.strip()]
        file_list = [f for f in all_files if f.suffix.lstrip(".").lower() not in exclude_exts]
    else:
        file_list = all_files

    file_count = len(file_list)
    if file_count == 0:
        log(f"❌ 未找到可处理的文件")
        return False

    if input_type == "single":
        log(f"📤 处理单个文件：{file_list[0].name}")
    elif input_type == "multiple":
        log(f"📤 开始批量{mode}文件，共找到 {file_count} 个文件")
    else:
        log(f"📤 开始批量{mode}文件，共找到 {file_count} 个文件")

    target_path = Path(target_dir)
    target_path.mkdir(exist_ok=True, parents=True)
    process_count = 0
    for idx, file_path in enumerate(file_list):
        try:
            dest_path = target_path / file_path.name
            if dest_path.exists():
                dest_path = target_path / f"{file_path.stem}_{int(time.time())}{file_path.suffix}"

            if mode == "copy":
                import shutil
                shutil.copy2(file_path, dest_path)
            else:
                file_path.rename(dest_path)

            process_count += 1
        except PermissionError:
            log(f"\n⚠️ 无权限操作 {file_path.name}，请关闭该文件后重试")
        except Exception as e:
            log(f"\n⚠️ 处理 {file_path.name} 失败：{str(e)}")
            continue

        if log_callback:
            progress = int((idx + 1) / file_count * 100)
            log(f"progress:{progress}")

    log(f"✅ 批量{mode}完成，共处理 {process_count} 个文件，目标目录：{target_path.absolute()}")
    return True
