from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtCore import QTimer
from interfazv1 import Ui_MainWindow
import serial.tools.list_ports

import time
import datetime

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.buttonBuscarArchivos.clicked.connect(self.filechooser)

    
    
    
    
    
    def filechooser(self):
        # Abrir el diálogo de selección de archivos
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        
        # Se selecciona una carpeta y se muestra la ruta
        if file_dialog.exec():
            selected_folder = file_dialog.selectedFiles()
            self.txtArchivos.setText(selected_folder[0])




        
    def get_status(self):
        self.datetime.setText(f'{datetime.datetime.now():%m/%d/%Y %H:%M:%S}')
        
    #def connect_to_sampler(self):
    #    if self.connect.text() == 'Connect':
    #        result = None
    #        try:
    #            self.sampler = serial.Serial(port=self.comPort.currentText(), baudrate=self.baudrate.currentText(), timeout=0.1, write_timeout=0.1)
    #            time.sleep(2)
    #            self.sampler.write(bytes(f'ECHO\n', encoding='utf-8'))
    #            result = self.sampler.read_until(b'\n').decode().strip()
    #        except serial.serialutil.SerialException as e:
    #            self.statusbar.showMessage(str(e))
    #            self.sampler = None
    #        finally:
    #            if result == 'ACK':
    #                self.statusbar.showMessage('Connected to sampler', 2000)
    #                self.connect.setText('Disconnect')
    #                self.timer.start(1000)
    #                self.FiltersGroup.setEnabled(True)
    #                self.PumpGroup.setEnabled(True)
    #                self.commsGroup.setEnabled(True)
    #            else:
    #                self.statusbar.showMessage('Unable to connect to sampler', 2000)
    #    elif self.connect.text() == 'Disconnect':
    #        self.sampler.close()
    #        self.connect.setText('Connect')
    #        self.datetime.setText('')
    #        self.FiltersGroup.setEnabled(False)
    #        self.PumpGroup.setEnabled(False)
    #        self.commsGroup.setEnabled(False)
    #        self.timer.stop()




app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()