# -*- coding: utf-8 -*-
"""进度跟踪器模块"""

import time
from typing import Optional, Callable
from datetime import datetime


class ProgressTracker:
    """进度跟踪器"""

    def __init__(self, total: int, description: str = "处理中"):
        """初始化进度跟踪器

        Args:
            total: 总任务数
            description: 任务描述
        """
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
        self.callback = None

    def set_callback(self, callback: Callable[[int, int, float], None]):
        """设置进度回调函数

        Args:
            callback: 回调函数，参数为 (current, total, percentage)
        """
        self.callback = callback

    def update(self, increment: int = 1, info: str = ""):
        """更新进度

        Args:
            increment: 增加的数量
            info: 额外信息
        """
        self.current += increment
        if self.current > self.total:
            self.current = self.total

        percentage = (self.current / self.total * 100) if self.total > 0 else 0
        elapsed = time.time() - self.start_time

        if self.callback:
            self.callback(self.current, self.total, percentage)

        if info:
            self._log(f"{info} ({self.current}/{self.total}, {percentage:.1f}%)")
        elif self.current % max(1, self.total // 10) == 0 or self.current == self.total:
            eta = self._calculate_eta(percentage)
            self._log(f"{self.description}: {self.current}/{self.total} ({percentage:.1f}%) - 预计剩余: {eta}")

    def _calculate_eta(self, percentage: float) -> str:
        """计算预计剩余时间

        Args:
            percentage: 完成百分比

        Returns:
            剩余时间字符串
        """
        if percentage == 0:
            return "计算中..."

        elapsed = time.time() - self.start_time
        if percentage >= 100:
            return "已完成"

        estimated_total = elapsed / (percentage / 100)
        remaining = estimated_total - elapsed

        if remaining < 60:
            return f"{remaining:.0f}秒"
        elif remaining < 3600:
            return f"{remaining/60:.1f}分钟"
        else:
            return f"{remaining/3600:.1f}小时"

    def _log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def finish(self):
        """完成任务"""
        self.current = self.total
        elapsed = time.time() - self.start_time
        self._log(f"✅ {self.description} 完成！总耗时: {elapsed:.2f}秒")


class MultiProgressTracker:
    """多任务进度跟踪器"""

    def __init__(self):
        """初始化多任务进度跟踪器"""
        self.tasks = {}

    def add_task(self, task_id: str, total: int, description: str):
        """添加任务

        Args:
            task_id: 任务ID
            total: 总数
            description: 任务描述
        """
        self.tasks[task_id] = {
            'tracker': ProgressTracker(total, description),
            'total': total,
            'completed': 0
        }

    def update(self, task_id: str, increment: int = 1):
        """更新任务进度

        Args:
            task_id: 任务ID
            increment: 增加的数量
        """
        if task_id in self.tasks:
            self.tasks[task_id]['tracker'].update(increment)
            self.tasks[task_id]['completed'] += increment

    def get_overall_progress(self) -> float:
        """获取整体进度

        Returns:
            整体完成百分比
        """
        if not self.tasks:
            return 0.0

        total_items = sum(task['total'] for task in self.tasks.values())
        completed_items = sum(task['completed'] for task in self.tasks.values())

        if total_items == 0:
            return 0.0

        return (completed_items / total_items) * 100

    def print_summary(self):
        """打印汇总信息"""
        print("\n" + "=" * 60)
        print("任务汇总")
        print("=" * 60)

        for task_id, task in self.tasks.items():
            tracker = task['tracker']
            percentage = (task['completed'] / task['total'] * 100) if task['total'] > 0 else 0
            print(f"{task_id}: {task['completed']}/{task['total']} ({percentage:.1f}%)")

        overall = self.get_overall_progress()
        print(f"\n整体进度: {overall:.1f}%")
        print("=" * 60)
