from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot, Qt
from PyQt6.QtGui import QPixmap, QImage, QTransform
import cv2
from interfazv1 import Ui_MainWindow
import serial.tools.list_ports
import numpy as np
from pygrabber.dshow_graph import FilterGraph


import time
import datetime

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.buttonBuscarArchivos.clicked.connect(self.filechooser)
        self.buttonConfiguracion.clicked.connect(self.openConfigCamera)
        self.buttonConectar.clicked.connect(self.conectarCamara)
        self.thread = VideoThread()

        self.fillCameras()
        self.list_cameras()

        self.comboBoxCamara.currentIndexChanged.connect(self.update_camera_index)
        self.buttonConfiguracion.clicked.connect(self.settings)
        

        self.display_width = self.width() // 2
        self.display_height = self.height() // 2

    def list_cameras(self):
        cameras = []
        for index in range(10):  
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap.isOpened():
                cameras.append(index)
                cap.release()
        
        return cameras
    

    def update_camera_index(self, index):
        if self.thread and self.thread.isRunning():
            self.thread.stop()  # Detener el hilo existente
            self.thread.finished.connect(self.thread.deleteLater)  # Eliminar el objeto del hilo después de que termine

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.set_camera_index(index)
        self.thread.start()




    def get_available_cameras(self) :

        devices = FilterGraph().get_input_devices()

        available_cameras = {}

        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name

        return available_cameras

    
    def fillCameras(self):
        available_cameras = self.get_available_cameras()
        for camera_index, camera_name in available_cameras.items():
            self.comboBoxCamara.addItem(camera_name)

    def conectarCamara(self):
        print(self.comboBoxCamara.currentIndex())

    def settings(self):
        self.thread.settings()
    
    def filechooser(self):
        # Abrir el diálogo de selección de archivos
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        
        # Se selecciona una carpeta y se muestra la ruta
        if file_dialog.exec():
            selected_folder = file_dialog.selectedFiles()
            self.txtArchivos.setText(selected_folder[0])

    def openConfigCamera(self):
        print("en proceso")


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Actualiza el QLabel con una nueva imagen de OpenCV"""
        qt_img = self.convert_cv_qt(cv_img)
        
        transform = QTransform()
        transform.rotate(90)
        qt_img = qt_img.transformed(transform)

        # Ajustar el tamaño del widget labelCamara
        self.labelCamara.setPixmap(qt_img)
        self.labelCamara.setFixedSize(qt_img.size())


    def convert_cv_qt(self, cv_img):
        """Convierte una imagen de OpenCV a QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)



        
    def get_status(self):
        self.datetime.setText(f'{datetime.datetime.now():%m/%d/%Y %H:%M:%S}')



class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.cap = None
        self._run_flag = True

    def run(self):
        # Captura desde la cámara web
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        while self._run_flag:
            ret, cv_img = self.cap.read()
            if ret:
                # Imprimir las dimensiones del fotograma
                height, width, _ = cv_img.shape
                #########print("Dimensiones del fotograma:", height, "x", width)

                # Emitir la señal con el fotograma capturado
                self.change_pixmap_signal.emit(cv_img)
        # Apagar el sistema de captura
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
            #ABRA QUE MIRAR DE CAMBIAR ESTA RUTA
            cv2.imwrite(r'C:\Users\david\Desktop\interfaz-V0.1\imagenes-prueba', cv_img)

    def set_camera_index(self, index):
        """Establece el índice del dispositivo de captura"""
        self.camera_index = index


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()