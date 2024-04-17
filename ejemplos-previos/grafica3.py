import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsProxyWidget
import pyqtgraph as pg
import numpy as np

class GraphTestWindow(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Crear una escena para el QGraphicsView
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Crear datos de ejemplo para las temperaturas
        temperatura_bloque = np.random.rand(100)
        temperatura_liquido = np.random.rand(100)
        temperatura_consigna = np.random.rand(100)

        # Llamar a la función pintar_grafica para mostrar la gráfica en el QGraphicsView
        self.pintar_grafica(temperatura_bloque, temperatura_liquido, temperatura_consigna)

    def pintar_grafica(self, temperatura_bloque, temperatura_liquido, temperatura_consigna):
        """Pinta una gráfica utilizando PyQtGraph y la muestra en un QGraphicsView."""
        # Crear un widget de gráfico
        self.plot_widget = pg.PlotWidget()

        # Personalizar la apariencia del gráfico
        self.plot_widget.setBackground('k')
        self.plot_widget.setTitle('Rampa de enfriamiento')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)

        # Agregar las líneas de la gráfica
        self.plot_widget.plot(temperatura_bloque, pen=pg.mkPen(color='r'), name='Temperatura Bloque')
        self.plot_widget.plot(temperatura_liquido, pen=pg.mkPen(color='b'), name='Temperatura Líquido')
        self.plot_widget.plot(temperatura_consigna, pen=pg.mkPen(color='#939393'), name='Temperatura Consigna')

        # Crear un proxy widget para el plot_widget
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.plot_widget)

        # Ajustar el tamaño del proxy para que coincida con el plot_widget
        proxy.setPos(0, 0)
        proxy.resize(self.plot_widget.width(), self.plot_widget.height())

        # Agregar el proxy a la escena
        self.scene.addItem(proxy)

        # Agregar etiquetas de texto para los ejes x e y
        x_label = QGraphicsTextItem('timestamp (s)')
        y_label = QGraphicsTextItem('temperature (ºC)')
        self.scene.addItem(x_label)
        self.scene.addItem(y_label)
        x_label.setPos(self.plot_widget.width() - x_label.boundingRect().width(), self.plot_widget.height() - 20)
        y_label.setPos(10, self.plot_widget.height() / 2 - y_label.boundingRect().height() / 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphTestWindow()
    window.setGeometry(100, 100, 800, 600)  # Establecer la geometría de la ventana
    window.show()
    sys.exit(app.exec())
