# 🤝 贡献指南

欢迎加入我们的开源项目！无论是代码贡献、文档改进、Bug报告还是功能建议，我们都非常欢迎！

> **项目简介**：这是一个功能强大的文件批量处理工具，支持批量重命名、图片格式转换、文件压缩、分类整理、水印添加等功能，还提供AI智能助手支持自然语言操作。

---

## 📖 目录

1. [如何贡献](#1-如何贡献)
2. [开发流程](#2-开发流程)
3. [代码规范](#3-代码规范)
4. [提交指南](#4-提交指南)
5. [贡献者列表](#5-贡献者列表)

---

## 💡 快速开始

如果您是第一次贡献，可以从以下简单的任务开始：

- 📝 改进文档或示例代码
- 🐛 报告并修复简单的 Bug
- ✨ 添加小的功能改进
- 📚 补充注释和文档字符串

---

## 1. 如何贡献

### 1.1 报告问题

如果您发现了 Bug 或者有功能建议，请按照以下步骤：

1. 查看 [Issues](https://github.com/c-the-life/file_batch_tool/issues) 是否已有相关讨论
2. 如果没有，请新建一个 Issue
3. 描述清楚问题或建议：
   - 🐛 **Bug报告**：提供复现步骤、错误信息、截图
   - 💡 **功能建议**：说明您想要的功能及其用途

### 1.2 提交代码

1. **Fork 仓库**：点击 GitHub 页面右上角的 "Fork" 按钮
2. **克隆您的仓库**：
   ```bash
   git clone https://github.com/your-username/file_batch_tool.git
   cd file_batch_tool
   ```
3. **创建分支**：
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **提交更改**：按照 [提交指南](#4-提交指南) 提交
5. **推送分支**：
   ```bash
   git push origin feature/your-feature-name
   ```
6. **创建 Pull Request**：在 GitHub 上创建 PR

---

## 2. 开发流程

### 2.1 环境设置

```bash
# 克隆项目
git clone https://github.com/c-the-life/file_batch_tool.git
cd file_batch_tool

# 创建虚拟环境（推荐）
python -m venv venv
# 激活虚拟环境
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install pytest black
```

### 2.2 运行测试

```bash
# 运行测试（如果有测试文件）
pytest tests/

# 代码格式化
black src/
```

### 2.3 目录结构

```
file_batch_tool/
├── src/                    # 源代码
│   ├── core/               # 核心模块（WorkerThread）
│   ├── ui/                 # 界面模块（主窗口）
│   ├── utils/              # 工具函数（文件操作）
│   └── __init__.py         # 包导出
├── examples/               # 示例代码
├── tests/                  # 测试文件
├── screenshots/            # 截图
├── README.md               # 项目说明
├── requirements.txt         # 依赖列表
└── setup.py                # 打包配置
```

---

## 3. 代码规范

### 3.1 Python 代码规范

- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 规范
- 使用 4 个空格缩进
- 行宽不超过 120 字符
- 使用类型注解
- 函数和类要有文档字符串

### 3.2 提交消息规范

```
<类型>: <简短描述>

<详细描述（可选）>
```

**类型**：
- `feat`：新功能
- `fix`：修复 Bug
- `docs`：文档更新
- `style`：代码格式（不影响功能）
- `refactor`：重构（既不新增功能也不修复 Bug）
- `test`：测试相关
- `chore`：构建/工具相关

**示例**：
```
feat: 添加图片格式转换功能

- 支持 JPG/PNG/WebP 互转
- 自动处理透明通道
```

---

## 4. 提交指南

### 4.1 基本流程

```bash
# 查看状态
git status

# 添加文件
git add .

# 提交（使用规范的提交消息）
git commit -m "feat: 添加拖拽支持"

# 拉取最新代码（避免冲突）
git pull origin master

# 推送到您的仓库
git push origin your-branch
```

### 4.2 Pull Request 规范

1. **标题**：清晰描述您的更改
2. **描述**：
   - 做了什么更改
   - 为什么做这些更改
   - 如何测试
3. **相关 Issue**：如果有相关 Issue，请引用

---

## 5. 贡献者列表

### ✨ 贡献者

感谢所有为这个项目做出贡献的人！

| 贡献者 | 贡献内容 |
|--------|----------|
| [the-life](https://github.com/c-the-life) | 项目创始人，核心功能开发 |

### 📊 贡献统计

您可以在以下页面查看详细的贡献统计：

- **GitHub**：[Contributors](https://github.com/c-the-life/file_batch_tool/graphs/contributors)
- **Gitee**：[贡献者](https://gitee.com/the-life/file_batch_tool/contributors)

### 🎖️ 贡献徽章

如果您贡献了代码，可以在您的个人资料中添加这个徽章：

```markdown
[![Contributor](https://img.shields.io/badge/Contributor-file--batch--tool-blue.svg)](https://github.com/c-the-life/file_batch_tool)
```

---

## 6. 代码审查指南

### 6.1 Pull Request 检查清单

在提交 PR 之前，请确保：

- [ ] 代码已通过所有测试
- [ ] 代码符合项目的编码规范
- [ ] 已添加必要的文档和注释
- [ ] 已更新相关的 README 或文档
- [ ] 提交消息遵循规范
- [ ] 没有引入不必要的依赖
- [ ] 没有包含调试代码（如 print 语句）

### 6.2 代码审查要点

#### 功能性检查
- ✅ 代码是否实现了预期功能？
- ✅ 是否处理了边界情况？
- ✅ 是否有适当的错误处理？
- ✅ 是否会影响现有功能？

#### 代码质量检查
- ✅ 代码是否清晰易懂？
- ✅ 变量和函数命名是否合适？
- ✅ 是否有重复代码可以提取？
- ✅ 是否有更好的实现方式？

#### 性能检查
- ✅ 是否有性能问题？
- ✅ 循环或递归是否会导致问题？
- ✅ 内存使用是否合理？

#### 安全检查
- ✅ 是否有安全隐患？
- ✅ 是否正确处理用户输入？
- ✅ 是否有文件操作风险？

### 6.3 审查建议

**作为审查者：**
1. 保持尊重和建设性的态度
2. 提供具体的建议，而不是模糊的批评
3. 解释为什么需要更改
4. 认可好的代码实践

**作为被审查者：**
1. 认真对待每个反馈
2. 询问不清楚的地方
3. 解释你的设计决策
4. 感谢审查者的时间

---

## 7. 文档贡献

### 7.1 文档类型

我们欢迎以下文档贡献：

- 📖 教程和使用指南
- 📚 API 文档和注释
- 🎯 示例代码和用例
- 🐛 故障排除指南
- 📝 常见问题解答

### 7.2 文档规范

1. **清晰易懂**：使用简洁的语言
2. **结构合理**：使用标题、列表、代码块
3. **示例完整**：提供可运行的代码示例
4. **保持更新**：确保文档与代码一致

### 7.3 文档工具

我们使用以下格式：
- **Markdown**：所有文档使用 Markdown 格式
- **代码块**：使用 ```python 或 ```bash 标记

---

## 8. 获取帮助

如果您在贡献过程中遇到问题：

1. **查看文档**：先阅读 README 和教程
2. **搜索 Issues**：看看是否有类似问题
3. **提问**：在 Discussions 中提问
4. **联系维护者**：通过 GitHub 联系

### 8.1 沟通渠道

- **Issues**：报告 Bug 和功能建议
- **Discussions**：讨论项目相关话题
- **Pull Requests**：代码审查和讨论

---

## 9. 社区准则

### 9.1 我们重视

- 🏆 尊重和友善
- 🤝 协作和互助
- 💡 开放和包容
- 🔍 专业和负责

### 9.2 避免

- ❌ 攻击性或贬低性评论
- ❌ 人身攻击
- ❌ 泄露隐私
- ❌ 垃圾信息或广告

---

## 📝 许可证

所有贡献的代码都将遵循项目的 [MIT License](LICENSE)。

---

## 🎉 总结

感谢您考虑为 file_batch_tool 做出贡献！

无论贡献大小，每一份努力都让这个项目变得更好：
- 🐛 报告 Bug
- 💡 提出想法
- 📝 改进文档
- 💻 编写代码

**再次感谢您的贡献！** 🎉

