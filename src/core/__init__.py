"""文件批量处理工具 - 核心模块
包含工作线程功能

这个模块提供了项目的核心线程处理类，用于在后台执行
耗时的文件操作任务，避免阻塞GUI界面。

主要功能：
- 异步任务执行
- 实时进度更新
- 日志信息传递
- 错误处理
"""

from .worker import WorkerThread

__all__ = [
    "WorkerThread",
]

# 模块元数据
__module_version__ = "1.0.0"
__module_author__ = "File Batch Tool Team"

