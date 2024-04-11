import matplotlib
import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MatplotlibWidget, self).__init__(fig)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gráfico Matplotlib en PyQt6')
        self.setGeometry(100, 100, 800, 600)

        # Crear un widget de Matplotlib
        self.matplotlib_widget = MatplotlibWidget(self)
        self.setCentralWidget(self.matplotlib_widget)

        # Agregar datos al gráfico
        self.plotData()

    def plotData(self):
        # Aquí puedes agregar tus datos y graficarlos
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 5, 7, 11]
        self.matplotlib_widget.axes.plot(x, y, color='white')  # Color de la línea
        self.matplotlib_widget.axes.set_facecolor('black')  # Color de fondo
        self.matplotlib_widget.axes.set_title('Mi Gráfico', color='white')  # Color del título
        self.matplotlib_widget.axes.spines['bottom'].set_color('white')  # Color del borde inferior
        self.matplotlib_widget.axes.spines['top'].set_color('white')  # Color del borde superior
        self.matplotlib_widget.axes.spines['left'].set_color('white')  # Color del borde izquierdo
        self.matplotlib_widget.axes.spines['right'].set_color('white')  # Color del borde derecho
        self.matplotlib_widget.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())