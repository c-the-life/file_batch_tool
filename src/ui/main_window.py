import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QFileDialog,
    QSpinBox, QGroupBox, QMessageBox, QProgressBar, QDateTimeEdit, QScrollArea, QCheckBox
)
from PyQt5.QtCore import Qt, QDateTime, QSize, QMimeData, QThread
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QDragEnterEvent, QDropEvent
from src.core.worker import WorkerThread
from src.utils.ai_assistant import AIAssistant


class DragDropLineEdit(QLineEdit):
    """支持拖拽文件夹、单个文件和多个文件的输入框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.file_list_separator = "|||"
        self.on_files_changed = None
        
    def set_files_changed_callback(self, callback):
        self.on_files_changed = callback
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    path = Path(url.toLocalFile())
                    if path.is_dir() or path.is_file():
                        event.acceptProposedAction()
                        return
        event.ignore()
        
    def dropEvent(self, event: QDropEvent):
        paths = []
        for url in event.mimeData().urls():
            if url.isLocalFile():
                path_str = url.toLocalFile()
                path = Path(path_str)
                if path.is_dir() or path.is_file():
                    paths.append(path_str)
        
        if paths:
            if len(paths) == 1:
                self.setText(paths[0])
            else:
                self.setText(self.file_list_separator.join(paths))
            event.acceptProposedAction()
            if self.on_files_changed:
                self.on_files_changed()
        else:
            event.ignore()


class FileToolMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ai_assistant = AIAssistant()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("文件批量处理工具")
        self.setGeometry(100, 100, 1100, 750)
        self.setMinimumSize(900, 600)

        font = QFont("Segoe UI", 10)
        self.setFont(font)

        self.setStyleSheet(self.get_stylesheet())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        title_label = QLabel("📁 文件批量处理工具")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2d3748;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        version_label = QLabel("v1.2")
        version_label.setStyleSheet("color: #718096; font-size: 12px;")
        header_layout.addWidget(version_label)

        main_layout.addLayout(header_layout)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setStyleSheet("""
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: #f7fafc;
                color: #4a5568;
                padding: 10px 24px;
                margin: 0 4px;
                border-radius: 8px 8px 0 0;
                font-size: 13px;
                font-weight: 500;
                min-width: 100px;
            }
            QTabBar::tab:hover {
                background: #edf2f7;
            }
            QTabBar::tab:selected {
                background: white;
                color: #2b6cb0;
                border-bottom: 3px solid #3182ce;
            }
        """)
        main_layout.addWidget(self.tab_widget)

        self.init_ai_tab()
        self.init_rename_tab()
        self.init_convert_img_tab()
        self.init_compress_tab()
        self.init_classify_tab()
        self.init_watermark_tab()
        self.init_modify_time_tab()
        self.init_extract_exif_tab()
        self.init_copy_move_tab()

    def init_ai_tab(self):
        """AI智能助手界面"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        ai_group = QGroupBox("🤖 AI 智能助手")
        ai_layout = QVBoxLayout(ai_group)
        ai_layout.setSpacing(16)

        desc_label = QLabel("用自然语言告诉我要做什么，我来帮您自动完成！")
        desc_label.setStyleSheet("color: #4a5568; font-size: 14px;")
        ai_layout.addWidget(desc_label)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)
        
        self.ai_input = QLineEdit()
        self.ai_input.setPlaceholderText("例如：把图片转换成webp格式，给图片加水印...")
        self.ai_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 14px 18px;
                font-size: 14px;
                min-height: 48px;
            }
            QLineEdit:focus {
                border-color: #3182ce;
            }
        """)
        input_layout.addWidget(self.ai_input)

        ai_button = QPushButton("发送")
        ai_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #48bb78, stop:1 #38a169);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px 32px;
                font-size: 14px;
                font-weight: 600;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68d391, stop:1 #48bb78);
            }
        """)
        ai_button.clicked.connect(self.on_ai_command)
        input_layout.addWidget(ai_button)

        ai_layout.addLayout(input_layout)

        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setSpacing(12)
        
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("""
            QTextEdit {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 16px;
                font-size: 14px;
                min-height: 200px;
            }
        """)
        self.chat_history.setText("🤖 你好！我是您的文件处理助手。\n\n请告诉我您想做什么，例如：\n- 把图片转换成webp格式\n- 给图片加水印\n- 按扩展名分类文件\n- 提取图片EXIF信息\n\n您可以先选择文件，然后告诉我要执行什么操作。")
        
        chat_layout.addWidget(self.chat_history)
        ai_layout.addWidget(chat_container)

        hint_group = QGroupBox("💡 支持的命令")
        hint_layout = QVBoxLayout(hint_group)
        
        hint_text = QTextEdit()
        hint_text.setReadOnly(True)
        hint_text.setStyleSheet("""
            QTextEdit {
                background: #ebf8ff;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                color: #2c7a7b;
            }
        """)
        
        commands = self.ai_assistant.get_supported_commands()
        hint_content = "我可以帮您完成以下任务：\n\n"
        for cmd in commands:
            hint_content += f"• {cmd['description']}\n"
            for example in cmd['examples'][:2]:
                hint_content += f"  - {example}\n"
            hint_content += "\n"
        
        hint_text.setText(hint_content)
        hint_layout.addWidget(hint_text)
        
        ai_layout.addWidget(hint_group)

        layout.addWidget(ai_group)

        self.tab_widget.addTab(tab, "🤖 AI助手")

    def on_ai_command(self):
        """处理AI命令"""
        user_input = self.ai_input.text().strip()
        if not user_input:
            return

        self.chat_history.append(f"\n\n👤 您说：{user_input}")
        self.ai_input.clear()

        parsed, response = self.ai_assistant.generate_response(user_input)
        self.chat_history.append(f"\n🤖 {response}")

        if parsed:
            self.execute_ai_command(parsed)

    def execute_ai_command(self, command):
        """执行AI解析的命令"""
        cmd_type = command['command']
        params = command['params']
        
        if cmd_type == 'convert':
            target_format = params.get('to_format', 'webp')
            self.tab_widget.setCurrentIndex(2)
            self.convert_to_format.setCurrentText(target_format.upper())
            self.chat_history.append(f"\n✅ 已切换到图片转换功能，目标格式：{target_format}")
            
        elif cmd_type == 'watermark':
            self.tab_widget.setCurrentIndex(5)
            self.chat_history.append("\n✅ 已切换到图片水印功能")
            
        elif cmd_type == 'rename':
            self.tab_widget.setCurrentIndex(1)
            if 'prefix' in params:
                self.rename_prefix.setText(params['prefix'])
            if 'suffix' in params:
                self.rename_suffix.setText(params['suffix'])
            self.chat_history.append("\n✅ 已切换到批量重命名功能")
            
        elif cmd_type == 'classify':
            by_type = params.get('by_type', 'extension')
            self.tab_widget.setCurrentIndex(4)
            if by_type == 'date':
                self.classify_by_combo.setCurrentIndex(1)
            else:
                self.classify_by_combo.setCurrentIndex(0)
            self.chat_history.append("\n✅ 已切换到文件分类功能")
            
        elif cmd_type == 'exif':
            self.tab_widget.setCurrentIndex(7)
            self.chat_history.append("\n✅ 已切换到EXIF提取功能")
            
        elif cmd_type == 'compress':
            self.tab_widget.setCurrentIndex(3)
            self.chat_history.append("\n✅ 已切换到文件压缩功能")
            
        elif cmd_type == 'copy' or cmd_type == 'move':
            self.tab_widget.setCurrentIndex(8)
            if cmd_type == 'move':
                self.copy_move_combo.setCurrentIndex(1)
            else:
                self.copy_move_combo.setCurrentIndex(0)
            if 'target_dir' in params:
                self.copy_move_target.setText(params['target_dir'])
            self.chat_history.append("\n✅ 已切换到批量复制/移动功能")
            
        elif cmd_type == 'modify_time':
            self.tab_widget.setCurrentIndex(6)
            self.chat_history.append("\n✅ 已切换到修改文件时间功能")

    def get_stylesheet(self):
        return """
            QWidget {
                background-color: #f7fafc;
            }
            QGroupBox {
                background: white;
                border: none;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 8px;
            }
            QGroupBox::title {
                color: #2d3748;
                font-size: 14px;
                font-weight: 600;
                padding: 0 8px;
                margin-left: 8px;
            }
            QLineEdit {
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                color: #2d3748;
                selection-background-color: #bee3f8;
            }
            QLineEdit:focus {
                border-color: #3182ce;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #a0aec0;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e53e3e, stop:1 #c53030);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fc8181, stop:1 #e53e3e);
            }
            QPushButton:pressed {
                background: #9b2c2c;
            }
            QPushButton:disabled {
                background: #a0aec0;
            }
            QComboBox {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                color: #2d3748;
                min-width: 180px;
            }
            QComboBox:focus {
                border-color: #3182ce;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(:/icons/down_arrow.png);
                width: 16px;
                height: 16px;
            }
            QSpinBox {
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: #2d3748;
            }
            QSpinBox:focus {
                border-color: #3182ce;
                outline: none;
            }
            QTextEdit {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                color: #2d3748;
            }
            QProgressBar {
                background: #e2e8f0;
                border: none;
                border-radius: 8px;
                height: 12px;
                text-align: center;
                font-size: 11px;
                color: #2d3748;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3182ce, stop:1 #63b3ed);
                border-radius: 8px;
            }
            QDateTimeEdit {
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: #2d3748;
            }
            QDateTimeEdit:focus {
                border-color: #3182ce;
                outline: none;
            }
            QCheckBox {
                font-size: 13px;
                color: #2d3748;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #e2e8f0;
                background: white;
            }
            QCheckBox::indicator:checked {
                background: #3182ce;
                border-color: #3182ce;
            }
        """

    def init_rename_tab(self):
        """批量重命名界面"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        file_group = QGroupBox("选择文件")
        file_layout = QVBoxLayout(file_group)

        self.rename_input = DragDropLineEdit()
        self.rename_input.setPlaceholderText("拖拽文件到这里，或点击下方按钮选择")
        file_layout.addWidget(self.rename_input)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        select_btn = QPushButton("选择文件")
        select_btn.clicked.connect(lambda: self.select_files(self.rename_input))
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()

        file_layout.addLayout(btn_layout)
        layout.addWidget(file_group)

        setting_group = QGroupBox("重命名设置")
        setting_layout = QVBoxLayout(setting_group)
        setting_layout.setSpacing(16)

        row1 = QHBoxLayout()
        row1.setSpacing(20)

        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(QLabel("前缀："))
        self.rename_prefix = QLineEdit()
        self.rename_prefix.setPlaceholderText("输入前缀")
        prefix_layout.addWidget(self.rename_prefix)
        row1.addLayout(prefix_layout)

        suffix_layout = QHBoxLayout()
        suffix_layout.addWidget(QLabel("后缀："))
        self.rename_suffix = QLineEdit()
        self.rename_suffix.setPlaceholderText("输入后缀")
        suffix_layout.addWidget(self.rename_suffix)
        row1.addLayout(suffix_layout)

        setting_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(20)

        start_num_layout = QHBoxLayout()
        start_num_layout.addWidget(QLabel("起始编号："))
        self.rename_start_num = QSpinBox()
        self.rename_start_num.setRange(1, 9999)
        self.rename_start_num.setValue(1)
        start_num_layout.addWidget(self.rename_start_num)
        row2.addLayout(start_num_layout)

        num_digits_layout = QHBoxLayout()
        num_digits_layout.addWidget(QLabel("编号位数："))
        self.rename_num_digits = QSpinBox()
        self.rename_num_digits.setRange(1, 6)
        self.rename_num_digits.setValue(3)
        num_digits_layout.addWidget(self.rename_num_digits)
        row2.addLayout(num_digits_layout)

        setting_layout.addLayout(row2)
        layout.addWidget(setting_group)

        progress_group = QGroupBox("进度")
        progress_layout = QVBoxLayout(progress_group)
        self.rename_progress = QProgressBar()
        self.rename_progress.setValue(0)
        progress_layout.addWidget(self.rename_progress)
        layout.addWidget(progress_group)

        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout(log_group)
        self.rename_log = QTextEdit()
        self.rename_log.setReadOnly(True)
        self.rename_log.setMaximumHeight(150)
        log_layout.addWidget(self.rename_log)
        layout.addWidget(log_group)

        apply_btn = QPushButton("应用")
        apply_btn.clicked.connect(self.rename_files)
        layout.addWidget(apply_btn)

        self.tab_widget.addTab(tab, "🏷️ 批量重命名")

    def init_convert_img_tab(self):
        """图片格式转换界面"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        file_group = QGroupBox("选择图片")
        file_layout = QVBoxLayout(file_group)

        self.convert_input = DragDropLineEdit()
        self.convert_input.setPlaceholderText("拖拽图片文件夹或图片文件到这里")
        file_layout.addWidget(self.convert_input)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        select_btn = QPushButton("选择文件夹")
        select_btn.clicked.connect(lambda: self.select_folder(self.convert_input))
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()

        file_layout.addLayout(btn_layout)
        layout.addWidget(file_group)

        setting_group = QGroupBox("转换设置")
        setting_layout = QVBoxLayout(setting_group)
        setting_layout.setSpacing(16)

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("目标格式："))
        self.convert_to_format = QComboBox()
        self.convert_to_format.addItems(["JPG", "PNG", "WEBP"])
        format_layout.addWidget(self.convert_to_format)
        setting_layout.addLayout(format_layout)

        layout.addWidget(setting_group)

        progress_group = QGroupBox("进度")
        progress_layout = QVBoxLayout(progress_group)
        self.convert_progress = QProgressBar()
        self.convert_progress.setValue(0)
        progress_layout.addWidget(self.convert_progress)
        layout.addWidget(progress_group)

        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout(log_group)
        self.convert_log = QTextEdit()
        self.convert_log.setReadOnly(True)
        self.convert_log.setMaximumHeight(150)
        log_layout.addWidget(self.convert_log)
        layout.addWidget(log_group)

        apply_btn = QPushButton("转换")
        apply_btn.clicked.connect(self.convert_images)
        layout.addWidget(apply_btn)

        self.tab_widget.addTab(tab, "🖼️ 图片转换")

    def init_compress_tab(self):
        """文件压缩界面"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        file_group = QGroupBox("选择文件")
        file_layout = QVBoxLayout(file_group)

        self.compress_input = DragDropLineEdit()
        self.compress_input.setPlaceholderText("拖拽文件或文件夹到这里")
        file_layout.addWidget(self.compress_input)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        select_btn = QPushButton("选择文件")
        select_btn.clicked.connect(lambda: self.select_files(self.compress_input))
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()

        file_layout.addLayout(btn_layout)
        layout.addWidget(file_group)

        setting_group = QGroupBox("压缩设置")
        setting_layout = QVBoxLayout(setting_group)
        setting_layout.setSpacing(16)

        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出路径："))
        self.compress_output = QLineEdit()
        self.compress_output.setPlaceholderText("自动生成")
        output_layout.addWidget(self.compress_output)
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_compress_output)
        output_layout.addWidget(browse_btn)
        setting_layout.addLayout(output_layout)

        layout.addWidget(setting_group)

        progress_group = QGroupBox("进度")
        progress_layout = QVBoxLayout(progress_group)
        self.compress_progress = QProgressBar()
        self.compress_progress.setValue(0)
        progress_layout.addWidget(self.compress_progress)
        layout.addWidget(progress_group)

        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout(log_group)
        self.compress_log = QTextEdit()
        self.compress_log.setReadOnly(True)
        self.compress_log.setMaximumHeight(150)
        log_layout.addWidget(self.compress_log)
        layout.addWidget(log_group)

        apply_btn = QPushButton("压缩")
        apply_btn.clicked.connect(self.compress_files)
        layout.addWidget(apply_btn)

        self.tab_widget.addTab(tab, "📦 文件压缩")

    def init_classify_tab(self):
        """文件分类界面"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        file_group = QGroupBox("选择文件")
        file_layout = QVBoxLayout(file_group)

        self.classify_input = DragDropLineEdit()
        self.classify_input.setPlaceholderText("拖拽文件或文件夹到这里")
        file_layout.addWidget(self.classify_input)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        select_btn = QPushButton("选择文件")
        select_btn.clicked.connect(lambda: self.select_files(self.classify_input))
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()

        file_layout.addLayout(btn_layout)
        layout.addWidget(file_group)

        setting_group = QGroupBox("分类设置")
        setting_layout = QVBoxLayout(setting_group)
        setting_layout.setSpacing(16)

        by_layout = QHBoxLayout()
        by_layout.addWidget(QLabel("分类方式："))
        self.classify_by_combo = QComboBox()
        self.classify_by_combo.addItems(["按扩展名", "按日期"])
        by_layout.addWidget(self.classify_by_combo)
        setting_layout.addLayout(by_layout)

        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录："))
        self.classify_output = QLineEdit()
        self.classify_output.setPlaceholderText("自动生成")
        output_layout.addWidget(self.classify_output)
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_classify_output)
        output_layout.addWidget(browse_btn)
        setting_layout.addLayout(output_layout)

        layout.addWidget(setting_group)

        progress_group = QGroupBox("进度")
        progress_layout = QVBoxLayout(progress_group)
        self.classify_progress = QProgressBar()
        self.classify_progress.setValue(0)
        progress_layout.addWidget(self.classify_progress)
        layout.addWidget(progress_group)

        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout(log_group)
        self.classify_log = QTextEdit()
        self.classify_log.setReadOnly(True)
        self.classify_log.setMaximumHeight(150)
        log_layout.addWidget(self.classify_log)
        layout.addWidget(log_group)

        apply_btn = QPushButton("分类")
        apply_btn.clicked.connect(self.classify_files)
        layout.addWidget(apply_btn)

        self.tab_widget.addTab(tab, "📂 文件分类")

    def init_watermark_tab(self):
        """图片水印界面"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        file_group = QGroupBox("选择图片")
        file_layout = QVBoxLayout(file_group)

        self.watermark_input = DragDropLineEdit()
        self.watermark_input.setPlaceholderText("拖拽图片文件夹或图片文件到这里")
        file_layout.addWidget(self.watermark_input)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        select_btn = QPushButton("选择文件夹")
        select_btn.clicked.connect(lambda: self.select_folder(self.watermark_input))
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()

        file_layout.addLayout(btn_layout)
        layout.addWidget(file_group)

        setting_group = QGroupBox("水印设置")
        setting_layout = QVBoxLayout(setting_group)
        setting_layout.setSpacing(16)

        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("水印类型："))
        self.watermark_type = QComboBox()
        self.watermark_type.addItems(["文字水印", "图片水印"])
        self.watermark_type.currentIndexChanged.connect(self.toggle_watermark_settings)
        type_layout.addWidget(self.watermark_type)
        setting_layout.addLayout(type_layout)

        self.text_watermark_group = QGroupBox("文字水印设置")
        text_layout = QVBoxLayout(self.text_watermark_group)

        text_content_layout = QHBoxLayout()
        text_content_layout.addWidget(QLabel("水印文字："))
        self.watermark_text = QLineEdit()
        self.watermark_text.setText("© 版权所有")
        text_content_layout.addWidget(self.watermark_text)
        text_layout.addLayout(text_content_layout)

        text_color_layout = QHBoxLayout()
        text_color_layout.addWidget(QLabel("文字颜色："))
        self.watermark_color = QLineEdit()
        self.watermark_color.setText("#FFFFFF")
        text_color_layout.addWidget(self.watermark_color)
        text_layout.addLayout(text_color_layout)

        text_size_layout = QHBoxLayout()
        text_size_layout.addWidget(QLabel("文字大小："))
        self.watermark_size = QSpinBox()
        self.watermark_size.setRange(10, 100)
        self.watermark_size.setValue(24)
        text_size_layout.addWidget(self.watermark_size)
        text_layout.addLayout(text_size_layout)

        text_opacity_layout = QHBoxLayout()
        text_opacity_layout.addWidget(QLabel("透明度："))
        self.watermark_opacity = QSpinBox()
        self.watermark_opacity.setRange(1, 100)
        self.watermark_opacity.setValue(50)
        text_opacity_layout.addWidget(self.watermark_opacity)
        text_layout.addLayout(text_opacity_layout)

        setting_layout.addWidget(self.text_watermark_group)

        self.image_watermark_group = QGroupBox("图片水印设置")
        image_layout = QVBoxLayout(self.image_watermark_group)

        image_path_layout = QHBoxLayout()
        image_path_layout.addWidget(QLabel("水印图片："))
        self.watermark_image_path = QLineEdit()
        image_path_layout.addWidget(self.watermark_image_path)
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_watermark_image)
        image_path_layout.addWidget(browse_btn)
        image_layout.addLayout(image_path_layout)

        image_opacity_layout = QHBoxLayout()
        image_opacity_layout.addWidget(QLabel("透明度："))
        self.watermark_image_opacity = QSpinBox()
        self.watermark_image_opacity.setRange(1, 100)
        self.watermark_image_opacity.setValue(50)
        image_opacity_layout.addWidget(self.watermark_image_opacity)
        image_layout.addLayout(image_opacity_layout)

        setting_layout.addWidget(self.image_watermark_group)

        self.image_watermark_group.hide()

        layout.addWidget(setting_group)

        progress_group = QGroupBox("进度")
        progress_layout = QVBoxLayout(progress_group)
        self.watermark_progress = QProgressBar()
        self.watermark_progress.setValue(0)
        progress_layout.addWidget(self.watermark_progress)
        layout.addWidget(progress_group)

        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout(log_group)
        self.watermark_log = QTextEdit()
        self.watermark_log.setReadOnly(True)
        self.watermark_log.setMaximumHeight(150)
        log_layout.addWidget(self.watermark_log)
        layout.addWidget(log_group)

        apply_btn = QPushButton("添加水印")
        apply_btn.clicked.connect(self.add_watermark)
        layout.addWidget(apply_btn)

        self.tab_widget.addTab(tab, "💧 图片水印")

    def init_modify_time_tab(self):
        """修改文件时间界面"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        file_group = QGroupBox("选择文件")
        file_layout = QVBoxLayout(file_group)

        self.modify_time_input = DragDropLineEdit()
        self.modify_time_input.setPlaceholderText("拖拽文件或文件夹到这里")
        file_layout.addWidget(self.modify_time_input)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        select_btn = QPushButton("选择文件")
        select_btn.clicked.connect(lambda: self.select_files(self.modify_time_input))
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()

        file_layout.addLayout(btn_layout)
        layout.addWidget(file_group)

        setting_group = QGroupBox("时间设置")
        setting_layout = QVBoxLayout(setting_group)
        setting_layout.setSpacing(16)

        create_time_layout = QHBoxLayout()
        create_time_layout.addWidget(QLabel("创建时间："))
        self.create_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.create_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        create_time_layout.addWidget(self.create_time_edit)
        setting_layout.addLayout(create_time_layout)

        modify_time_layout = QHBoxLayout()
        modify_time_layout.addWidget(QLabel("修改时间："))
        self.modify_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.modify_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        modify_time_layout.addWidget(self.modify_time_edit)
        setting_layout.addLayout(modify_time_layout)

        layout.addWidget(setting_group)

        progress_group = QGroupBox("进度")
        progress_layout = QVBoxLayout(progress_group)
        self.modify_time_progress = QProgressBar()
        self.modify_time_progress.setValue(0)
        progress_layout.addWidget(self.modify_time_progress)
        layout.addWidget(progress_group)

        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout(log_group)
        self.modify_time_log = QTextEdit()
        self.modify_time_log.setReadOnly(True)
        self.modify_time_log.setMaximumHeight(150)
        log_layout.addWidget(self.modify_time_log)
        layout.addWidget(log_group)

        apply_btn = QPushButton("修改时间")
        apply_btn.clicked.connect(self.modify_file_time)
        layout.addWidget(apply_btn)

        self.tab_widget.addTab(tab, "⏰ 修改时间")

    def init_extract_exif_tab(self):
        """提取EXIF信息界面"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        file_group = QGroupBox("选择图片")
        file_layout = QVBoxLayout(file_group)

        self.exif_input = DragDropLineEdit()
        self.exif_input.setPlaceholderText("拖拽图片文件夹或图片文件到这里")
        file_layout.addWidget(self.exif_input)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        select_btn = QPushButton("选择文件夹")
        select_btn.clicked.connect(lambda: self.select_folder(self.exif_input))
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()

        file_layout.addLayout(btn_layout)
        layout.addWidget(file_group)

        setting_group = QGroupBox("输出设置")
        setting_layout = QVBoxLayout(setting_group)
        setting_layout.setSpacing(16)

        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出CSV路径："))
        self.exif_output = QLineEdit()
        self.exif_output.setPlaceholderText("自动生成")
        output_layout.addWidget(self.exif_output)
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_exif_output)
        output_layout.addWidget(browse_btn)
        setting_layout.addLayout(output_layout)

        layout.addWidget(setting_group)

        progress_group = QGroupBox("进度")
        progress_layout = QVBoxLayout(progress_group)
        self.exif_progress = QProgressBar()
        self.exif_progress.setValue(0)
        progress_layout.addWidget(self.exif_progress)
        layout.addWidget(progress_group)

        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout(log_group)
        self.exif_log = QTextEdit()
        self.exif_log.setReadOnly(True)
        self.exif_log.setMaximumHeight(150)
        log_layout.addWidget(self.exif_log)
        layout.addWidget(log_group)

        apply_btn = QPushButton("提取EXIF")
        apply_btn.clicked.connect(self.extract_exif)
        layout.addWidget(apply_btn)

        self.tab_widget.addTab(tab, "📊 提取EXIF")

    def init_copy_move_tab(self):
        """复制/移动文件界面"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        file_group = QGroupBox("选择文件")
        file_layout = QVBoxLayout(file_group)

        self.copy_move_input = DragDropLineEdit()
        self.copy_move_input.setPlaceholderText("拖拽文件或文件夹到这里")
        file_layout.addWidget(self.copy_move_input)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        select_btn = QPushButton("选择文件")
        select_btn.clicked.connect(lambda: self.select_files(self.copy_move_input))
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()

        file_layout.addLayout(btn_layout)
        layout.addWidget(file_group)

        setting_group = QGroupBox("操作设置")
        setting_layout = QVBoxLayout(setting_group)
        setting_layout.setSpacing(16)

        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("操作类型："))
        self.copy_move_combo = QComboBox()
        self.copy_move_combo.addItems(["复制", "移动"])
        type_layout.addWidget(self.copy_move_combo)
        setting_layout.addLayout(type_layout)

        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("目标目录："))
        self.copy_move_target = QLineEdit()
        self.copy_move_target.setPlaceholderText("选择目标目录")
        target_layout.addWidget(self.copy_move_target)
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_copy_move_target)
        target_layout.addWidget(browse_btn)
        setting_layout.addLayout(target_layout)

        layout.addWidget(setting_group)

        progress_group = QGroupBox("进度")
        progress_layout = QVBoxLayout(progress_group)
        self.copy_move_progress = QProgressBar()
        self.copy_move_progress.setValue(0)
        progress_layout.addWidget(self.copy_move_progress)
        layout.addWidget(progress_group)

        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout(log_group)
        self.copy_move_log = QTextEdit()
        self.copy_move_log.setReadOnly(True)
        self.copy_move_log.setMaximumHeight(150)
        log_layout.addWidget(self.copy_move_log)
        layout.addWidget(log_group)

        apply_btn = QPushButton("执行")
        apply_btn.clicked.connect(self.copy_move_files)
        layout.addWidget(apply_btn)

        self.tab_widget.addTab(tab, "📥 复制/移动")

    def toggle_watermark_settings(self):
        """切换水印设置界面"""
        if self.watermark_type.currentText() == "文字水印":
            self.text_watermark_group.show()
            self.image_watermark_group.hide()
        else:
            self.text_watermark_group.hide()
            self.image_watermark_group.show()

    def select_files(self, line_edit):
        """选择多个文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择文件", "", "所有文件 (*.*)"
        )
        if files:
            if len(files) == 1:
                line_edit.setText(files[0])
            else:
                line_edit.setText(line_edit.file_list_separator.join(files))

    def select_folder(self, line_edit):
        """选择文件夹"""
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            line_edit.setText(folder)

    def browse_compress_output(self):
        """浏览压缩输出路径"""
        path, _ = QFileDialog.getSaveFileName(
            self, "选择输出文件", "", "ZIP文件 (*.zip)"
        )
        if path:
            if not path.endswith(".zip"):
                path += ".zip"
            self.compress_output.setText(path)

    def browse_classify_output(self):
        """浏览分类输出目录"""
        folder = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder:
            self.classify_output.setText(folder)

    def browse_watermark_image(self):
        """浏览水印图片"""
        path, _ = QFileDialog.getOpenFileName(
            self, "选择水印图片", "", "图片文件 (*.png *.jpg *.jpeg)"
        )
        if path:
            self.watermark_image_path.setText(path)

    def browse_exif_output(self):
        """浏览EXIF输出路径"""
        path, _ = QFileDialog.getSaveFileName(
            self, "选择输出文件", "", "CSV文件 (*.csv)"
        )
        if path:
            if not path.endswith(".csv"):
                path += ".csv"
            self.exif_output.setText(path)

    def browse_copy_move_target(self):
        """浏览复制/移动目标目录"""
        folder = QFileDialog.getExistingDirectory(self, "选择目标目录")
        if folder:
            self.copy_move_target.setText(folder)

    def get_file_list(self, line_edit):
        """从输入框获取文件列表"""
        text = line_edit.text().strip()
        if not text:
            return []

        if line_edit.file_list_separator in text:
            paths = text.split(line_edit.file_list_separator)
        else:
            paths = [text]

        file_list = []
        for path_str in paths:
            path = Path(path_str)
            if path.is_file():
                file_list.append(path)
            elif path.is_dir():
                for item in path.rglob("*"):
                    if item.is_file():
                        file_list.append(item)

        return file_list

    def rename_files(self):
        """批量重命名"""
        files = self.get_file_list(self.rename_input)
        if not files:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return

        prefix = self.rename_prefix.text()
        suffix = self.rename_suffix.text()
        start_num = self.rename_start_num.value()
        num_digits = self.rename_num_digits.value()

        self.rename_log.clear()
        self.rename_progress.setValue(0)

        worker = WorkerThread(
            task_type="rename",
            files=files,
            prefix=prefix,
            suffix=suffix,
            start_num=start_num,
            num_digits=num_digits
        )
        worker.log_signal.connect(self.rename_log.append)
        worker.progress_signal.connect(self.rename_progress.setValue)
        worker.finished.connect(lambda: QMessageBox.information(self, "完成", "重命名完成"))
        worker.start()

    def convert_images(self):
        """图片格式转换"""
        files = self.get_file_list(self.convert_input)
        if not files:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return

        to_format = self.convert_to_format.currentText().lower()

        self.convert_log.clear()
        self.convert_progress.setValue(0)

        worker = WorkerThread(
            task_type="convert",
            files=files,
            to_format=to_format
        )
        worker.log_signal.connect(self.convert_log.append)
        worker.progress_signal.connect(self.convert_progress.setValue)
        worker.finished.connect(lambda: QMessageBox.information(self, "完成", "转换完成"))
        worker.start()

    def compress_files(self):
        """文件压缩"""
        files = self.get_file_list(self.compress_input)
        if not files:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return

        output = self.compress_output.text().strip()
        if not output:
            output = str(files[0].parent / "compressed.zip")

        self.compress_log.clear()
        self.compress_progress.setValue(0)

        worker = WorkerThread(
            task_type="compress",
            files=files,
            output=output
        )
        worker.log_signal.connect(self.compress_log.append)
        worker.progress_signal.connect(self.compress_progress.setValue)
        worker.finished.connect(lambda: QMessageBox.information(self, "完成", "压缩完成"))
        worker.start()

    def classify_files(self):
        """文件分类"""
        files = self.get_file_list(self.classify_input)
        if not files:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return

        by_type = "date" if self.classify_by_combo.currentIndex() == 1 else "extension"
        output = self.classify_output.text().strip()
        if not output:
            output = str(files[0].parent / "classified")

        self.classify_log.clear()
        self.classify_progress.setValue(0)

        worker = WorkerThread(
            task_type="classify",
            files=files,
            by_type=by_type,
            output=output
        )
        worker.log_signal.connect(self.classify_log.append)
        worker.progress_signal.connect(self.classify_progress.setValue)
        worker.finished.connect(lambda: QMessageBox.information(self, "完成", "分类完成"))
        worker.start()

    def add_watermark(self):
        """添加水印"""
        files = self.get_file_list(self.watermark_input)
        if not files:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return

        if self.watermark_type.currentText() == "文字水印":
            worker = WorkerThread(
                task_type="watermark",
                files=files,
                type_="text",
                content=self.watermark_text.text(),
                color=self.watermark_color.text(),
                font_size=self.watermark_size.value(),
                opacity=self.watermark_opacity.value()
            )
        else:
            watermark_image = self.watermark_image_path.text().strip()
            if not watermark_image:
                QMessageBox.warning(self, "警告", "请选择水印图片")
                return
            worker = WorkerThread(
                task_type="watermark",
                files=files,
                type_="image",
                image_path=watermark_image,
                opacity=self.watermark_image_opacity.value()
            )

        self.watermark_log.clear()
        self.watermark_progress.setValue(0)

        worker.log_signal.connect(self.watermark_log.append)
        worker.progress_signal.connect(self.watermark_progress.setValue)
        worker.finished.connect(lambda: QMessageBox.information(self, "完成", "水印添加完成"))
        worker.start()

    def modify_file_time(self):
        """修改文件时间"""
        files = self.get_file_list(self.modify_time_input)
        if not files:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return

        create_time = self.create_time_edit.dateTime().toPyDateTime()
        modify_time = self.modify_time_edit.dateTime().toPyDateTime()

        self.modify_time_log.clear()
        self.modify_time_progress.setValue(0)

        worker = WorkerThread(
            task_type="modify_time",
            files=files,
            create_time=create_time,
            modify_time=modify_time
        )
        worker.log_signal.connect(self.modify_time_log.append)
        worker.progress_signal.connect(self.modify_time_progress.setValue)
        worker.finished.connect(lambda: QMessageBox.information(self, "完成", "时间修改完成"))
        worker.start()

    def extract_exif(self):
        """提取EXIF信息"""
        files = self.get_file_list(self.exif_input)
        if not files:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return

        output = self.exif_output.text().strip()
        if not output:
            output = str(files[0].parent / "exif_info.csv")

        self.exif_log.clear()
        self.exif_progress.setValue(0)

        worker = WorkerThread(
            task_type="exif",
            files=files,
            output=output
        )
        worker.log_signal.connect(self.exif_log.append)
        worker.progress_signal.connect(self.exif_progress.setValue)
        worker.finished.connect(lambda: QMessageBox.information(self, "完成", "EXIF提取完成"))
        worker.start()

    def copy_move_files(self):
        """复制/移动文件"""
        files = self.get_file_list(self.copy_move_input)
        if not files:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return

        target_dir = self.copy_move_target.text().strip()
        if not target_dir:
            QMessageBox.warning(self, "警告", "请选择目标目录")
            return

        task_type = "move" if self.copy_move_combo.currentIndex() == 1 else "copy"

        self.copy_move_log.clear()
        self.copy_move_progress.setValue(0)

        worker = WorkerThread(
            task_type=task_type,
            files=files,
            target_dir=target_dir
        )
        worker.log_signal.connect(self.copy_move_log.append)
        worker.progress_signal.connect(self.copy_move_progress.setValue)
        worker.finished.connect(lambda: QMessageBox.information(self, "完成", "操作完成"))
        worker.start()



def run():
    """运行文件批量处理工具"""
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    window = FileToolMainWindow()
    window.show()
    sys.exit(app.exec_())
