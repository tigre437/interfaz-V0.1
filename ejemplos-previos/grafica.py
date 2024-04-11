import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication

class LineDragger:
    def __init__(self, plot, step_size, min_pos, max_pos):
        self.plot = plot
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.line = pg.InfiniteLine(pos=5, angle=90, movable=True, pen='r')  # Línea vertical inicialmente en x=5
        self.plot.addItem(self.line)
        self.step_size = step_size

        # Conectar el evento de cambio de posición de la línea a la función on_line_dragged
        self.line.sigPositionChanged.connect(self.on_line_dragged)

    def on_line_dragged(self):
        # Obtener el valor de la posición actual de la línea
        pos = self.line.value()
        new_pos = round(pos / self.step_size) * self.step_size

        # Limitar el rango de movimiento de la línea
        if new_pos < self.min_pos:
            new_pos = self.min_pos
        elif new_pos > self.max_pos:
            new_pos = self.max_pos

        # Establecer la nueva posición de la línea
        self.line.setValue(new_pos)

        print("Posición de la línea vertical:", new_pos)

if __name__ == "__main__":
    # Generar algunos datos de ejemplo
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Crear la aplicación de PyQt6
    app = QApplication([])

    # Crear un objeto PlotWidget
    plot = pg.plot()

    # Agregar los datos al gráfico
    plot.plot(x, y)

    # Definir el tamaño del paso para el salto de unidad en unidad
    step_size = 1

    # Definir los límites mínimos y máximos de movimiento de la línea
    min_pos = 0
    max_pos = 10

    # Inicializar el LineDragger con el tamaño de paso y los límites definidos
    line_dragger = LineDragger(plot, step_size, min_pos, max_pos)

    # Mostrar la ventana
    app.exec()