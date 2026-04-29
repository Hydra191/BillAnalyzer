import sys
from PyQt6.QtWidgets import QApplication
from mainwindow import MainWindow
from modewindow import ModeWindow
QSS = """
    #MainContainer {
        background-color: #1e1e1e;   /* 主背景深灰 */   
    }
    
    #TitleBar {
        background-color: #252526;   /* 标题栏略深于背景 */
        border-top-left-radius: 15px;
        border-top-right-radius: 15px;
    }
    
    #TitleLabel {
        color: #cccccc;
        font-weight: bold;
        font-size: 13px;
    }
    
    #CloseButton, #MinButton {
        background-color: transparent;
        color: #cccccc;
        border: none;
        font-size: 16px;
        width: 35px;
    }
    
    #CloseButton:hover {
        background-color: #e81123;   /* 典型的关闭红 */
        color: white;
    }

    #MinButton:hover {
        background-color: #3f3f3f;
    }
    
    #PrimaryButton {
        background-color: #22ffffff;   /* 经典深蓝色 */
        color: white;
        border-radius: 15px;
        padding: 8px 15px;
        font-family: "Segoe UI", "Microsoft YaHei";
    }
    
    #PrimaryButton:hover {
        background-color: #21B4FD;
    }
    
    #StatLabel {
        color: #d4d4d4;
        font-size: 14px;
    }
    
    /* 表格区域美化 */
    QTableWidget {
        background-color: #252526;
        color: #d4d4d4;
        gridline-color: #333333;
        border: none;
        border-radius: 8px;
        selection-background-color: #264f78; /* 选中行颜色 */
        selection-color: white;
    }
    
    QHeaderView::section {
        background-color: #333333;
        color: #cccccc;
        padding: 8px;
        border: none;
        font-weight: bold;
    }

    /* 滚动条美化 */
    QScrollBar:vertical {
        background: #1e1e1e;
        width: 10px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #424242;
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""
class Controller:
    def __init__(self):
        self.welcome = ModeWindow()
        self.main_window = None
        # 绑定信号
        self.welcome.mode_selected.connect(self.show_main)

    def show_welcome(self):
        self.welcome.show()

    def show_main(self, mode):
        self.welcome.close()
        # 实例化主窗口并传入模式
        self.main_window = MainWindow(mode=mode)
        self.main_window.show()
        
        # 自动触发一次文件选择
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(300, self.main_window.handle_import)

if __name__ == "__main__":

    
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    
    # 使用控制器管理窗口切换
    controller = Controller()
    controller.show_welcome()
    sys.exit(app.exec())