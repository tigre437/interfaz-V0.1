import os
import cv2
import json
import numpy as np
import pyqtgraph as pg
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    QFileDialog, QDialog, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QGraphicsProxyWidget
)
from PyQt6.QtCore import pyqtSlot, Qt, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap, QTransform
from interfazv1 import Ui_MainWindow  # Importa la interfaz de la ventana principal
from pygrabber.dshow_graph import FilterGraph
import datetime
from configFotos import Ui_Dialog



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)  # Configura la interfaz gráfica definida en Ui_MainWindow


        # Crear una instancia del diálogo y almacenarla como un atributo de instancia
        self.dialog = QtWidgets.QDialog()
        self.dialog.ui = Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)

        # Conectar el botón de aceptar del cuadro de diálogo a la función guardar_datos_camara
        self.dialog.ui.buttonBox.accepted.connect(self.guardar_datos_camara)


        self.thread = VideoThread()


        # Graficas
        scene = QtWidgets.QGraphicsScene()

        # Asignar el QGraphicsScene a graphicsView
        self.graphicsView.setScene(scene)

        # Conexiones de los botones con los métodos correspondientes
        self.buttonBuscarArchivos.clicked.connect(self.filechooser)
        self.buttonConfiguracion.clicked.connect(self.settings)
        self.comboBoxFiltro.addItem("Crear un filtro nuevo ...")
        

        # Llena el combobox de cámaras disponibles
        self.fillCameras()
        self.list_cameras()

        # Conexiones de señales
        
        self.comboBoxCamara.currentIndexChanged.connect(self.update_camera_index)
        self.checkBoxHabilitarA.stateChanged.connect(self.cambiarPlacaA)
        self.checkBoxHabilitarB.stateChanged.connect(self.cambiarPlacaB)
        self.comboBoxFiltro.currentIndexChanged.connect(self.comprobar_opcion_seleccionada)
        self.buttonGuardarFiltro.clicked.connect(self.guardar_datos_filtro)
        self.buttonCancelarFiltro.clicked.connect(self.cancelar_cambios_filtro)
        self.buttonIniciar.clicked.connect(self.iniciar_experimento)

        self.tabWidget_2.currentChanged.connect(self.tab_changed)
        self.checkBoxHabilitarA.stateChanged.connect(self.tab_changed)
        self.checkBoxHabilitarB.stateChanged.connect(self.tab_changed)
        self.checkBoxAmbasPlacas.stateChanged.connect(self.desactivar_placaB)

        self.buttonGuardarParamDetec.clicked.connect(self.guardar_datos_detection)
        self.buttonCancelarParamDetec.clicked.connect(self.cancelar_cambios_detect)

        self.buttonGuardarParamTemp.clicked.connect(self.guardar_datos_temp)
        self.buttonCancelarParamTemp.clicked.connect(self.cancelar_cambios_temp)

        self.buttonConfiguracionExper.clicked.connect(self.open_dialog)

        #self.buttonIniciar.clicked.connect(self.iniciar_expermiento)
        
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

        self.buttonConectarTermo.clicked.connect(self.save)

        #Aqui hay que setear de primeras las temperaturas de los liquidos
        #self.pintar_grafica(temp_bloc, temp_liquid, temp_set)


        # Timer de la grafica

        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.actualizar_grafica)
        #self.timer.start(1000)

        # CADA TIMER SE AÑADE UN VALOR A LAS LISTAS DE DATO


    def detener_timer(self):
        self.timer.stop()

    def open_dialog(self):
        # Ruta al archivo camera.json
        ruta_camera_json = self.obtener_ruta_json("camera.json")

        # Verificar si el archivo existe
        if os.path.exists(ruta_camera_json):
            # Leer el archivo y obtener los datos de la cámara
            datos_camara = self.leer_json_camara(ruta_camera_json)
        else:
            # Si el archivo no existe, crearlo con valores predeterminados
            self.crear_json_camara(os.path.dirname(ruta_camera_json))
            datos_camara = {
                'frecuencia': 2,
                'habilitado': True,
                'temp_set': -3
            }

        # Rellenar los campos del diálogo con los datos de la cámara
        self.dialog.ui.labelFrecuencia.setText(str(datos_camara['frecuencia']))
        self.dialog.ui.checkBox.setChecked(datos_camara['habilitado'])
        self.dialog.ui.doubleSpinTemp.setValue(datos_camara['temp_set'])

        # Mostrar el diálogo
        self.dialog.exec()

    def desactivar_placaB(self):
        if self.checkBoxAmbasPlacas.isChecked():
            self.checkBoxHabilitarB.setChecked(False)
            self.checkBoxHabilitarB.setEnabled(False)
            self.copiarDatosA()
        else:
            self.checkBoxHabilitarB.setEnabled(True)

    def copiarDatosA(self):
        self.txtNombrePlacaB.setText(self.txtNombrePlacaA.text())
        self.txtVDropPlacaB.setText(self.txtVDropPlacaA.text())
        self.txtVWashPlacaB.setText(self.txtVWashPlacaA.text())
        self.txtFactorDilucPlacaB.setText(self.txtFactorDilucPlacaA.text())
        self.txtFraccFiltroPlacaB.setText(self.txtFraccFiltroPlacaA.text())
        self.txtTasaMuestreoPlacaB.setText(self.txtTasaMuestreoPlacaA.text())
        self.txtVelEnfriamientoPlacaB.setText(self.txtVelEnfriamientoPlacaA.text())
        self.txtObservPlacaB.setPlainText(self.txtObservPlacaA.toPlainText())


    def cambiarPlacaA(self):
        """Habilita o deshabilita campos según el estado del checkbox."""
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
        """Habilita o deshabilita campos según el estado del checkbox."""
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
        """Retorna una lista de carpetas que comienzan con 'SNS' dentro del directorio dado."""
        carpetas = [nombre for nombre in os.listdir(directorio) if os.path.isdir(os.path.join(directorio, nombre))]
        carpetas_sns = [carpeta for carpeta in carpetas if carpeta.startswith("SNS")]
        return carpetas_sns

    def filechooser(self):
        """Abre un diálogo para seleccionar una carpeta."""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        
        if file_dialog.exec():
            selected_folder = file_dialog.selectedFiles()
            carpeta_seleccionada = selected_folder[0]
            self.txtArchivos.setText(carpeta_seleccionada)
            carpetas_sns = self.buscar_carpetas_sns(carpeta_seleccionada)
            
            if carpetas_sns:

                if self.comboBoxFiltro.count() > 1:
                    self.comboBoxFiltro.clear()
                    self.comboBoxFiltro.addItem("Crear un filtro nuevo ...")
                for carpeta in carpetas_sns:
                    self.comboBoxFiltro.addItem(carpeta)
            else:
                print("No se encontraron carpetas que empiecen por 'SNS' dentro de la carpeta seleccionada.")

    def comprobar_opcion_seleccionada(self, index):
        """Comprueba la opción seleccionada en el combobox de filtros."""
        if index == 0:  
            if(self.txtArchivos.text() == None or self.txtArchivos.text() == ""):
                QMessageBox.warning(self, "Alerta", "Seleccione una carpeta para guardar los filtros antes de continuar.")
                self.filechooser()
            nombre_carpeta = self.obtener_nombre_carpeta()
            if nombre_carpeta:
                self.crear_carpeta(nombre_carpeta)
        else:
            datos_filtro = self.leer_json_filtro(self.txtArchivos.text() + "/" + self.comboBoxFiltro.currentText() + "/" + "filter.json")
            if (datos_filtro != None):
                self.rellenar_datos_filtro(datos_filtro)

            datos_detection = self.leer_json_detection(self.txtArchivos.text() + "/" + self.comboBoxFiltro.currentText() + "/" + "detection.json")
            if (datos_detection != None):
                self.rellenar_datos_detection(datos_detection)

            datos_temp = self.leer_json_temp(self.txtArchivos.text() + "/" + self.comboBoxFiltro.currentText() + "/" + "temp.json")
            if (datos_temp != None):
                self.rellenar_datos_temp(datos_temp)
    

    def cancelar_cambios_filtro(self):
        """Cancela la edición del filtro seleccionado."""
        datos_filtro = self.leer_json_filtro(self.txtArchivos.text() + "/" + self.comboBoxFiltro.currentText() + "/" + "filter.json")
        if (datos_filtro != None):
            self.rellenar_datos_filtro(datos_filtro)

    def cancelar_cambios_detect(self):
        """Cancela la edición del filtro seleccionado."""
        datos_detection = self.leer_json_detection(self.txtArchivos.text() + "/" + self.comboBoxFiltro.currentText() + "/" + "detection.json")
        if (datos_detection != None):
            self.rellenar_datos_detection(datos_detection)

    def cancelar_cambios_temp(self):
        """Cancela la edición del filtro seleccionado."""
        datos_temp = self.leer_json_temp(self.txtArchivos.text() + "/" + self.comboBoxFiltro.currentText() + "/" + "temp.json")
        if (datos_temp != None):
            self.rellenar_datos_temp(datos_temp)

    def obtener_nombre_carpeta(self):
        """Abre un diálogo para ingresar el nombre de la carpeta."""
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
        """Crea una carpeta para el nuevo filtro."""
        fecha_actual = datetime.datetime.now().strftime("%Y%m%d")
        nombre_carpeta_sns = f"SNS_{fecha_actual}_{nombre_carpeta}"
        directorio_seleccionado = self.txtArchivos.text()
        
        if os.path.isdir(directorio_seleccionado):
            ruta_carpeta_sns = os.path.join(directorio_seleccionado, nombre_carpeta_sns)
            os.makedirs(ruta_carpeta_sns)
            print(f"Carpeta '{nombre_carpeta_sns}' creada exitosamente en '{directorio_seleccionado}'.")
            carpetas_sns = self.buscar_carpetas_sns(directorio_seleccionado)

            # Desconecta la señal currentIndexChanged temporalmente
            self.comboBoxFiltro.currentIndexChanged.disconnect(self.comprobar_opcion_seleccionada)
            self.comboBoxFiltro.clear()
            self.comboBoxFiltro.addItem("Crear un filtro nuevo ...")
            for carpeta in carpetas_sns:
                self.comboBoxFiltro.addItem(carpeta)
            self.comboBoxFiltro.setCurrentText(nombre_carpeta_sns)

            # Crear el archivo filter.json
            self.crear_json_filtro(ruta_carpeta_sns)

            # Cargar los datos del filtro recién creado
            self.comprobar_opcion_seleccionada(1)  # Índice 1 para seleccionar el nuevo filtro

            # Vuelve a conectar la señal currentIndexChanged
            self.comboBoxFiltro.currentIndexChanged.connect(self.comprobar_opcion_seleccionada)
            
        else:
            print("Error: El directorio seleccionado no es válido.")


    ######################### JSON #################################

    def leer_json_filtro(self, archivo_json):
        """Lee un archivo JSON y devuelve los datos relevantes."""
        try:
            with open(archivo_json, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(self, "Advertencia", f"El archivo '{archivo_json}' no existe.", QMessageBox.StandardButton.Ok)
            return
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Advertencia", f"El archivo '{archivo_json}' no es un archivo JSON válido.", QMessageBox.StandardButton.Ok)
            return

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

    def rellenar_datos_filtro(self, datos):
        """Asigna los valores correspondientes a cada campo de texto."""
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

    def crear_json_filtro(self, ruta_carpeta_sns):
        """Crea el archivo filter.json."""
        ruta_filter_json = os.path.join(ruta_carpeta_sns, 'filter.json')
        with open(ruta_filter_json, 'w') as file:
            json.dump({
                "label": "Sin etiqueta",
                "storage_temperature": "0",
                "sampler_id": "Sin ID",
                "filter_position": "0",
                "air_volume": "0.0",
                "start_time": "2000-01-01 00:00",
                "end_time": "2000-01-01 00:00",
                "observations": "Sin observaciones"
            }
            , file) 

    def guardar_datos_filtro(self):
        """Guarda los datos del filtro en un archivo JSON."""
        # Obtener los datos de los campos de texto
        label = self.txtNombreFiltro.text()
        storage_temperature = self.txtTempStorage.text()
        sampler_id = self.txtIdMuestreador.text()
        filter_position = self.txtPosFilter.text()
        air_volume = self.txtAirVol.text()
        start_time = self.txtHoraInicio.dateTime().toString("yyyy-MM-dd hh:mm")
        end_time = self.txtHoraFin.dateTime().toString("yyyy-MM-dd hh:mm")
        observations = self.txaObservFiltro.toPlainText()

        # Crear un diccionario con los datos
        datos_filtro = {
            'label': label,
            'storage_temperature': storage_temperature,
            'sampler_id': sampler_id,
            'filter_position': filter_position,
            'air_volume': air_volume,
            'start_time': start_time,
            'end_time': end_time,
            'observations': observations
        }

        # Obtener la ruta del archivo JSON
        ruta_json = self.obtener_ruta_json("filter.json")

        # Guardar los datos en el archivo JSON
        with open(ruta_json, 'w') as file:
            json.dump(datos_filtro, file)

        QMessageBox.information(self, "Guardado", "Los datos del filtro se han actualizado correctamente.", QMessageBox.StandardButton.Ok)



    def leer_json_camara(self, archivo_json):
        """Lee un archivo JSON y devuelve los datos relevantes."""
        try:
            with open(archivo_json, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(self, "Advertencia", f"El archivo '{archivo_json}' no existe.", QMessageBox.StandardButton.Ok)
            return
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Advertencia", f"El archivo '{archivo_json}' no es un archivo JSON válido.", QMessageBox.StandardButton.Ok)
            return

        frecuencia = data.get('frecuencia', 2)
        habilitado = data.get('habilitado', True)
        temp_set = data.get('temp_set', -3)

        return {
            'frecuencia': frecuencia,
            'habilitado': habilitado,
            'temp_set': temp_set
        }

    def rellenar_datos_camara(self, datos):
        """Asigna los valores correspondientes a cada campo de texto."""
        self.labelFrecuencia.setText(str(datos['frecuencia']))
        self.checkBox.setChecked(datos['habilitado'])
        self.doubleSpinTemp.setValue(datos['temp_set'])

    def crear_json_camara(self, ruta_carpeta_sns):
        """Crea el archivo camera.json."""
        ruta_camera_json = os.path.join(ruta_carpeta_sns, 'camera.json')
        with open(ruta_camera_json, 'w') as file:
            json.dump(
                {
                    "Frec": 2,
                    "habilitado": True,
                    "Temp_Set": -3
                },
                file
            )

    def guardar_datos_camara(self):
        """Guarda los datos de la cámara en un archivo JSON."""
        # Obtener los datos de los campos de texto del diálogo
        frecuencia = self.dialog.ui.labelFrecuencia.text()
        print(frecuencia)
        habilitado = self.dialog.ui.checkBox.isChecked()
        temp_set = self.dialog.ui.doubleSpinTemp.value()

        # Crear un diccionario con los datos
        datos_camara = {
            'frecuencia': frecuencia,
            'habilitado': habilitado,
            'temp_set': temp_set
        }

        # Obtener la ruta del archivo camera.json
        ruta_camera_json = self.obtener_ruta_json("camera.json")

        # Guardar los nuevos datos en el archivo camera.json
        with open(ruta_camera_json, 'w') as file:
            json.dump(datos_camara, file)

        # Informar al usuario que los datos han sido guardados correctamente
        QtWidgets.QMessageBox.information(self, "Guardado", "Los datos de la cámara se han actualizado correctamente.", QtWidgets.QMessageBox.StandardButton.Ok)




    def leer_json_detection(self, archivo_json):
        """Lee un archivo JSON de detección y devuelve los datos relevantes."""
        try:
            with open(archivo_json, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(self, "Advertencia", f"El archivo '{archivo_json}' no existe.", QMessageBox.StandardButton.Ok)
            return
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Advertencia", f"El archivo '{archivo_json}' no es un archivo JSON válido.", QMessageBox.StandardButton.Ok)
            return

        threshold = data.get('threshold', 180)
        min_radius = data.get('min_radius', 14)
        max_radius = data.get('max_radius', 20)
        polygon = data.get('polygon', 5)

        return {
            'threshold': threshold,
            'min_radius': min_radius,
            'max_radius': max_radius,
            'polygon': polygon
        }

    def rellenar_datos_detection(self, datos):
        """Asigna los valores correspondientes a cada campo de texto de detección."""
        self.hSliderUmbral.setValue(datos['threshold'])
        self.dSpinBoxUmbral.setValue(datos['threshold'])
        self.hSliderRadioMin.setValue(datos['min_radius'])
        self.dSpinBoxRadioMin.setValue(datos['min_radius'])
        self.hSliderRadioMax.setValue(datos['max_radius'])
        self.dSpinBoxRadioMax.setValue(datos['max_radius'])
        self.hSliderGradoPolig.setValue(datos['polygon'])
        self.dSpinBoxGradoPolig.setValue(datos['polygon'])

    def crear_json_detection(self, ruta_carpeta_sns):
        """Crea el archivo detection.json."""
        ruta_detection_json = os.path.join(ruta_carpeta_sns, 'detection.json')
        with open(ruta_detection_json, 'w') as file:
            json.dump({
                "threshold": 180,
                "min_radius": 14,
                "max_radius": 20,
                "polygon": 5
            }
            , file) 

    def guardar_datos_detection(self):
        """Guarda los datos de detección en un archivo JSON."""
        # Obtener los datos de los campos de detección
        threshold = self.dSpinBoxUmbral.value()
        min_radius = self.dSpinBoxRadioMin.value()
        max_radius = self.dSpinBoxRadioMax.value()
        polygon = self.dSpinBoxGradoPolig.value()


        # Crear un diccionario con los datos de detección
        datos_detection = {
            'threshold': threshold,
            'min_radius': min_radius,
            'max_radius': max_radius,
            'polygon': polygon
        }

        # Obtener la ruta del archivo JSON
        ruta_json = self.obtener_ruta_json("detection.json")

        # Guardar los datos de detección en el archivo JSON
        with open(ruta_json, 'w') as file:
            json.dump(datos_detection, file)

        QMessageBox.information(self, "Guardado", "Los datos de detección se han actualizado correctamente.", QMessageBox.StandardButton.Ok)


    def leer_json_temp(self, archivo_json):
        """Lee un archivo JSON de temperatura y devuelve los datos relevantes."""
        try:
            with open(archivo_json, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(self, "Advertencia", f"El archivo '{archivo_json}' no existe.", QMessageBox.StandardButton.Ok)
            return
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Advertencia", f"El archivo '{archivo_json}' no es un archivo JSON válido.", QMessageBox.StandardButton.Ok)
            return

        temp_max = data.get('tempMax', 0.00)
        temp_min = data.get('tempMin', 0.00)
        temp_set = data.get('tempSet', 0.00)

        return {
            'tempMax': temp_max,
            'tempMin': temp_min,
            'tempSet': temp_set
        }

    def rellenar_datos_temp(self, datos):
        """Asigna los valores correspondientes a cada campo de texto de temperatura."""
        self.dSpinBoxTempMax.setValue(datos['tempMax'])
        self.dSpinBoxTempMin.setValue(datos['tempMin'])
        self.dSpinBoxTempSet.setValue(datos['tempSet'])

    def crear_json_temp(self, ruta_carpeta_sns):
        """Crea el archivo temp.json."""
        ruta_temp_json = os.path.join(ruta_carpeta_sns, 'temp.json')
        with open(ruta_temp_json, 'w') as file:
            json.dump({
                "tempMax": 0.00,
                "tempMin": 0.00,
                "tempSet": 0.00
            }, file) 

    def guardar_datos_temp(self):
        """Guarda los datos de temperatura en un archivo JSON."""
        # Obtener los datos de los campos de temperatura
        temp_max = self.dSpinBoxTempMax.value()
        temp_min = self.dSpinBoxTempMin.value()
        temp_set = self.dSpinBoxTempSet.value()

        # Crear un diccionario con los datos de temperatura
        datos_temp = {
            'tempMax': temp_max,
            'tempMin': temp_min,
            'tempSet': temp_set
        }

        # Obtener la ruta del archivo JSON
        ruta_json = self.obtener_ruta_json("temp.json")

        # Guardar los datos de temperatura en el archivo JSON
        with open(ruta_json, 'w') as file:
            json.dump(datos_temp, file)

        QMessageBox.information(self, "Guardado", "Los datos de temperatura se han actualizado correctamente.", QMessageBox.StandardButton.Ok)




    def obtener_ruta_json(self, archivo):
        """Obtiene la ruta completa del archivo JSON."""
        carpeta_seleccionada = self.txtArchivos.text()
        nombre_filtro = self.comboBoxFiltro.currentText()
        ruta_json = os.path.join(carpeta_seleccionada, nombre_filtro, archivo)
        return ruta_json
    


    ######################## GRAFICA ####################################

    def actualizar_grafica(self):

        #temperatura_bloque = [20, 25, 30, 28, 27, 26, 25, 24, 23, 22]
        #temperatura_liquido = [22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
        #temperatura_consigna = [25, 25, 25, 25, 25, 25, 25, 25, 25, 25]
        #self.pintar_grafica(temperatura_bloque, temperatura_liquido, temperatura_consigna)
        print("hola")
    
    def pintar_grafica(self, temperatura_bloque, temperatura_liquido, temperatura_consigna):
        """Pinta una gráfica utilizando PyQtGraph y la muestra en un QGraphicsView."""
        # Crear un widget de gráfico
        self.plot_widget = pg.PlotWidget()

        # Agregar las líneas de la gráfica
        self.plot_widget.plot(temperatura_bloque, pen=pg.mkPen(color='r'), name='Temperatura Bloque')  # Línea roja para la temperatura del bloque
        self.plot_widget.plot(temperatura_liquido, pen=pg.mkPen(color='b'), name='Temperatura Líquido')  # Línea azul para la temperatura del líquido
        self.plot_widget.plot(temperatura_consigna, pen=pg.mkPen(color='#939393'), name='Temperatura Consigna')  # Línea gris claro para la temperatura de consigna

        # Personalizar la apariencia del gráfico
        self.plot_widget.setBackground('k')  # Color de fondo
        self.plot_widget.setTitle('Rampa de enfriamiento')  # Título
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)  # Mostrar rejilla
        self.plot_widget.getAxis('bottom').setPen(pg.mkPen(color='w'))  # Color del eje x
        self.plot_widget.getAxis('left').setPen(pg.mkPen(color='w'))  # Color del eje y
        self.plot_widget.getAxis('bottom').setTextPen('w')  # Color de los números en el eje x
        self.plot_widget.getAxis('left').setTextPen('w')  # Color de los números en el eje y

        # Crear un proxy widget para el plot_widget
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.plot_widget)

        # Ajustar el tamaño del proxy para que coincida con el plot_widget
        proxy.setPos(0, 0)
        proxy.resize(self.graphicsView.width(), self.graphicsView.height())

        # Agregar el proxy al graphicsView
        self.graphicsView.scene().addItem(proxy)

    ######################### EXPERIMENTO #################################
        
    def obtener_ruta_experimento_json(self):
        """Obtiene la ruta completa del archivo JSON."""
        carpeta_seleccionada = self.txtArchivos.text()
        nombre_filtro = self.comboBoxFiltro.currentText()
        fecha_actual = datetime.datetime.now().strftime("%Y%m%d")
        hora_actual = datetime.datetime.now().strftime("%H%M")

        placa = self.tabWidget_2.tabText(self.tabWidget_2.currentIndex())
        if (placa == "Placa A"):
            nombre_experimento = self.txtNombrePlacaA.text()
        else:
            nombre_experimento = self.txtNombrePlacaB.text()

        nombre_experimento_con_fecha = f"{fecha_actual}_{hora_actual}_{nombre_experimento}_{self.tabWidget_2.tabText(self.tabWidget_2.currentIndex())}"
        if (not self.checkBoxAmbasPlacas.isChecked()):
            nombre_experimento_con_fecha = f"{fecha_actual}_{hora_actual}_{nombre_experimento}_{self.tabWidget_2.tabText(self.tabWidget_2.currentIndex())}"
        else:
            nombre_experimento_con_fecha = f"{fecha_actual}_{hora_actual}_{self.txtNombrePlacaA.text()}_Placa_AB"
        
        ruta_json = os.path.join(carpeta_seleccionada, nombre_filtro, nombre_experimento_con_fecha, "experimento.json")
        return ruta_json
        
    def obtener_ruta_experimento(self):
        """Obtiene la ruta completa del archivo JSON."""
        carpeta_seleccionada = self.txtArchivos.text()
        nombre_filtro = self.comboBoxFiltro.currentText()
        placa = self.tabWidget_2.tabText(self.tabWidget_2.currentIndex())
        if (placa == "Placa A"):
            nombre_experimento = self.txtNombrePlacaA.text()
        else:
            nombre_experimento = self.txtNombrePlacaB.text()

        fecha_actual = datetime.datetime.now().strftime("%Y%m%d")
        hora_actual = datetime.datetime.now().strftime("%H%M")

        if (not self.checkBoxAmbasPlacas.isChecked()):
            nombre_experimento_con_fecha = f"{fecha_actual}_{hora_actual}_{nombre_experimento}_{placa}"
        else:
            nombre_experimento_con_fecha = f"{fecha_actual}_{hora_actual}_{self.txtNombrePlacaA.text()}_Placa_AB"
        
        ruta_experimento = os.path.join(carpeta_seleccionada, nombre_filtro, nombre_experimento_con_fecha)
        return ruta_experimento

    def iniciar_experimento(self):
        datos_filtro = self.leer_json_filtro(os.path.join(self.txtArchivos.text(), self.comboBoxFiltro.currentText(), "filter.json"))
        datos_detection = self.leer_json_detection(os.path.join(self.txtArchivos.text(), self.comboBoxFiltro.currentText(), "detection.json"))
        placa = self.tabWidget_2.tabText(self.tabWidget_2.currentIndex())
        if (placa == "Placa A"):
            datos_exper = {
                "v_drop": float(self.txtVDropPlacaA.text()),
                "v_wash": float(self.txtVWashPlacaA.text()),
                "dil_factor": float(self.txtFactorDilucPlacaA.text()),
                "filter_fraction": float(self.txtFraccFiltroPlacaA.text()),
                "sampling_rate": float(self.txtTasaMuestreoPlacaA.text()),
                "cooling_rate": float(self.txtVelEnfriamientoPlacaA.text()),
                "observations_exp": self.txtObservPlacaA.toPlainText()
            }
        else:
            datos_exper = {
                "v_drop": float(self.txtVDropPlacaB.text()),
                "v_wash": float(self.txtVWashPlacaB.text()),
                "dil_factor": float(self.txtFactorDilucPlacaB.text()),
                "filter_fraction": float(self.txtFraccFiltroPlacaB.text()),
                "sampling_rate": float(self.txtTasaMuestreoPlacaB.text()),
                "cooling_rate": float(self.txtVelEnfriamientoPlacaB.text()),
                "observations_exp": self.txtObservPlacaB.toPlainText()
            }
        
        ruta_carpeta_experimento = self.obtener_ruta_experimento()

        # Verificar si la carpeta del experimento ya existe
        if not os.path.exists(ruta_carpeta_experimento):
            os.makedirs(ruta_carpeta_experimento)  # Crear la carpeta del experimento si no existe

        ruta_json = self.obtener_ruta_experimento_json()

        # Verificar si el archivo JSON ya existe y eliminarlo si es así
        if os.path.exists(ruta_json):
            respuesta = self.mostrar_dialogo_confirmacion("Sobreescribir experimento", "¿Estás seguro de que quieres sobreescribir los datos del experimento?")
            if not respuesta:
                return  
            else:
                os.remove(ruta_json)
        
        datos_experimento = {}
        datos_experimento.update(datos_filtro)
        datos_experimento.update(datos_detection)
        datos_experimento.update(datos_exper)

        with open(ruta_json, 'w') as file:
            json.dump(datos_experimento, file)


    def mostrar_dialogo_confirmacion(self, titulo, mensaje):
        dialogo = QMessageBox()
        dialogo.setWindowTitle(titulo)
        dialogo.setText(mensaje)
        dialogo.setIcon(QMessageBox.Icon.Question)
        dialogo.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dialogo.setDefaultButton(QMessageBox.StandardButton.No)
        respuesta = dialogo.exec()
        return respuesta == QMessageBox.StandardButton.Yes


    def tab_changed(self):

        index = self.tabWidget_2.currentIndex()
        
        if index is not None:
            if index == 0:
                self.buttonIniciar.setEnabled(False)
            elif index == 1 and self.checkBoxHabilitarA.isChecked():
                self.buttonIniciar.setEnabled(True)
            elif index == 2 and self.checkBoxHabilitarB.isChecked():
                self.buttonIniciar.setEnabled(True)
            else:
                self.buttonIniciar.setEnabled(False)

    ####################### CAMARA ##############################
    
    def update_camera_index(self, index):
        if self.thread and self.thread.isRunning():
            self.thread.stop()  # Detener el hilo existente
            self.thread.finished.connect(self.thread.deleteLater)  # Eliminar el objeto del hilo después de que termine

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.set_camera_index(index)
        self.thread.start()

    def list_cameras(self):
        """Obtiene una lista de cámaras disponibles."""
        cameras = []
        filter_graph = FilterGraph()
        devices = filter_graph.get_input_devices()

        for index in enumerate(devices):
            cameras.append(index)

        return cameras


    def fillCameras(self):
        """Llena el combobox con las cámaras disponibles."""
        available_cameras = self.get_available_cameras()
        for camera_index, camera_name in available_cameras.items():
            self.comboBoxCamara.addItem(camera_name)

    def settings(self):
        self.thread.settings()

    def save(self):
        self.thread.save()

    #def guardar_imagenes(self):
    #    #CAMBIAR ESTO POR EL VALOR QUE NOS DE EL APARATO
    #    temp_set = 0
    #    if (self.dSpinBoxTempSet.value() == temp_set):
    #        while():


    @pyqtSlot(np.ndarray)

    def get_available_cameras(self):
        """Obtiene las cámaras disponibles utilizando pygrabber."""
        devices = FilterGraph().get_input_devices()
        available_cameras = {}
        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name
        return available_cameras

    def update_image(self, cv_img):
        """Actualiza el QLabel con una nueva imagen de OpenCV"""
        qt_img = self.convert_cv_qt(cv_img)
        
        transform = QTransform()
        transform.rotate(90)
        qt_img = qt_img.transformed(transform)

        # Ajustar el tamaño del widget labelCamara
        self.labelCamara.setPixmap(qt_img)
        self.labelCamara.setFixedSize(qt_img.size())

    def get_status(self):
        """Actualiza la fecha y hora en el widget datetime."""
        self.datetime.setText(f'{datetime.datetime.now():%m/%d/%Y %H:%M:%S}')

    def convert_cv_qt(self, cv_img):
        """Convierte una imagen de OpenCV a QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)

    

####################### CLASE CAMARA ##############################

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
            cv2.imwrite("image.jpg", cv_img)

    def set_camera_index(self, index):
        """Establece el índice del dispositivo de captura"""
        self.camera_index = index

# Creación de la aplicación y ventana principal
app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
