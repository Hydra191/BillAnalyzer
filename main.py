import sys
from PyQt6.QtWidgets import QApplication
from mainwindow import MainWindow
from modewindow import ModeWindow
QSS = """
    #MainContainer {
        background-color: #1E1E1E;   /* 主背景深灰 */   
    }

    #MinButton {
        background-color: #32CD32;

        border: none;
        border-radius: 7px; /* 半径是宽度30的一半 */
        font-weight: bold;
    }
    #CloseButton {
        background-color: #FF4040;

        border: none;
        border-radius: 7px; /* 半径是宽度30的一半 */
        font-weight: bold;
    }
    

    #TitleBar {
        background-color: #16161C;   /* 标题栏略深于背景 */
        border-top-left-radius: 15px;
        border-top-right-radius: 15px;
    }
    
    #TitleLabel {
        color: #cccccc;
        font-weight: bold;
        font-size: 13px;
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
        background-color: #18191B;
        border: none;
        border-radius: 8px;
        selection-background-color: #264f78; /* 选中行颜色 */
        selection-color: white;
    }
    QTableCornerButton::section {
        background-color: #18191B; /* 与表头和表格背景保持一致 */
        border: none;
    }
    QHeaderView::section {
        background-color: #18191B;
        color: #cccccc;
        padding: 8px;
        border: none;
        font-weight: bold;
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