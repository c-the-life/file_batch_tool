# 依赖管理指南

## 一、依赖说明

### 核心依赖

| 依赖包 | 版本要求 | 用途 | 安装命令 |
|--------|----------|------|----------|
| **Pillow** | >= 10.0.0 | 图片处理（格式转换、水印、EXIF提取） | `pip install Pillow>=10.0.0` |
| **PyQt5** | >= 5.15.0 | GUI图形界面 | `pip install PyQt5>=5.15.0` |

### 为什么选择这些依赖？

#### Pillow
- **用途**：图片格式转换、添加水印、提取EXIF信息
- **优势**：Python 最流行的图片处理库，支持 100+ 种图片格式
- **文档**：https://pillow.readthedocs.io/

#### PyQt5
- **用途**：图形用户界面（GUI）
- **优势**：跨平台、功能强大、界面美观
- **文档**：https://www.riverbankcomputing.com/static/Docs/PyQt5/

---

## 二、安装方法

### 方法 1：使用 requirements.txt（推荐）

```bash
# 安装所有依赖
pip install -r requirements.txt
```

### 方法 2：手动安装

```bash
# 安装 Pillow
pip install Pillow>=10.0.0

# 安装 PyQt5
pip install PyQt5>=5.15.0
```

### 方法 3：使用国内镜像加速

```bash
# 使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 使用阿里云镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
```

---

## 三、常见安装问题

### 问题 1：PyQt5 安装失败

**Windows 解决方案：**
```bash
# 方案1：指定版本
pip install PyQt5==5.15.9

# 方案2：使用 conda
conda install pyqt

# 方案3：安装 PyQt5-Qt5 和 PyQt5-sip
pip install PyQt5-Qt5 PyQt5-sip PyQt5
```

**Linux 解决方案：**
```bash
# Ubuntu/Debian
sudo apt install libgl1-mesa-glx libegl1 libxkbcommon-x11-0
pip install PyQt5

# Fedora/CentOS
sudo dnf install mesa-libGL mesa-libEGL libxkbcommon-x11
pip install PyQt5
```

### 问题 2：Pillow 安装失败

**Linux 解决方案：**
```bash
# Ubuntu/Debian
sudo apt install libjpeg-dev zlib1g-dev libpng-dev
pip install Pillow

# Fedora/CentOS
sudo dnf install libjpeg-devel zlib-devel libpng-devel
pip install Pillow
```

### 问题 3：权限不足

```bash
# 使用 --user 参数
pip install -r requirements.txt --user

# 或使用 sudo（Linux/macOS）
sudo pip install -r requirements.txt
```

### 问题 4：网络超时

```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或设置超时时间
pip install -r requirements.txt --timeout 100
```

---

## 四、虚拟环境使用

### 为什么使用虚拟环境？

- 隔离项目依赖，避免版本冲突
- 方便项目迁移和部署
- 保持系统 Python 环境干净

### 创建虚拟环境

**Windows:**
```bash
# 创建
python -m venv venv

# 激活
venv\Scripts\activate

# 退出
deactivate
```

**Linux / macOS:**
```bash
# 创建
python3 -m venv venv

# 激活
source venv/bin/activate

# 退出
deactivate
```

---

## 五、作为库被其他项目依赖

### 方式 1：从 PyPI 安装

```bash
pip install file-batch-tool
```

### 方式 2：从 Git 仓库安装

```txt
# 在 requirements.txt 中
git+https://github.com/c-the-life/file_batch_tool.git@v1.1.0#egg=file-batch-tool
```

### 方式 3：从本地安装

```bash
pip install -e /path/to/file_batch_tool
```

---

## 六、版本管理

### 语义化版本

格式：`MAJOR.MINOR.PATCH`

- **MAJOR**：不兼容的 API 变更
- **MINOR**：向下兼容的功能新增
- **PATCH**：向下兼容的问题修正

### 依赖版本指定方式

```txt
# 精确版本
Pillow==10.0.0

# 最小版本
Pillow>=10.0.0

# 版本范围
Pillow>=10.0.0,<11.0.0

# 兼容版本
Pillow~=10.0.0  # 等同于 >=10.0.0,<11.0.0
```

---

## 七、依赖更新

### 检查可更新的依赖

```bash
pip list --outdated
```

### 更新依赖

```bash
# 更新单个包
pip install --upgrade Pillow

# 更新所有依赖
pip install --upgrade -r requirements.txt
```

### 冻结当前依赖版本

```bash
pip freeze > requirements.txt
```

---

## 八、最佳实践

1. **使用虚拟环境** - 隔离项目依赖
2. **固定版本范围** - 使用 `>=x.x.x,<y.y.y` 格式
3. **定期更新依赖** - 获取安全补丁和新功能
4. **使用国内镜像** - 加速下载
5. **记录依赖变更** - 使用 `pip freeze` 保存当前环境
