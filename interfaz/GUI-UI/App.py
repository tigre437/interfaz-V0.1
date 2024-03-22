from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot, Qt
from PyQt6.QtGui import QPixmap, QImage, QTransform
import cv2
from interfazv1 import Ui_MainWindow
import serial.tools.list_ports
import numpy as np
from pygrabber.dshow_graph import FilterGraph
import os


import time
import datetime

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.buttonBuscarArchivos.clicked.connect(self.filechooser)
        self.buttonConfiguracion.clicked.connect(self.openConfigCamera)
        self.thread = VideoThread()

        self.fillCameras()
        self.list_cameras()

        self.comboBoxCamara.currentIndexChanged.connect(self.update_camera_index)
        self.buttonConfiguracion.clicked.connect(self.settings)

        self.checkBoxHabilitarA.stateChanged.connect(self.cambiarPlacaA)
        self.checkBoxHabilitarB.stateChanged.connect(self.cambiarPlacaB)

        self.comboBoxFiltro.currentIndexChanged.connect(self.comprobar_opcion_seleccionada)
        

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

    def settings(self):
        self.thread.settings()
    

    def cambiarPlacaA(self):
        if self.checkBoxHabilitarA.isChecked():
            self.txtNombrePlacaA.setEnabled(True)
            self.txtVDropPlacaA.setEnabled(True)
            self.txtVWashPlacaA.setEnabled(True)
            self.txtFactorDilucPlacaA.setEnabled(True)
            self.txtFraccFiltroPlacaA.setEnabled(True)
            self.txtTasaMuestreoPlacaA.setEnabled(True)
            self.txtVelEnfriamientoPlacaA.setEnabled(True)
            self.txtObservPlacaA.setEnabled(True)
        else:
            self.txtNombrePlacaA.setEnabled(False)
            self.txtVDropPlacaA.setEnabled(False)
            self.txtVWashPlacaA.setEnabled(False)
            self.txtFactorDilucPlacaA.setEnabled(False)
            self.txtFraccFiltroPlacaA.setEnabled(False)
            self.txtTasaMuestreoPlacaA.setEnabled(False)
            self.txtVelEnfriamientoPlacaA.setEnabled(False)
            self.txtObservPlacaA.setEnabled(False)

    def cambiarPlacaB(self):
        if self.checkBoxHabilitarB.isChecked():
            self.txtNombrePlacaB.setEnabled(True)
            self.txtVDropPlacaB.setEnabled(True)
            self.txtVWashPlacaB.setEnabled(True)
            self.txtFactorDilucPlacaB.setEnabled(True)
            self.txtFraccFiltroPlacaB.setEnabled(True)
            self.txtTasaMuestreoPlacaB.setEnabled(True)
            self.txtVelEnfriamientoPlacaB.setEnabled(True)
            self.txtObservPlacaB.setEnabled(True)
        else:
            self.txtNombrePlacaB.setEnabled(False)
            self.txtVDropPlacaB.setEnabled(False)
            self.txtVWashPlacaB.setEnabled(False)
            self.txtFactorDilucPlacaB.setEnabled(False)
            self.txtFraccFiltroPlacaB.setEnabled(False)
            self.txtTasaMuestreoPlacaB.setEnabled(False)
            self.txtVelEnfriamientoPlacaB.setEnabled(False)
            self.txtObservPlacaB.setEnabled(False)

#Sistema de busqueda de carpetas SNS
    def buscar_carpetas_sns(self, directorio):
            # Obtener una lista de todas las carpetas dentro del directorio proporcionado
            carpetas = [nombre for nombre in os.listdir(directorio) if os.path.isdir(os.path.join(directorio, nombre))]
            
            # Filtrar las carpetas que comienzan por "SNS"
            carpetas_sns = [carpeta for carpeta in carpetas if carpeta.startswith("SNS")]

            return carpetas_sns
#Cargo todos los resultados de la busqueda de los filtros en el combobox de los filtros
    def filechooser(self):
        # Abrir el diálogo de selección de archivos
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        
        # Seleccionar una carpeta y mostrar la ruta
        if file_dialog.exec():
            selected_folder = file_dialog.selectedFiles()
            carpeta_seleccionada = selected_folder[0]
            self.txtArchivos.setText(carpeta_seleccionada)
            
            # Buscar todas las carpetas que comienzan por "SNS" dentro de la carpeta seleccionada
            carpetas_sns = self.buscar_carpetas_sns(carpeta_seleccionada)
            
            if carpetas_sns:
                # Limpiar el comboBox antes de agregar nuevas carpetas
                self.comboBoxFiltro.clear()
                self.comboBoxFiltro.addItem("Crear un filtro nuevo ...")
                
                # Agregar las carpetas encontradas al comboBox
                for carpeta in carpetas_sns:
                    self.comboBoxFiltro.addItem(carpeta)
            else:
                print("No se encontraron carpetas que empiecen por 'SNS' dentro de la carpeta seleccionada.")

    def comprobar_opcion_seleccionada(self, index):
        if index == 0:  # Si se selecciona la opción de crear una carpeta
            nombre_carpeta = self.obtener_nombre_carpeta()
            if nombre_carpeta:
                self.crear_carpeta(nombre_carpeta)

    def obtener_nombre_carpeta(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Nombre de la carpeta")
        
        etiqueta = QLabel("Ingrese el nombre de la carpeta:")
        campo_texto = QLineEdit()
        boton_aceptar = QPushButton("Aceptar")
        boton_cancelar = QPushButton("Cancelar")

        layout = QVBoxLayout()
        layout.addWidget(etiqueta)
        layout.addWidget(campo_texto)
        layout.addWidget(boton_aceptar)
        layout.addWidget(boton_cancelar)

        dialogo.setLayout(layout)

        def aceptar():
            nombre_carpeta = campo_texto.text()
            if nombre_carpeta:
                dialogo.accept()

        boton_aceptar.clicked.connect(aceptar)
        boton_cancelar.clicked.connect(dialogo.reject)

        if dialogo.exec() == QDialog.DialogCode.Accepted:
            return campo_texto.text()
        else:
            return None

    def crear_carpeta(self, nombre_carpeta):
        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now().strftime("%Y%m%d")
        nombre_carpeta_sns = f"SNS_{fecha_actual}_{nombre_carpeta}"
        
        # Obtener la ruta del directorio seleccionado por el usuario
        directorio_seleccionado = self.txtArchivos.text()
        
        # Comprobar si el directorio existe y crear la carpeta si es necesario
        if os.path.isdir(directorio_seleccionado):
            ruta_carpeta_sns = os.path.join(directorio_seleccionado, nombre_carpeta_sns)
            os.makedirs(ruta_carpeta_sns)
            print(f"Carpeta '{nombre_carpeta_sns}' creada exitosamente en '{directorio_seleccionado}'.")
            carpetas_sns = self.buscar_carpetas_sns(directorio_seleccionado)
            self.comboBoxFiltro.clear()
            self.comboBoxFiltro.addItem("Crear un filtro nuevo ...")
            
            # Agregar las carpetas encontradas al comboBox
            for carpeta in carpetas_sns:
                self.comboBoxFiltro.addItem(carpeta)
            self.comboBoxFiltro.setCurrentText(nombre_carpeta_sns)
        else:
            print("Error: El directorio seleccionado no es válido.")
   

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