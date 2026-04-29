from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QTableWidget, 
                             QTableWidgetItem, QLabel, QHeaderView, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor
from data_engine import DataEngine

class MainWindow(QMainWindow):
    def __init__(self, mode): # 必须接收 mode 参数
        super().__init__()
        self.mode = mode
        self.engine = DataEngine()
        
        # 1. 隐藏原生边框 & 设置背景透明
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.resize(900, 600)
        self.init_ui()
        
        # 用于记录鼠标位置实现拖动
        self._old_pos = None

    def init_ui(self):
        # 2. 创建一个主容器 QFrame，用于承载圆角和背景
        self.main_container = QFrame()
        self.main_container.setObjectName("MainContainer")
        self.setCentralWidget(self.main_container)
        
        # 设置圆角阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.main_container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.main_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- 3. 自定义标题栏 ---
        self.title_bar = QWidget()
        self.title_bar.setObjectName("TitleBar")
        self.title_bar.setFixedHeight(60)
        
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 0, 20, 0)
        
        self.btn_import = QPushButton("重新导入")
        self.btn_import.setObjectName("PrimaryButton")
        self.btn_import.clicked.connect(self.handle_import)
        
        # 最小化 & 关闭按钮
        self.btn_min = QPushButton("")
        self.btn_close = QPushButton("")
        
        # 设置对象名称以便在QSS中引用
        self.btn_min.setObjectName("MinButton")
        self.btn_close.setObjectName("CloseButton")
        
        # 设置固定大小为圆形 (宽=高)
        self.btn_min.setFixedSize(14, 14)
        self.btn_close.setFixedSize(14, 14)
        
        # 可选：设置字体大小以适配圆形按钮
        font = self.btn_min.font()
        font.setPointSize(12)
        self.btn_min.setFont(font)
        self.btn_close.setFont(font)

        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_close.clicked.connect(self.close)

        title_layout.addWidget(self.btn_import)

        title_layout.addStretch()

        title_layout.setSpacing(15)
        title_layout.addWidget(self.btn_min)
        title_layout.addWidget(self.btn_close)
        
        layout.addWidget(self.title_bar)

        # --- 4. 内容区域 ---
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # 操作栏
        tool_layout = QHBoxLayout()

        
        self.label_stat = QLabel("等待数据导入...")
        self.label_stat.setObjectName("StatLabel")
        
        tool_layout.addSpacing(20)
        tool_layout.addWidget(self.label_stat)
        tool_layout.addStretch()
        content_layout.addLayout(tool_layout)

        # 表格美化
        self.table = QTableWidget()
        self.table.setFrameShape(QFrame.Shape.NoFrame)
        self.table.setShowGrid(False);
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # 【新增】禁止编辑表格单元格
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # 可选：如果不希望用户选中单元格，也可以取消选择模式
        # self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        content_layout.addWidget(self.table)
        layout.addWidget(content_area)

    # --- 窗口拖动逻辑 ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._old_pos:
            delta = event.globalPosition().toPoint() - self._old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._old_pos = None

    # --- 业务逻辑复用 ---
    def handle_import(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择", "", "Excel Files (*.xlsx)")
        if path:
            try:
                data = self.engine.process_wechat_bill(path)
                self.refresh_table(data)
                stats = self.engine.get_summary()
                self.label_stat.setText(f"总支出: ¥{stats['支出']:.2f} | 总收入: ¥{stats['收入']:.2f}")
            except Exception as e:
                self.label_stat.setText(f"错误: {e}")

    def refresh_table(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        for i in range(len(df)):
            for j in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                if df.columns[j] == '金额(元)':
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(i, j, item)