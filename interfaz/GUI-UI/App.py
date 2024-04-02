from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot, Qt, QObject
from PyQt6.QtGui import QPixmap, QImage, QTransform
import cv2
from interfazv1 import Ui_MainWindow  # Importa la interfaz de la ventana principal
from pygrabber.dshow_graph import FilterGraph
import os
import time
import datetime
import numpy as np
import serial.tools.list_ports
import json

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)  # Configura la interfaz gráfica definida en Ui_MainWindow

        # Conexiones de los botones con los métodos correspondientes
        self.buttonBuscarArchivos.clicked.connect(self.filechooser)
        self.buttonConfiguracion.clicked.connect(self.openConfigCamera)
        self.comboBoxFiltro.addItem("Crear un filtro nuevo ...")

        # Instancia del hilo para captura de video
        self.thread = VideoThread()

        # Llena el combobox de cámaras disponibles
        self.fillCameras()
        self.list_cameras()

        # Conexiones de señales
        self.comboBoxCamara.currentIndexChanged.connect(self.update_camera_index)
        self.buttonConfiguracion.clicked.connect(self.settings)
        self.checkBoxHabilitarA.stateChanged.connect(self.cambiarPlacaA)
        self.checkBoxHabilitarB.stateChanged.connect(self.cambiarPlacaB)
        self.comboBoxFiltro.currentIndexChanged.connect(self.comprobar_opcion_seleccionada)
        
        # Dimensiones para mostrar la imagen
        self.display_width = self.width() // 2
        self.display_height = self.height() // 2


        # Conectar Sliders con Spin box
        self.hSliderRadioMin.valueChanged.connect(self.dSpinBoxRadioMin.setValue)
        self.hSliderRadioMax.valueChanged.connect(self.dSpinBoxRadioMax.setValue)
        self.hSliderGradoPolig.valueChanged.connect(self.dSpinBoxGradoPolig.setValue)
        self.hSliderUmbral.valueChanged.connect(self.dSpinBoxUmbral.setValue)

        self.hSliderTempMin.valueChanged.connect(self.dSpinBoxTempMin.setValue)
        self.hSliderTempMax.valueChanged.connect(self.dSpinBoxTempMax.setValue)
        self.hSliderTempSet.valueChanged.connect(self.dSpinBoxTempSet.setValue)

        # Conectar Spin boxes con Sliders
        self.dSpinBoxRadioMin.valueChanged.connect(self.hSliderRadioMin.setValue)
        self.dSpinBoxRadioMax.valueChanged.connect(self.hSliderRadioMax.setValue)
        self.dSpinBoxGradoPolig.valueChanged.connect(self.hSliderGradoPolig.setValue)
        self.dSpinBoxUmbral.valueChanged.connect(self.hSliderUmbral.setValue)

        self.dSpinBoxTempMin.valueChanged.connect(self.hSliderTempMin.setValue)
        self.dSpinBoxTempMax.valueChanged.connect(self.hSliderTempMax.setValue)
        self.dSpinBoxTempSet.valueChanged.connect(self.hSliderTempSet.setValue)




    def list_cameras(self):
        cameras = []
        filter_graph = FilterGraph()
        devices = filter_graph.get_input_devices()

        for index, device in enumerate(devices):
            cameras.append(index)

        return cameras

    def update_camera_index(self, index):
        if self.thread and self.thread.isRunning():
            self.thread.stop()  
            self.thread.finished.connect(self.thread.deleteLater)  

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.set_camera_index(index)
        self.thread.start()

    def fillCameras(self):
        available_cameras = self.get_available_cameras()
        for camera_index, camera_name in available_cameras.items():
            self.comboBoxCamara.addItem(camera_name)

    def settings(self):
        selected_index = self.comboBoxCamara.currentIndex()
        if selected_index == -1:
            QMessageBox.critical(self, "Error", "No se ha seleccionado ninguna cámara.", QMessageBox.StandardButton.Ok)
        else:
            self.thread.settings()









    def cambiarPlacaA(self):
        # Habilita o deshabilita campos según el estado del checkbox
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
            

    def buscar_carpetas_sns(self, directorio):
        # Retorna una lista de carpetas que comienzan con "SNS" dentro del directorio dado
        carpetas = [nombre for nombre in os.listdir(directorio) if os.path.isdir(os.path.join(directorio, nombre))]
        carpetas_sns = [carpeta for carpeta in carpetas if carpeta.startswith("SNS")]
        return carpetas_sns

    def filechooser(self):
        # Abre un diálogo para seleccionar una carpeta
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        
        if file_dialog.exec():
            selected_folder = file_dialog.selectedFiles()
            carpeta_seleccionada = selected_folder[0]
            self.txtArchivos.setText(carpeta_seleccionada)
            carpetas_sns = self.buscar_carpetas_sns(carpeta_seleccionada)
            
            if carpetas_sns:
                self.comboBoxFiltro.clear()
                self.comboBoxFiltro.addItem("Crear un filtro nuevo ...")
                for carpeta in carpetas_sns:
                    self.comboBoxFiltro.addItem(carpeta)
            else:
                print("No se encontraron carpetas que empiecen por 'SNS' dentro de la carpeta seleccionada.")

    def comprobar_opcion_seleccionada(self, index):
        if index == 0:  
            if(self.txtArchivos.text() == None or self.txtArchivos.text() == ""):
                QMessageBox.warning(self, "Alerta", "Seleccione una carpeta para guardar los filtros antes de continuar.")
                self.filechooser()
            nombre_carpeta = self.obtener_nombre_carpeta()
            if nombre_carpeta:
                self.crear_carpeta(nombre_carpeta)
        else:
            datos = self.leer_json_filtro(self.txtArchivos.text() + "/" + self.comboBoxFiltro.currentText() + "/" + "filter.json")
            self.rellenar_datos(datos)
            print(datos)

    def obtener_nombre_carpeta(self):
        # Abre un diálogo para ingresar el nombre de la carpeta
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Nombre del filtro")
        
        etiqueta = QLabel("Ingrese el nombre del filtros:")
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
        fecha_actual = datetime.datetime.now().strftime("%Y%m%d")
        nombre_carpeta_sns = f"SNS_{fecha_actual}_{nombre_carpeta}"
        directorio_seleccionado = self.txtArchivos.text()
        
        if os.path.isdir(directorio_seleccionado):
            ruta_carpeta_sns = os.path.join(directorio_seleccionado, nombre_carpeta_sns)
            os.makedirs(ruta_carpeta_sns)
            print(f"Carpeta '{nombre_carpeta_sns}' creada exitosamente en '{directorio_seleccionado}'.")
            carpetas_sns = self.buscar_carpetas_sns(directorio_seleccionado)
            self.comboBoxFiltro.clear()
            self.comboBoxFiltro.addItem("Crear un filtro nuevo ...")
            for carpeta in carpetas_sns:
                self.comboBoxFiltro.addItem(carpeta)
            self.comboBoxFiltro.setCurrentText(nombre_carpeta_sns)
        else:
            print("Error: El directorio seleccionado no es válido.")

    def openConfigCamera(self):
        print("Configurando cámara...")




    ######################### PARTE DEL JSON #################################
        


    def leer_json_filtro(self, archivo_json):
        """Lee un archivo JSON y devuelve los datos relevantes"""
        with open(archivo_json, 'r') as f:
            data = json.load(f)

        label = data.get('label', 'Sin etiqueta')
        storage_temperature = data.get('storage_temperature', 0)
        sampler_id = data.get('sampler_id', 'Sin ID')
        filter_position = data.get('filter_position', 0)
        air_volume = data.get('air_volume', 0.0)
        start_time = data.get('start_time', 'Sin hora de inicio')
        end_time = data.get('end_time', 'Sin hora de fin')
        observations = data.get('observations', 'Sin observaciones')

        return {
            'label': label,
            'storage_temperature': storage_temperature,
            'sampler_id': sampler_id,
            'filter_position': filter_position,
            'air_volume': air_volume,
            'start_time': start_time,
            'end_time': end_time,
            'observations': observations
        }



    def rellenar_datos(self, datos):
        # Asigna los valores correspondientes a cada campo de texto
        self.txtNombreFiltro.setText(datos['label'])
        self.txtTempStorage.setText(str(datos['storage_temperature']))
        self.txtIdMuestreador.setText(datos['sampler_id'])
        self.txtPosFilter.setText(str(datos['filter_position']))
        self.txtAirVol.setText(str(datos['air_volume']))
        self.txtHoraInicio.setDateTime(QtCore.QDateTime.fromString(datos['start_time'], "yyyy-MM-dd hh:mm"))
        self.txtHoraFin.setDateTime(QtCore.QDateTime.fromString(datos['end_time'], "yyyy-MM-dd hh:mm"))
        
        # Observaciones puede ser nulo, así que verificamos antes de asignar
        if datos['observations'] is not None:
            self.txaObservFiltro.setPlainText(datos['observations'])
        else:
            self.txaObservFiltro.clear()  # Limpiamos el campo si las observaciones son nulas



    ################################   DESLIZADORES   #############################

    




    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Actualiza el QLabel con una nueva imagen de OpenCV"""
        qt_img = self.convert_cv_qt(cv_img)
        transform = QTransform()
        transform.rotate(90)
        qt_img = qt_img.transformed(transform)
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

    def get_available_cameras(self) :
        """Obtiene las cámaras disponibles utilizando pygrabber"""
        devices = FilterGraph().get_input_devices()
        available_cameras = {}
        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name
        return available_cameras

    def get_status(self):
        """Actualiza la fecha y hora en el widget datetime"""
        self.datetime.setText(f'{datetime.datetime.now():%m/%d/%Y %H:%M:%S}')

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.cap = None
        self._run_flag = True

    def run(self):
        """Inicia el hilo para la captura de video"""
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        while self._run_flag:
            ret, cv_img = self.cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        self.cap.release()

    def stop(self):
        """Detiene el hilo"""
        self._run_flag = False
        self.wait()

    def settings(self):
        """Abre la configuración de la cámara"""
        self.cap.set(cv2.CAP_PROP_SETTINGS, 1)

    def save(self):
        """Guarda la imagen capturada"""
        ret, cv_img = self.cap.read()
        if ret:
            cv2.imwrite(r'C:\Users\david\Desktop\interfaz-V0.1\imagenes-prueba', cv_img)

    def set_camera_index(self, index):
        """Establece el índice del dispositivo de captura"""
        self.camera_index = index

# Creación de la aplicación y ventana principal
app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
