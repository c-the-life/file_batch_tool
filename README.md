# 📁 文件批量处理工具
轻量Python命令行工具，支持5大核心功能：重命名、图片转换、压缩、分类、加水印。

## ✨ 功能列表
1. 📝 批量重命名：正则替换、前缀/后缀
2. 🖼️ 图片转换：jpg/png/webp互转
3. 📦 文件压缩：ZIP打包，支持排除文件
4. 📂 文件分类：按扩展名/日期自动归档
5. 🔖 图片水印：文字/图片水印，支持透明度调整

## 🚀 安装方式
```bash
# 方式1：通过pip安装
python -m pip install file-batch-tool

# 方式2：从源码安装
git clone https://gitee.com/the-life/file_batch_tool.git
cd file_batch_tool
python -m pip install -r requirements.txt
```

# 📖 使用示例
##使用之前
找到 Python 的 Scripts 路径，比如：
C:\Users\LX\AppData\Local\Programs\Python\Python3x\Scripts
把这个路径添加到系统环境变量 PATH 里。
重新打开 PowerShell，执行：
pip install -e .
之后就可以直接运行以下命令
### 批量重命名
```bash
# 给所有文件添加前缀 "2024_"
file-batch-tool rename --dir ./test --prefix 2024_

# 正则替换：将 "img_001.jpg" 改为 "photo_001.jpg"
file-batch-tool rename --dir ./test --pattern "img_" --replace "photo_"
```

### 批量转换图片格式
```bash
# 将目录下所有图片转为jpg格式
file-batch-tool convert-img --dir ./images --to-format jpg
```

### 批量压缩文件
```bash
# 压缩 ./files 目录下所有文件（排除zip和log）
file-batch-tool compress --dir ./files --output my_files.zip --exclude zip,log
```

### 批量分类文件
```bash
# 按扩展名分类
file-batch-tool classify --dir ./files --mode ext

# 按创建日期分类（按月归档）
file-batch-tool classify --dir ./files --mode date
```

### 批量添加水印
```bash
# 添加文字水印
file-batch-tool watermark --dir ./images --type text --content "我的水印" --size 32

# 添加图片水印
file-batch-tool watermark --dir ./images --type image --watermark-path ./logo.png --size 64
```

## 🤝 贡献指南
欢迎提交Issue和PR！贡献步骤：
1. Fork本仓库
2. 创建功能分支：`git checkout -b feature/xxx`
3. 提交变更：`git commit -m "新增xxx功能"`
4. 推送分支：`git push origin feature/xxx`
5. 提交PR

## 📄 许可证
MIT License
