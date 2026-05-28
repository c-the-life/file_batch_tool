import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QFileDialog,
    QSpinBox, QGroupBox, QMessageBox, QProgressBar, QDateTimeEdit, QScrollArea, QCheckBox
)
from PyQt5.QtCore import Qt, QDateTime, QSize, QMimeData
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QDragEnterEvent, QDropEvent
from src.core.worker import WorkerThread


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

        version_label = QLabel("v1.0")
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

        self.init_rename_tab()
        self.init_convert_img_tab()
        self.init_compress_tab()
        self.init_classify_tab()
        self.init_watermark_tab()
        self.init_modify_time_tab()
        self.init_extract_exif_tab()
        self.init_copy_move_tab()

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
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNiAxMGwtNi00IDYtNCA2IDQtNiA0eiIvPjwvc3ZnPg==);
                width: 12px;
                height: 12px;
            }
            QSpinBox {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                color: #2d3748;
                min-width: 80px;
            }
            QSpinBox:focus {
                border-color: #3182ce;
                outline: none;
            }
            QDateTimeEdit {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                color: #2d3748;
            }
            QDateTimeEdit:focus {
                border-color: #3182ce;
                outline: none;
            }
            QTextEdit {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                color: #2d3748;
            }
            QProgressBar {
                background: #e2e8f0;
                border: none;
                border-radius: 20px;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: linear-gradient(90deg, #3182ce 0%, #38a169 100%);
                border-radius: 20px;
            }
            QMessageBox {
                background: white;
                border-radius: 12px;
            }
        """

    def init_rename_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "批量重命名")

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        dir_group = QGroupBox("目标目录")
        dir_layout = QHBoxLayout(dir_group)
        dir_layout.setSpacing(12)
        self.rename_dir_edit = DragDropLineEdit()
        self.rename_dir_edit.setPlaceholderText("选择目录或文件（支持批量拖拽多个文件）")
        self.rename_dir_edit.setMinimumHeight(40)
        dir_btn = QPushButton("浏览")
        dir_btn.clicked.connect(lambda: self.select_dir(self.rename_dir_edit))
        dir_layout.addWidget(self.rename_dir_edit)
        dir_layout.addWidget(dir_btn)
        layout.addWidget(dir_group)
        
        self.rename_dir_edit.set_files_changed_callback(self.update_rename_file_settings)

        param_group = QGroupBox("整体设置（应用于所有文件）")
        param_layout = QVBoxLayout(param_group)
        param_layout.setSpacing(16)

        # 前缀后缀行
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(16)

        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(QLabel("前缀"))
        prefix_layout.addWidget(QLabel(":"))
        self.rename_prefix_edit = QLineEdit()
        self.rename_prefix_edit.setPlaceholderText("例如：风景_")
        self.rename_prefix_edit.setMinimumWidth(180)
        prefix_layout.addWidget(self.rename_prefix_edit)
        row1_layout.addLayout(prefix_layout)

        suffix_layout = QHBoxLayout()
        suffix_layout.addWidget(QLabel("后缀"))
        suffix_layout.addWidget(QLabel(":"))
        self.rename_suffix_edit = QLineEdit()
        self.rename_suffix_edit.setPlaceholderText("例如：_高清")
        self.rename_suffix_edit.setMinimumWidth(180)
        suffix_layout.addWidget(self.rename_suffix_edit)
        row1_layout.addLayout(suffix_layout)
        row1_layout.addStretch()
        param_layout.addLayout(row1_layout)

        # 启用自动编号复选框
        auto_num_check_layout = QHBoxLayout()
        auto_num_check_layout.setSpacing(12)
        self.rename_use_auto_number = QCheckBox("启用自动编号")
        self.rename_use_auto_number.stateChanged.connect(self.toggle_auto_number)
        auto_num_check_layout.addWidget(self.rename_use_auto_number)
        auto_num_check_layout.addStretch()
        param_layout.addLayout(auto_num_check_layout)

        # 自动编号组
        self.auto_number_group = QGroupBox()
        auto_number_layout = QHBoxLayout(self.auto_number_group)
        auto_number_layout.setSpacing(16)

        name_base_layout = QHBoxLayout()
        name_base_layout.addWidget(QLabel("基础名称"))
        name_base_layout.addWidget(QLabel(":"))
        self.rename_name_base_edit = QLineEdit()
        self.rename_name_base_edit.setPlaceholderText("例如：照片")
        self.rename_name_base_edit.setMinimumWidth(200)
        self.rename_name_base_edit.setText("照片")
        name_base_layout.addWidget(self.rename_name_base_edit)
        auto_number_layout.addLayout(name_base_layout)

        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("起始编号"))
        start_layout.addWidget(QLabel(":"))
        self.rename_start_spin = QSpinBox()
        self.rename_start_spin.setMinimum(1)
        self.rename_start_spin.setMaximum(99999)
        self.rename_start_spin.setValue(1)
        start_layout.addWidget(self.rename_start_spin)
        auto_number_layout.addLayout(start_layout)

        digit_layout = QHBoxLayout()
        digit_layout.addWidget(QLabel("位数"))
        digit_layout.addWidget(QLabel(":"))
        self.rename_digit_spin = QSpinBox()
        self.rename_digit_spin.setMinimum(1)
        self.rename_digit_spin.setMaximum(8)
        self.rename_digit_spin.setValue(3)
        digit_layout.addWidget(self.rename_digit_spin)
        auto_number_layout.addLayout(digit_layout)
        auto_number_layout.addStretch()
        
        self.auto_number_group.setVisible(False)
        param_layout.addWidget(self.auto_number_group)

        layout.addWidget(param_group)

        files_group = QGroupBox("单个文件设置（可滚动）")
        files_layout = QVBoxLayout(files_group)
        files_layout.setSpacing(8)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(200)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.rename_files_container = QWidget()
        self.rename_files_layout = QVBoxLayout(self.rename_files_container)
        self.rename_files_layout.setSpacing(8)
        self.rename_files_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(self.rename_files_container)
        files_layout.addWidget(scroll)
        layout.addWidget(files_group)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(16)
        
        # 应用按钮
        self.rename_run_btn = QPushButton("应用")
        self.rename_run_btn.clicked.connect(self.run_rename)
        action_layout.addWidget(self.rename_run_btn)
        action_layout.addStretch()
        layout.addLayout(action_layout)

        progress_group = QGroupBox("进度")
        progress_layout = QHBoxLayout(progress_group)
        self.rename_progress_bar = QProgressBar()
        self.rename_progress_bar.setRange(0, 100)
        self.rename_progress_bar.setValue(0)
        progress_layout.addWidget(self.rename_progress_bar)
        layout.addWidget(progress_group)

        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(log_group)
        self.rename_log_edit = QTextEdit()
        self.rename_log_edit.setReadOnly(True)
        self.rename_log_edit.setMinimumHeight(150)
        log_layout.addWidget(self.rename_log_edit)
        layout.addWidget(log_group)

    def init_convert_img_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "图片格式转换")

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        dir_group = QGroupBox("图片目录")
        dir_layout = QHBoxLayout(dir_group)
        dir_layout.setSpacing(12)
        self.convert_dir_edit = DragDropLineEdit()
        self.convert_dir_edit.setPlaceholderText("选择目录或图片（支持批量拖拽多个文件）")
        self.convert_dir_edit.setMinimumHeight(40)
        dir_btn = QPushButton("浏览")
        dir_btn.clicked.connect(lambda: self.select_dir(self.convert_dir_edit))
        dir_layout.addWidget(self.convert_dir_edit)
        dir_layout.addWidget(dir_btn)
        layout.addWidget(dir_group)

        format_group = QGroupBox("转换参数")
        format_layout = QHBoxLayout(format_group)
        format_layout.setSpacing(12)
        format_layout.addWidget(QLabel("目标格式"))
        format_layout.addWidget(QLabel(":"))
        self.convert_format_combo = QComboBox()
        self.convert_format_combo.addItems(["jpg", "png", "webp"])
        format_layout.addWidget(self.convert_format_combo)
        format_layout.addStretch()
        layout.addWidget(format_group)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(16)
        self.convert_run_btn = QPushButton("应用")
        self.convert_run_btn.clicked.connect(self.run_convert_img)
        action_layout.addWidget(self.convert_run_btn)
        action_layout.addStretch()
        layout.addLayout(action_layout)

        progress_group = QGroupBox("进度")
        progress_layout = QHBoxLayout(progress_group)
        self.convert_progress_bar = QProgressBar()
        self.convert_progress_bar.setRange(0, 100)
        self.convert_progress_bar.setValue(0)
        progress_layout.addWidget(self.convert_progress_bar)
        layout.addWidget(progress_group)

        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(log_group)
        self.convert_log_edit = QTextEdit()
        self.convert_log_edit.setReadOnly(True)
        self.convert_log_edit.setMinimumHeight(150)
        log_layout.addWidget(self.convert_log_edit)
        layout.addWidget(log_group)

    def init_compress_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "文件压缩")

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        dir_group = QGroupBox("目标目录")
        dir_layout = QHBoxLayout(dir_group)
        dir_layout.setSpacing(12)
        self.compress_dir_edit = DragDropLineEdit()
        self.compress_dir_edit.setPlaceholderText("选择目录或文件（支持批量拖拽多个文件）")
        self.compress_dir_edit.setMinimumHeight(40)
        dir_btn = QPushButton("浏览")
        dir_btn.clicked.connect(lambda: self.select_dir(self.compress_dir_edit))
        dir_layout.addWidget(self.compress_dir_edit)
        dir_layout.addWidget(dir_btn)
        layout.addWidget(dir_group)

        output_group = QGroupBox("输出设置")
        output_layout = QVBoxLayout(output_group)
        output_layout.setSpacing(16)

        output_layout1 = QHBoxLayout()
        output_layout1.setSpacing(12)
        output_layout1.addWidget(QLabel("压缩包路径"))
        output_layout1.addWidget(QLabel(":"))
        self.compress_output_edit = QLineEdit()
        self.compress_output_edit.setPlaceholderText("默认：目录名_compressed.zip")
        output_btn = QPushButton("浏览")
        output_btn.clicked.connect(lambda: self.select_save_file(self.compress_output_edit, "ZIP压缩包 (*.zip)"))
        output_layout1.addWidget(self.compress_output_edit)
        output_layout1.addWidget(output_btn)
        output_layout.addLayout(output_layout1)

        exclude_layout = QHBoxLayout()
        exclude_layout.setSpacing(12)
        exclude_layout.addWidget(QLabel("排除扩展名"))
        exclude_layout.addWidget(QLabel(":"))
        self.compress_exclude_edit = QLineEdit()
        self.compress_exclude_edit.setPlaceholderText("例如：zip,log,tmp")
        exclude_layout.addWidget(self.compress_exclude_edit)
        exclude_layout.addStretch()
        output_layout.addLayout(exclude_layout)

        layout.addWidget(output_group)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(16)
        self.compress_run_btn = QPushButton("应用")
        self.compress_run_btn.clicked.connect(self.run_compress)
        action_layout.addWidget(self.compress_run_btn)
        action_layout.addStretch()
        layout.addLayout(action_layout)

        progress_group = QGroupBox("进度")
        progress_layout = QHBoxLayout(progress_group)
        self.compress_progress_bar = QProgressBar()
        self.compress_progress_bar.setRange(0, 100)
        self.compress_progress_bar.setValue(0)
        progress_layout.addWidget(self.compress_progress_bar)
        layout.addWidget(progress_group)

        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(log_group)
        self.compress_log_edit = QTextEdit()
        self.compress_log_edit.setReadOnly(True)
        self.compress_log_edit.setMinimumHeight(150)
        log_layout.addWidget(self.compress_log_edit)
        layout.addWidget(log_group)

    def init_classify_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "文件分类")

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        dir_group = QGroupBox("目标目录")
        dir_layout = QHBoxLayout(dir_group)
        dir_layout.setSpacing(12)
        self.classify_dir_edit = DragDropLineEdit()
        self.classify_dir_edit.setPlaceholderText("选择目录或文件（支持批量拖拽多个文件）")
        self.classify_dir_edit.setMinimumHeight(40)
        dir_btn = QPushButton("浏览")
        dir_btn.clicked.connect(lambda: self.select_dir(self.classify_dir_edit))
        dir_layout.addWidget(self.classify_dir_edit)
        dir_layout.addWidget(dir_btn)
        layout.addWidget(dir_group)

        mode_group = QGroupBox("分类模式")
        mode_layout = QHBoxLayout(mode_group)
        mode_layout.setSpacing(12)
        mode_layout.addWidget(QLabel("分类方式"))
        mode_layout.addWidget(QLabel(":"))
        self.classify_mode_combo = QComboBox()
        self.classify_mode_combo.addItems(["按扩展名", "按创建日期"])
        mode_layout.addWidget(self.classify_mode_combo)
        mode_layout.addStretch()
        layout.addWidget(mode_group)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(16)
        self.classify_run_btn = QPushButton("应用")
        self.classify_run_btn.clicked.connect(self.run_classify)
        action_layout.addWidget(self.classify_run_btn)
        action_layout.addStretch()
        layout.addLayout(action_layout)

        progress_group = QGroupBox("进度")
        progress_layout = QHBoxLayout(progress_group)
        self.classify_progress_bar = QProgressBar()
        self.classify_progress_bar.setRange(0, 100)
        self.classify_progress_bar.setValue(0)
        progress_layout.addWidget(self.classify_progress_bar)
        layout.addWidget(progress_group)

        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(log_group)
        self.classify_log_edit = QTextEdit()
        self.classify_log_edit.setReadOnly(True)
        self.classify_log_edit.setMinimumHeight(150)
        log_layout.addWidget(self.classify_log_edit)
        layout.addWidget(log_group)

    def init_watermark_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "图片加水印")

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        dir_group = QGroupBox("图片目录")
        dir_layout = QHBoxLayout(dir_group)
        dir_layout.setSpacing(12)
        self.watermark_dir_edit = DragDropLineEdit()
        self.watermark_dir_edit.setPlaceholderText("选择目录或图片（支持批量拖拽多个文件）")
        self.watermark_dir_edit.setMinimumHeight(40)
        dir_btn = QPushButton("浏览")
        dir_btn.clicked.connect(lambda: self.select_dir(self.watermark_dir_edit))
        dir_layout.addWidget(self.watermark_dir_edit)
        dir_layout.addWidget(dir_btn)
        layout.addWidget(dir_group)

        type_group = QGroupBox("水印类型")
        type_layout = QHBoxLayout(type_group)
        type_layout.setSpacing(12)
        type_layout.addWidget(QLabel("类型"))
        type_layout.addWidget(QLabel(":"))
        self.watermark_type_combo = QComboBox()
        self.watermark_type_combo.addItems(["文字水印", "图片水印"])
        self.watermark_type_combo.currentTextChanged.connect(self.switch_watermark_type)
        type_layout.addWidget(self.watermark_type_combo)
        type_layout.addStretch()
        layout.addWidget(type_group)

        self.text_watermark_group = QGroupBox("文字水印参数")
        text_layout = QVBoxLayout(self.text_watermark_group)
        text_layout.setSpacing(16)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)
        content_layout.addWidget(QLabel("水印文字"))
        content_layout.addWidget(QLabel(":"))
        self.watermark_content_edit = QLineEdit()
        self.watermark_content_edit.setPlaceholderText("例如：我的作品")
        content_layout.addWidget(self.watermark_content_edit)
        content_layout.addStretch()
        text_layout.addLayout(content_layout)

        font_layout = QHBoxLayout()
        font_layout.setSpacing(12)
        font_layout.addWidget(QLabel("字体文件"))
        font_layout.addWidget(QLabel(":"))
        self.watermark_font_edit = QLineEdit()
        self.watermark_font_edit.setPlaceholderText("可选，默认字体")
        font_btn = QPushButton("浏览")
        font_btn.clicked.connect(lambda: self.select_file(self.watermark_font_edit, "字体文件 (*.ttf *.otf)"))
        font_layout.addWidget(self.watermark_font_edit)
        font_layout.addWidget(font_btn)
        font_layout.addStretch()
        text_layout.addLayout(font_layout)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(16)

        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("文字大小"))
        size_layout.addWidget(QLabel(":"))
        self.watermark_size_spin = QSpinBox()
        self.watermark_size_spin.setRange(8, 100)
        self.watermark_size_spin.setValue(24)
        size_layout.addWidget(self.watermark_size_spin)
        row_layout.addLayout(size_layout)

        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("颜色(RGBA)"))
        color_layout.addWidget(QLabel(":"))
        self.watermark_color_edit = QLineEdit()
        self.watermark_color_edit.setPlaceholderText("例如：(255,255,255,128)")
        self.watermark_color_edit.setText("(255,255,255,128)")
        color_layout.addWidget(self.watermark_color_edit)
        row_layout.addLayout(color_layout)

        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("透明度"))
        opacity_layout.addWidget(QLabel(":"))
        self.watermark_opacity_spin = QSpinBox()
        self.watermark_opacity_spin.setRange(0, 255)
        self.watermark_opacity_spin.setValue(128)
        opacity_layout.addWidget(self.watermark_opacity_spin)
        row_layout.addLayout(opacity_layout)
        row_layout.addStretch()
        text_layout.addLayout(row_layout)

        layout.addWidget(self.text_watermark_group)

        self.image_watermark_group = QGroupBox("图片水印参数")
        image_layout = QVBoxLayout(self.image_watermark_group)
        image_layout.setSpacing(16)
        self.image_watermark_group.setVisible(False)

        watermark_path_layout = QHBoxLayout()
        watermark_path_layout.setSpacing(12)
        watermark_path_layout.addWidget(QLabel("水印图片"))
        watermark_path_layout.addWidget(QLabel(":"))
        self.watermark_path_edit = DragDropLineEdit()
        self.watermark_path_edit.setPlaceholderText("选择水印图片（可拖拽文件到这里）")
        watermark_path_btn = QPushButton("浏览")
        watermark_path_btn.clicked.connect(
            lambda: self.select_file(self.watermark_path_edit, "图片文件 (*.png *.jpg *.webp)"))
        watermark_path_layout.addWidget(self.watermark_path_edit)
        watermark_path_layout.addWidget(watermark_path_btn)
        watermark_path_layout.addStretch()
        image_layout.addLayout(watermark_path_layout)

        img_size_opacity_layout = QHBoxLayout()
        img_size_opacity_layout.setSpacing(16)

        img_size_layout = QHBoxLayout()
        img_size_layout.addWidget(QLabel("水印尺寸"))
        img_size_layout.addWidget(QLabel(":"))
        self.watermark_img_size_spin = QSpinBox()
        self.watermark_img_size_spin.setRange(10, 500)
        self.watermark_img_size_spin.setValue(50)
        img_size_layout.addWidget(self.watermark_img_size_spin)
        img_size_opacity_layout.addLayout(img_size_layout)

        img_opacity_layout = QHBoxLayout()
        img_opacity_layout.addWidget(QLabel("透明度"))
        img_opacity_layout.addWidget(QLabel(":"))
        self.watermark_img_opacity_spin = QSpinBox()
        self.watermark_img_opacity_spin.setRange(0, 255)
        self.watermark_img_opacity_spin.setValue(128)
        img_opacity_layout.addWidget(self.watermark_img_opacity_spin)
        img_size_opacity_layout.addLayout(img_opacity_layout)
        img_size_opacity_layout.addStretch()
        image_layout.addLayout(img_size_opacity_layout)

        layout.addWidget(self.image_watermark_group)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(16)
        self.watermark_run_btn = QPushButton("应用")
        self.watermark_run_btn.clicked.connect(self.run_watermark)
        action_layout.addWidget(self.watermark_run_btn)
        action_layout.addStretch()
        layout.addLayout(action_layout)

        progress_group = QGroupBox("进度")
        progress_layout = QHBoxLayout(progress_group)
        self.watermark_progress_bar = QProgressBar()
        self.watermark_progress_bar.setRange(0, 100)
        self.watermark_progress_bar.setValue(0)
        progress_layout.addWidget(self.watermark_progress_bar)
        layout.addWidget(progress_group)

        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(log_group)
        self.watermark_log_edit = QTextEdit()
        self.watermark_log_edit.setReadOnly(True)
        self.watermark_log_edit.setMinimumHeight(150)
        log_layout.addWidget(self.watermark_log_edit)
        layout.addWidget(log_group)

    def init_modify_time_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "批量修改文件时间")

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        dir_group = QGroupBox("目标目录")
        dir_layout = QHBoxLayout(dir_group)
        dir_layout.setSpacing(12)
        self.modify_time_dir_edit = DragDropLineEdit()
        self.modify_time_dir_edit.setPlaceholderText("选择目录或文件（支持批量拖拽多个文件）")
        self.modify_time_dir_edit.setMinimumHeight(40)
        dir_btn = QPushButton("浏览")
        dir_btn.clicked.connect(lambda: self.select_dir(self.modify_time_dir_edit))
        dir_layout.addWidget(self.modify_time_dir_edit)
        dir_layout.addWidget(dir_btn)
        layout.addWidget(dir_group)

        time_group = QGroupBox("时间参数")
        time_layout = QVBoxLayout(time_group)
        time_layout.setSpacing(16)

        time_layout1 = QHBoxLayout()
        time_layout1.setSpacing(12)
        time_layout1.addWidget(QLabel("目标时间"))
        time_layout1.addWidget(QLabel(":"))
        self.modify_time_datetime = QDateTimeEdit()
        self.modify_time_datetime.setDateTime(QDateTime.currentDateTime())
        self.modify_time_datetime.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        time_layout1.addWidget(self.modify_time_datetime)
        time_layout1.addStretch()
        time_layout.addLayout(time_layout1)

        time_layout2 = QHBoxLayout()
        time_layout2.setSpacing(12)
        time_layout2.addWidget(QLabel("修改类型"))
        time_layout2.addWidget(QLabel(":"))
        self.modify_time_type_combo = QComboBox()
        self.modify_time_type_combo.addItems(["创建时间和修改时间", "仅创建时间", "仅修改时间"])
        time_layout2.addWidget(self.modify_time_type_combo)
        time_layout2.addStretch()
        time_layout.addLayout(time_layout2)

        layout.addWidget(time_group)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(16)
        self.modify_time_run_btn = QPushButton("应用")
        self.modify_time_run_btn.clicked.connect(self.run_modify_time)
        action_layout.addWidget(self.modify_time_run_btn)
        action_layout.addStretch()
        layout.addLayout(action_layout)

        progress_group = QGroupBox("进度")
        progress_layout = QHBoxLayout(progress_group)
        self.modify_time_progress_bar = QProgressBar()
        self.modify_time_progress_bar.setRange(0, 100)
        self.modify_time_progress_bar.setValue(0)
        progress_layout.addWidget(self.modify_time_progress_bar)
        layout.addWidget(progress_group)

        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(log_group)
        self.modify_time_log_edit = QTextEdit()
        self.modify_time_log_edit.setReadOnly(True)
        self.modify_time_log_edit.setMinimumHeight(150)
        log_layout.addWidget(self.modify_time_log_edit)
        layout.addWidget(log_group)

    def init_extract_exif_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "提取图片EXIF信息")

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        dir_group = QGroupBox("图片目录")
        dir_layout = QHBoxLayout(dir_group)
        dir_layout.setSpacing(12)
        self.extract_exif_dir_edit = DragDropLineEdit()
        self.extract_exif_dir_edit.setPlaceholderText("选择目录或图片（支持批量拖拽多个文件）")
        self.extract_exif_dir_edit.setMinimumHeight(40)
        dir_btn = QPushButton("浏览")
        dir_btn.clicked.connect(lambda: self.select_dir(self.extract_exif_dir_edit))
        dir_layout.addWidget(self.extract_exif_dir_edit)
        dir_layout.addWidget(dir_btn)
        layout.addWidget(dir_group)

        output_group = QGroupBox("输出设置")
        output_layout = QHBoxLayout(output_group)
        output_layout.setSpacing(12)
        output_layout.addWidget(QLabel("CSV保存路径"))
        output_layout.addWidget(QLabel(":"))
        self.extract_exif_output_edit = QLineEdit()
        self.extract_exif_output_edit.setPlaceholderText("默认：目录名_exif.csv")
        output_btn = QPushButton("浏览")
        output_btn.clicked.connect(lambda: self.select_save_file(self.extract_exif_output_edit, "CSV文件 (*.csv)"))
        output_layout.addWidget(self.extract_exif_output_edit)
        output_layout.addWidget(output_btn)
        output_layout.addStretch()
        layout.addWidget(output_group)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(16)
        self.extract_exif_run_btn = QPushButton("应用")
        self.extract_exif_run_btn.clicked.connect(self.run_extract_exif)
        action_layout.addWidget(self.extract_exif_run_btn)
        action_layout.addStretch()
        layout.addLayout(action_layout)

        progress_group = QGroupBox("进度")
        progress_layout = QHBoxLayout(progress_group)
        self.extract_exif_progress_bar = QProgressBar()
        self.extract_exif_progress_bar.setRange(0, 100)
        self.extract_exif_progress_bar.setValue(0)
        progress_layout.addWidget(self.extract_exif_progress_bar)
        layout.addWidget(progress_group)

        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(log_group)
        self.extract_exif_log_edit = QTextEdit()
        self.extract_exif_log_edit.setReadOnly(True)
        self.extract_exif_log_edit.setMinimumHeight(150)
        log_layout.addWidget(self.extract_exif_log_edit)
        layout.addWidget(log_group)

    def init_copy_move_tab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "批量复制/移动文件")

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        src_group = QGroupBox("源目录")
        src_layout = QHBoxLayout(src_group)
        src_layout.setSpacing(12)
        self.copy_move_src_edit = DragDropLineEdit()
        self.copy_move_src_edit.setPlaceholderText("选择目录或文件（支持批量拖拽多个文件）")
        self.copy_move_src_edit.setMinimumHeight(40)
        src_btn = QPushButton("浏览")
        src_btn.clicked.connect(lambda: self.select_dir(self.copy_move_src_edit))
        src_layout.addWidget(self.copy_move_src_edit)
        src_layout.addWidget(src_btn)
        layout.addWidget(src_group)

        dest_group = QGroupBox("目标目录")
        dest_layout = QHBoxLayout(dest_group)
        dest_layout.setSpacing(12)
        self.copy_move_dest_edit = DragDropLineEdit()
        self.copy_move_dest_edit.setPlaceholderText("选择目标目录（可拖拽文件夹/文件到这里）")
        self.copy_move_dest_edit.setMinimumHeight(40)
        dest_btn = QPushButton("浏览")
        dest_btn.clicked.connect(lambda: self.select_dir(self.copy_move_dest_edit))
        dest_layout.addWidget(self.copy_move_dest_edit)
        dest_layout.addWidget(dest_btn)
        layout.addWidget(dest_group)

        param_group = QGroupBox("操作参数")
        param_layout = QVBoxLayout(param_group)
        param_layout.setSpacing(16)

        type_layout = QHBoxLayout()
        type_layout.setSpacing(12)
        type_layout.addWidget(QLabel("操作类型"))
        type_layout.addWidget(QLabel(":"))
        self.copy_move_mode_combo = QComboBox()
        self.copy_move_mode_combo.addItems(["复制", "移动"])
        type_layout.addWidget(self.copy_move_mode_combo)
        type_layout.addStretch()
        param_layout.addLayout(type_layout)

        exclude_layout = QHBoxLayout()
        exclude_layout.setSpacing(12)
        exclude_layout.addWidget(QLabel("排除扩展名"))
        exclude_layout.addWidget(QLabel(":"))
        self.copy_move_exclude_edit = QLineEdit()
        self.copy_move_exclude_edit.setPlaceholderText("例如：zip,log,tmp")
        exclude_layout.addWidget(self.copy_move_exclude_edit)
        exclude_layout.addStretch()
        param_layout.addLayout(exclude_layout)

        layout.addWidget(param_group)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(16)
        self.copy_move_run_btn = QPushButton("应用")
        self.copy_move_run_btn.clicked.connect(self.run_copy_move)
        action_layout.addWidget(self.copy_move_run_btn)
        action_layout.addStretch()
        layout.addLayout(action_layout)

        progress_group = QGroupBox("进度")
        progress_layout = QHBoxLayout(progress_group)
        self.copy_move_progress_bar = QProgressBar()
        self.copy_move_progress_bar.setRange(0, 100)
        self.copy_move_progress_bar.setValue(0)
        progress_layout.addWidget(self.copy_move_progress_bar)
        layout.addWidget(progress_group)

        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(log_group)
        self.copy_move_log_edit = QTextEdit()
        self.copy_move_log_edit.setReadOnly(True)
        self.copy_move_log_edit.setMinimumHeight(150)
        log_layout.addWidget(self.copy_move_log_edit)
        layout.addWidget(log_group)

    def select_dir(self, line_edit):
        """选择文件或文件夹"""
        from PyQt5.QtWidgets import QMessageBox
        # 使用MessageBox让用户选择
        reply = QMessageBox.question(
            self,
            "选择类型",
            "请选择要选择的类型：\n\n点击 '是' 选择文件夹\n点击 '否' 选择文件",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            # 选择文件夹
            dir_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
            if dir_path:
                line_edit.setText(dir_path)
                if hasattr(line_edit, 'on_files_changed') and line_edit.on_files_changed:
                    line_edit.on_files_changed()
        else:
            # 选择文件
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "选择文件",
                "",
                "所有文件 (*.*)"
            )
            if file_path:
                line_edit.setText(file_path)
                if hasattr(line_edit, 'on_files_changed') and line_edit.on_files_changed:
                    line_edit.on_files_changed()

    def select_file(self, line_edit, filter_str):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", filter_str)
        if file_path:
            line_edit.setText(file_path)
            if hasattr(line_edit, 'on_files_changed') and line_edit.on_files_changed:
                line_edit.on_files_changed()
                
    def toggle_auto_number(self):
        """切换是否显示自动编号设置"""
        self.auto_number_group.setVisible(self.rename_use_auto_number.isChecked())

    def update_rename_file_settings(self):
        """当文件选择变化时，动态更新单个文件设置框"""
        dir_path = self.rename_dir_edit.text().strip()
        if not dir_path:
            return
            
        # 清空现有设置框
        for i in reversed(range(self.rename_files_layout.count())):
            widget = self.rename_files_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # 解析所有文件
        file_list = []
        file_separator = "|||"
        if file_separator in dir_path:
            paths = dir_path.split(file_separator)
            for path in paths:
                path = path.strip()
                if path:
                    p = Path(path)
                    if p.is_file():
                        file_list.append(p)
                    elif p.is_dir():
                        file_list.extend([f for f in p.glob("*") if f.is_file()])
        else:
            p = Path(dir_path)
            if p.is_file():
                file_list.append(p)
            elif p.is_dir():
                file_list = [f for f in p.glob("*") if f.is_file()]
        
        # 为每个文件生成设置框
        self.rename_file_settings = []
        for file_path in file_list:
            setting_group = QGroupBox(file_path.name)
            setting_layout = QHBoxLayout(setting_group)
            setting_layout.setSpacing(12)
            
            # 复选框 - 是否处理此文件
            checkbox = QCheckBox("处理")
            checkbox.setChecked(True)
            setting_layout.addWidget(checkbox)
            
            # 原始文件名显示
            original_label = QLabel(f"原名：{file_path.name}")
            original_label.setStyleSheet("color: #666; font-size: 11px;")
            setting_layout.addWidget(original_label)
            
            setting_layout.addStretch()
            
            # 自定义前缀
            custom_prefix_edit = QLineEdit()
            custom_prefix_edit.setPlaceholderText("自定义前缀")
            custom_prefix_edit.setMaximumWidth(120)
            setting_layout.addWidget(QLabel("前缀"))
            setting_layout.addWidget(custom_prefix_edit)
            
            # 自定义后缀
            custom_suffix_edit = QLineEdit()
            custom_suffix_edit.setPlaceholderText("自定义后缀")
            custom_suffix_edit.setMaximumWidth(120)
            setting_layout.addWidget(QLabel("后缀"))
            setting_layout.addWidget(custom_suffix_edit)
            
            # 自定义新名称
            custom_name_edit = QLineEdit()
            custom_name_edit.setPlaceholderText("自定义新文件名")
            custom_name_edit.setMinimumWidth(200)
            setting_layout.addWidget(QLabel("重命名"))
            setting_layout.addWidget(custom_name_edit)
            
            self.rename_file_settings.append({
                'file_path': file_path,
                'checkbox': checkbox,
                'custom_prefix': custom_prefix_edit,
                'custom_suffix': custom_suffix_edit,
                'custom_name': custom_name_edit
            })
            
            self.rename_files_layout.addWidget(setting_group)

    def select_save_file(self, line_edit, filter_str):
        file_path, _ = QFileDialog.getSaveFileName(self, "选择保存位置", "", filter_str)
        if file_path:
            line_edit.setText(file_path)

    def switch_watermark_type(self):
        if "文字" in self.watermark_type_combo.currentText():
            self.text_watermark_group.setVisible(True)
            self.image_watermark_group.setVisible(False)
        else:
            self.text_watermark_group.setVisible(False)
            self.image_watermark_group.setVisible(True)

    def clear_log(self, log_edit):
        log_edit.clear()

    def append_log(self, log_edit, msg):
        log_edit.append(msg)
        log_edit.moveCursor(log_edit.textCursor().End)

    def run_rename(self):
        dir_path = self.rename_dir_edit.text().strip()
        if not dir_path:
            QMessageBox.warning(self, "警告", "请选择文件或目录！")
            return

        self.clear_log(self.rename_log_edit)
        self.rename_run_btn.setEnabled(False)
        
        # 如果有单个文件设置，逐个处理
        if hasattr(self, 'rename_file_settings') and self.rename_file_settings:
            # 获取整体设置
            global_prefix = self.rename_prefix_edit.text().strip()
            global_suffix = self.rename_suffix_edit.text().strip()
            use_auto_number = self.rename_use_auto_number.isChecked()
            
            # 自动编号设置
            name_base = self.rename_name_base_edit.text().strip()
            start_num = self.rename_start_spin.value()
            digit_count = self.rename_digit_spin.value()
            
            total_files = len(self.rename_file_settings)
            processed = 0
            renamed = 0
            skipped = 0
            current_num = start_num
            
            self.append_log(self.rename_log_edit, "📝 开始处理...")
            
            for setting in self.rename_file_settings:
                if not setting['checkbox'].isChecked():
                    skipped += 1
                    processed += 1
                    self.append_log(self.rename_log_edit, f"⚠️ 跳过：{setting['file_path'].name}")
                    continue
                
                file_path = setting['file_path']
                old_name = file_path.name
                name, ext = os.path.splitext(old_name)
                new_main_name = name
                
                # 优先使用单个文件设置
                custom_name = setting['custom_name'].text().strip()
                if custom_name:
                    new_main_name = custom_name
                else:
                    if use_auto_number:
                        # 自动编号模式
                        new_main_name = f"{name_base}{str(current_num).zfill(digit_count)}"
                        current_num += 1
                    
                    # 应用全局前缀后缀
                    final_prefix = setting['custom_prefix'].text().strip() or global_prefix
                    final_suffix = setting['custom_suffix'].text().strip() or global_suffix
                    
                    if final_prefix:
                        new_main_name = final_prefix + new_main_name
                    if final_suffix:
                        new_main_name = new_main_name + final_suffix
                
                new_name = new_main_name + ext
                if new_name == old_name:
                    skipped += 1
                    processed += 1
                    self.append_log(self.rename_log_edit, f"⚠️ 跳过（无变化）：{old_name}")
                    continue
                
                new_path = file_path.parent / new_name
                if new_path.exists():
                    skipped += 1
                    processed += 1
                    self.append_log(self.rename_log_edit, f"⚠️ 跳过（已存在）：{old_name} → {new_name}")
                    continue
                
                try:
                    file_path.rename(new_path)
                    renamed += 1
                    self.append_log(self.rename_log_edit, f"✅ 成功：{old_name} → {new_name}")
                except Exception as e:
                    skipped += 1
                    self.append_log(self.rename_log_edit, f"❌ 失败：{old_name} - {str(e)}")
                
                processed += 1
            
            self.append_log(self.rename_log_edit, f"\n✅ 完成！共处理 {total_files} 个，成功 {renamed} 个，跳过 {skipped} 个")
            self.task_finish(True, self.rename_run_btn)
        else:
            # 使用原始的批量处理
            params = {
                "dir": dir_path,
                "prefix": self.rename_prefix_edit.text().strip(),
                "suffix": self.rename_suffix_edit.text().strip(),
                "find_str": "",
                "replace_str": ""
            }

            self.rename_thread = WorkerThread("rename", params)
            self.rename_thread.log_signal.connect(lambda msg: self.append_log(self.rename_log_edit, msg))
            self.rename_thread.finish_signal.connect(lambda res: self.task_finish(res, self.rename_run_btn))
            self.rename_thread.start()

    def run_convert_img(self):
        dir_path = self.convert_dir_edit.text().strip()
        if not dir_path or not Path(dir_path).exists():
            QMessageBox.warning(self, "警告", "请选择有效的图片目录！")
            return

        self.clear_log(self.convert_log_edit)
        self.convert_run_btn.setEnabled(False)

        params = {
            "dir": dir_path,
            "to_format": self.convert_format_combo.currentText()
        }

        self.convert_thread = WorkerThread("convert_img", params)
        self.convert_thread.log_signal.connect(lambda msg: self.append_log(self.convert_log_edit, msg))
        self.convert_thread.progress_signal.connect(lambda val: self.convert_progress_bar.setValue(val))
        self.convert_thread.finish_signal.connect(lambda res: self.task_finish(res, self.convert_run_btn))
        self.convert_thread.start()

    def run_compress(self):
        dir_path = self.compress_dir_edit.text().strip()
        if not dir_path or not Path(dir_path).exists():
            QMessageBox.warning(self, "警告", "请选择有效的目标目录！")
            return

        self.clear_log(self.compress_log_edit)
        self.compress_run_btn.setEnabled(False)

        params = {
            "dir": dir_path,
            "output": self.compress_output_edit.text().strip(),
            "exclude": self.compress_exclude_edit.text().strip()
        }

        self.compress_thread = WorkerThread("compress", params)
        self.compress_thread.log_signal.connect(lambda msg: self.append_log(self.compress_log_edit, msg))
        self.compress_thread.progress_signal.connect(lambda val: self.compress_progress_bar.setValue(val))
        self.compress_thread.finish_signal.connect(lambda res: self.task_finish(res, self.compress_run_btn))
        self.compress_thread.start()

    def run_classify(self):
        dir_path = self.classify_dir_edit.text().strip()
        if not dir_path or not Path(dir_path).exists():
            QMessageBox.warning(self, "警告", "请选择有效的目标目录！")
            return

        self.clear_log(self.classify_log_edit)
        self.classify_run_btn.setEnabled(False)

        mode_text = self.classify_mode_combo.currentText()
        mode = "ext" if "扩展名" in mode_text else "date"

        params = {
            "dir": dir_path,
            "mode": mode
        }

        self.classify_thread = WorkerThread("classify", params)
        self.classify_thread.log_signal.connect(lambda msg: self.append_log(self.classify_log_edit, msg))
        self.classify_thread.progress_signal.connect(lambda val: self.classify_progress_bar.setValue(val))
        self.classify_thread.finish_signal.connect(lambda res: self.task_finish(res, self.classify_run_btn))
        self.classify_thread.start()

    def run_watermark(self):
        dir_path = self.watermark_dir_edit.text().strip()
        if not dir_path or not Path(dir_path).exists():
            QMessageBox.warning(self, "警告", "请选择有效的图片目录！")
            return

        type_text = self.watermark_type_combo.currentText()
        if "文字" in type_text and not self.watermark_content_edit.text().strip():
            QMessageBox.warning(self, "警告", "请输入文字水印内容！")
            return
        if "图片" in type_text and not self.watermark_path_edit.text().strip():
            QMessageBox.warning(self, "警告", "请选择水印图片！")
            return

        self.clear_log(self.watermark_log_edit)
        self.watermark_run_btn.setEnabled(False)

        params = {
            "dir": dir_path,
            "type": "text" if "文字" in type_text else "image",
            "content": self.watermark_content_edit.text().strip(),
            "font": self.watermark_font_edit.text().strip(),
            "size": self.watermark_size_spin.value() if "文字" in type_text else self.watermark_img_size_spin.value(),
            "color": self.watermark_color_edit.text().strip(),
            "opacity": self.watermark_opacity_spin.value() if "文字" in type_text else self.watermark_img_opacity_spin.value(),
            "watermark_path": self.watermark_path_edit.text().strip()
        }

        self.watermark_thread = WorkerThread("watermark", params)
        self.watermark_thread.log_signal.connect(lambda msg: self.append_log(self.watermark_log_edit, msg))
        self.watermark_thread.progress_signal.connect(lambda val: self.watermark_progress_bar.setValue(val))
        self.watermark_thread.finish_signal.connect(lambda res: self.task_finish(res, self.watermark_run_btn))
        self.watermark_thread.start()

    def run_modify_time(self):
        dir_path = self.modify_time_dir_edit.text().strip()
        if not dir_path or not Path(dir_path).exists():
            QMessageBox.warning(self, "警告", "请选择有效的目标目录！")
            return

        self.clear_log(self.modify_time_log_edit)
        self.modify_time_run_btn.setEnabled(False)

        target_time = self.modify_time_datetime.dateTime().toPyDateTime()
        time_type_text = self.modify_time_type_combo.currentText()
        if "创建时间和修改时间" in time_type_text:
            time_type = "both"
        elif "仅创建时间" in time_type_text:
            time_type = "create"
        else:
            time_type = "modify"

        params = {
            "dir": dir_path,
            "target_time": target_time,
            "time_type": time_type
        }

        self.modify_time_thread = WorkerThread("modify_time", params)
        self.modify_time_thread.log_signal.connect(lambda msg: self.append_log(self.modify_time_log_edit, msg))
        self.modify_time_thread.progress_signal.connect(lambda val: self.modify_time_progress_bar.setValue(val))
        self.modify_time_thread.finish_signal.connect(lambda res: self.task_finish(res, self.modify_time_run_btn))
        self.modify_time_thread.start()

    def run_extract_exif(self):
        dir_path = self.extract_exif_dir_edit.text().strip()
        if not dir_path or not Path(dir_path).exists():
            QMessageBox.warning(self, "警告", "请选择有效的图片目录！")
            return

        output_csv = self.extract_exif_output_edit.text().strip()
        if not output_csv:
            path_obj = Path(dir_path)
            if path_obj.is_file():
                output_csv = f"{path_obj.parent / path_obj.stem}_exif.csv"
            else:
                output_csv = f"{dir_path}_exif.csv"

        self.clear_log(self.extract_exif_log_edit)
        self.extract_exif_run_btn.setEnabled(False)

        params = {
            "dir": dir_path,
            "output_csv": output_csv
        }

        self.extract_exif_thread = WorkerThread("extract_exif", params)
        self.extract_exif_thread.log_signal.connect(lambda msg: self.append_log(self.extract_exif_log_edit, msg))
        self.extract_exif_thread.progress_signal.connect(lambda val: self.extract_exif_progress_bar.setValue(val))
        self.extract_exif_thread.finish_signal.connect(lambda res: self.task_finish(res, self.extract_exif_run_btn))
        self.extract_exif_thread.start()

    def run_copy_move(self):
        src_dir = self.copy_move_src_edit.text().strip()
        dest_dir = self.copy_move_dest_edit.text().strip()
        if not src_dir or not Path(src_dir).exists():
            QMessageBox.warning(self, "警告", "请选择有效的源目录！")
            return
        if not dest_dir:
            QMessageBox.warning(self, "警告", "请选择有效的目标目录！")
            return

        self.clear_log(self.copy_move_log_edit)
        self.copy_move_run_btn.setEnabled(False)

        mode = "copy" if "复制" in self.copy_move_mode_combo.currentText() else "move"
        exclude = self.copy_move_exclude_edit.text().strip()

        params = {
            "dir": src_dir,
            "target_dir": dest_dir,
            "mode": mode,
            "exclude": exclude
        }

        self.copy_move_thread = WorkerThread("copy_move", params)
        self.copy_move_thread.log_signal.connect(lambda msg: self.append_log(self.copy_move_log_edit, msg))
        self.copy_move_thread.progress_signal.connect(lambda val: self.copy_move_progress_bar.setValue(val))
        self.copy_move_thread.finish_signal.connect(lambda res: self.task_finish(res, self.copy_move_run_btn))
        self.copy_move_thread.start()

    def task_finish(self, result, btn):
        btn.setEnabled(True)
        if result:
            QMessageBox.information(self, "成功", "任务执行完成！")
        else:
            QMessageBox.critical(self, "失败", "任务执行失败，请查看日志！")


def run():
    """主入口函数，供setup.py entry_points调用"""
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = FileToolMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
