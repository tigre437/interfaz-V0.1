from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap
import sys
import cv2
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np




class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.cap = None
        self._run_flag = True

    def run(self):
        # capture from web cam
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self._run_flag:
            ret, cv_img = self.cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        self.cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def settings(self):
        self.cap.set(cv2.CAP_PROP_SETTINGS, 1)

    def save(self):
        ret, cv_img = self.cap.read()
        if ret:
            cv2.imwrite(r'G:\Mi unidad\code\qt\image.jpg', cv_img)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640/2
        self.display_height = 480/2
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create buttons
        self.settingsBTN = QPushButton("settings")
        self.saveBTN = QPushButton("save")
        
        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.settingsBTN)
        vbox.addWidget(self.saveBTN)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # connect the button to clickebutton function
        self.settingsBTN.clicked.connect(self.settings)
        self.saveBTN.clicked.connect(self.save)

        # start the thread
        self.thread.start()

    def settings(self):
        self.thread.settings()

    def save(self):
        self.thread.save()



    def closeEvent(self, event):
        self.thread.stop()
        event.accept()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec())