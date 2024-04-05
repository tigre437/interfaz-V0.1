import cv2 as cv
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer
import datetime
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

class Camera:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            print("Unable to read camera feed")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv.flip(frame, 1)
            rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            if self.callback:
                self.callback(pixmap)

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            time = str(datetime.datetime.now().today()).replace(':', "_") + '.jpg'
            cv.imwrite(time, frame)

    def release_camera(self):
        self.cap.release()

    def set_callback(self, callback):
        self.callback = callback

    def update_camera_index(self, index):
        if self.cap.isOpened():
            self.cap.release()
        self.cap = cv.VideoCapture(index)

    def open_camera_settings(self):
        self.camera.open_settings()


class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Camera App')
        self.setGeometry(100, 100, 646, 530)
        self.setStyleSheet('background-color: #58F;')

        self.camera = Camera()
        self.camera.set_callback(self.update_label)

        self.label = QLabel(self)
        self.label.setGeometry(20, 20, 600, 400)
        self.label.setStyleSheet('background-color: red;')

        self.capture_button = QPushButton('Capture Image 📷', self)
        self.capture_button.setGeometry(50, 440, 200, 50)
        self.capture_button.setStyleSheet('background-color: green; color: white;')
        self.capture_button.clicked.connect(self.capture_image)

        self.exit_button = QPushButton('EXIT ❌', self)
        self.exit_button.setGeometry(350, 440, 200, 50)
        self.exit_button.setStyleSheet('background-color: red; color: white;')
        self.exit_button.clicked.connect(self.exit_window)

    def update_label(self, pixmap):
        self.label.setPixmap(pixmap)

    def capture_image(self):
        self.camera.capture_image()

    def exit_window(self):
        self.camera.release_camera()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec())