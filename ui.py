"""UI components for the hand gesture control application."""
import sys
import cv2
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QColor

from config import CAM_INDEX, CAP_WIDTH, CAP_HEIGHT, CAP_FPS, DISPLAY_WIDTH, DISPLAY_HEIGHT
from logic_core import LogicCore, CyberRender


class VideoThread(QThread):
    """Background thread for video capture and processing."""
    
    change_pixmap_signal = pyqtSignal(QImage)
    status_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, CAP_FPS)

        renderer = CyberRender()
        core = LogicCore()

        self.status_signal.emit("RABOTAI // POZALUSTA")

        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = core.process(frame, renderer)

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                qt_img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
                p = qt_img.scaled(DISPLAY_WIDTH, DISPLAY_HEIGHT, Qt.AspectRatioMode.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)
            else:
                break
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class MainWindow(QMainWindow):
    """Main application window with frameless design."""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(1000, 650)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.bg = QFrame()
        self.bg.setStyleSheet("background: #0b0b10; border: 2px solid #00ffaa; border-radius: 10px;")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 255, 170, 80))
        self.bg.setGraphicsEffect(shadow)

        self.inner = QVBoxLayout(self.bg)

        self.title_bar = QHBoxLayout()
        self.lbl_title = QLabel("GLAZA_GRISHI")
        self.lbl_title.setStyleSheet("color: #00ffaa; font-family: Consolas; font-weight: bold;")
        self.btn_minimize = QPushButton("⊟")
        self.btn_minimize.setFixedSize(30, 30)
        self.btn_minimize.clicked.connect(self.showMinimized)
        self.btn_minimize.setStyleSheet(
            "QPushButton {"
            "    background: transparent;"
            "    color: #6B7280;"
            "    border: none;"
            "    border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "    background: #D1D5DB;"
            "}"
        )
        self.btn_exit = QPushButton("X")
        self.btn_exit.setFixedSize(30, 30)
        self.btn_exit.clicked.connect(self.close)
        self.btn_exit.setStyleSheet("background: transparent; color: red; border: 1px solid red; border-radius: 5px;")

        self.title_bar.addWidget(self.lbl_title)
        self.title_bar.addStretch()
        self.title_bar.addWidget(self.btn_minimize)
        self.title_bar.addWidget(self.btn_exit)
        self.inner.addLayout(self.title_bar)

        # Видео
        self.display = QLabel()
        self.display.setFixedSize(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.display.setStyleSheet("background: #000; border: 1px solid #222;")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inner.addWidget(self.display, alignment=Qt.AlignmentFlag.AlignCenter)

        # Статус
        self.lbl_stat = QLabel("INIT")
        self.lbl_stat.setStyleSheet("color: #aaa; font-family: Consolas;")
        self.inner.addWidget(self.lbl_stat)

        self.layout.addWidget(self.bg)

        # Логика окна
        self.old_pos = None

        # Запуск камеры
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(lambda x: self.display.setPixmap(QPixmap.fromImage(x)))
        self.thread.status_signal.connect(self.lbl_stat.setText)
        self.thread.start()

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, e):
        self.old_pos = None

    def closeEvent(self, e):
        self.thread.stop()


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
