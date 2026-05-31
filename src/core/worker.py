"""工作线程模块
提供异步文件处理任务执行功能
"""
import traceback

# PyQt5 相关导入
from PyQt5.QtCore import QThread, pyqtSignal

# 项目内部模块导入
from src.utils import file_operations

class WorkerThread(QThread):
    """工作线程类
    
    提供异步文件处理任务执行功能，支持进度和日志回调
    """
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finish_signal = pyqtSignal(bool)

    # 1. 建立任务类型与底层函数的自动映射关系
    # 键名为 task_type，键值为 file_operations 里的对应函数名
    TASK_MAPPING = {
        "rename": "batch_rename",
        "convert_img": "batch_convert_image",
        "compress": "batch_compress",
        "classify": "batch_classify",
        "watermark": "batch_watermark",
        "modify_time": "batch_modify_file_time",
        "extract_exif": "batch_extract_exif",
        "copy_move": "batch_copy_move"
    }

    def __init__(self, task_type, params):
        super().__init__()
        self.task_type = task_type
        self.params = params

    def run(self):
        # 2. 统一的进度和日志回调接口
        def log_callback(msg):
            if msg.startswith("progress:"):
                try:
                    progress = int(msg.split(":")[1])
                    self.progress_signal.emit(progress)
                except (ValueError, IndexError):
                    pass
            else:
                self.log_signal.emit(msg)

        try:
            # 3. 动态获取目标函数
            func_name = self.TASK_MAPPING.get(self.task_type)
            if not func_name or not hasattr(file_operations, func_name):
                self.log_signal.emit(f"❌ 不支持的任务类型: {self.task_type}")
                self.finish_signal.emit(False)
                return

            target_function = getattr(file_operations, func_name)

            # 4. 自动匹配参数
            # 我们将具体的参数名称与底层的形参做下映射（处理个别参数名不一致的情况）
            kwargs = self.params.copy()
            dir_path = kwargs.pop("dir", None)
            if dir_path is not None:
                kwargs["dir_path"] = dir_path
            
            # 因为 watermark 接收的是 type_，而 params 里是 type
            if "type" in kwargs:
                kwargs["type_"] = kwargs.pop("type")

            # 注入统一的回调函数
            kwargs["log_callback"] = log_callback

            # 5. 一行代码动态调用，优雅且拓展性极强
            result = target_function(**kwargs)
            self.finish_signal.emit(bool(result))

        except Exception as e:
            # 6. 安全捕获异常，打印完整堆栈，防止线程闪退
            error_msg = f"❌ 任务执行异常: {str(e)}\n{traceback.format_exc()}"
            self.log_signal.emit(error_msg)
            self.finish_signal.emit(False)
