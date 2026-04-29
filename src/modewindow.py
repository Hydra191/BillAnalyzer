from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

class ModeWindow(QWidget):
    # 定义信号，用于通知 main.py 选择了哪个模式
    mode_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # 隐藏系统标题栏，设置背景透明
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setFixedSize(260, 260) # 紧凑型小窗
        self.init_ui()
        self._old_pos = None

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 主容器（背景、圆角）
        self.container = QFrame()
        self.container.setObjectName("ModeContainer")
        
        # 内部按钮布局
        c_layout = QVBoxLayout(self.container)
        c_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        c_layout.setSpacing(25)

        # 微信按钮

        self.btn_wechat = QPushButton("微信支付")
        self.btn_wechat.setObjectName("BtnWechat")
        self.btn_wechat.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_wechat.clicked.connect(lambda: self.mode_selected.emit("wechat"))
        self.btn_wechat.setFixedSize(220, 100)

        # 支付宝按钮

        self.btn_alipay = QPushButton("支付宝")
        self.btn_alipay.setObjectName("BtnAlipay")
        self.btn_alipay.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_alipay.clicked.connect(lambda: self.mode_selected.emit("alipay"))
        self.btn_alipay.setFixedSize(220, 100)

        c_layout.addWidget(self.btn_wechat)
        c_layout.addWidget(self.btn_alipay)

        layout.addWidget(self.container)

    # 允许拖动这个小窗
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