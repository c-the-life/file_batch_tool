# -*- coding: utf-8 -*-
"""批量操作编排器模块"""

from typing import List, Callable, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class OperationStatus(Enum):
    """操作状态"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Operation:
    """操作定义"""
    name: str
    func: Callable
    args: tuple = ()
    kwargs: Dict[str, Any] = None
    status: OperationStatus = OperationStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}


class BatchOrchestrator:
    """批量操作编排器"""

    def __init__(self):
        """初始化编排器"""
        self.operations: List[Operation] = []
        self.current_index = 0
        self.on_progress: Optional[Callable] = None
        self.on_operation_complete: Optional[Callable] = None

    def add_operation(self, name: str, func: Callable, *args, **kwargs) -> 'BatchOrchestrator':
        """添加操作

        Args:
            name: 操作名称
            func: 操作函数
            *args: 函数位置参数
            **kwargs: 函数关键字参数

        Returns:
            self，方便链式调用
        """
        operation = Operation(name=name, func=func, args=args, kwargs=kwargs)
        self.operations.append(operation)
        return self

    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """设置进度回调

        Args:
            callback: 回调函数 (current, total, operation_name)
        """
        self.on_progress = callback

    def set_complete_callback(self, callback: Callable[[Operation], None]):
        """设置操作完成回调

        Args:
            callback: 回调函数 (operation)
        """
        self.on_operation_complete = callback

    def execute(self, stop_on_error: bool = True) -> List[Operation]:
        """执行所有操作

        Args:
            stop_on_error: 遇到错误是否停止

        Returns:
            操作结果列表
        """
        results = []
        total = len(self.operations)

        for i, operation in enumerate(self.operations):
            self.current_index = i

            if self.on_progress:
                self.on_progress(i + 1, total, operation.name)

            try:
                operation.status = OperationStatus.RUNNING
                operation.result = operation.func(*operation.args, **operation.kwargs)
                operation.status = OperationStatus.SUCCESS

            except Exception as e:
                operation.status = OperationStatus.FAILED
                operation.error = e

                if stop_on_error:
                    for remaining in self.operations[i + 1:]:
                        remaining.status = OperationStatus.SKIPPED
                    break

            if self.on_operation_complete:
                self.on_operation_complete(operation)

            results.append(operation)

        return results

    def get_summary(self) -> Dict[str, Any]:
        """获取执行摘要

        Returns:
            摘要信息字典
        """
        total = len(self.operations)
        success = sum(1 for op in self.operations if op.status == OperationStatus.SUCCESS)
        failed = sum(1 for op in self.operations if op.status == OperationStatus.FAILED)
        skipped = sum(1 for op in self.operations if op.status == OperationStatus.SKIPPED)

        return {
            "total": total,
            "success": success,
            "failed": failed,
            "skipped": skipped,
            "success_rate": (success / total * 100) if total > 0 else 0
        }

    def clear(self):
        """清空所有操作"""
        self.operations.clear()
        self.current_index = 0
