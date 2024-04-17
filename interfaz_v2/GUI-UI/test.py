import time
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

# Simulando los módulos Ins y Lauda
class Ins:
    def __init__(self):
        self.thermostat = Thermostat()

class Thermostat:
    def __init__(self):
        self.t_set = -30
        self.t_int = 20
        self.t_ext = 25
    
    def get_t_set(self):
        return self.t_set
    
    def get_t_int(self):
        return self.t_int
    
    def get_t_ext(self):
        return self.t_ext

# Configuración de parámetros
steptime = 5  # Intervalo de tiempo entre cada paso en segundos

# Inicialización de objetos 'ins'
ins = Ins()

# Inicialización de variables y registro de tiempo
timestamp = 0

# Creación de un DataFrame para almacenar los datos de temperatura
data = pd.DataFrame(data={'timestamp': [timestamp], 't_set': [ins.thermostat.t_set], 't_int': [ins.thermostat.t_int], 't_ext': [ins.thermostat.t_ext]})

# Configuración de la visualización en tiempo real
plt.ion()  # Habilita el modo interactivo de matplotlib
line1, = plt.plot(data["timestamp"], data['t_set'], 'k', label='t_set')  # Configura la línea para la temperatura objetivo
line2, = plt.plot(data["timestamp"], data['t_int'], 'b', label='t_int')  # Configura la línea para la temperatura interna
line3, = plt.plot(data["timestamp"], data['t_ext'], 'r', label='t_ext')  # Configura la línea para la temperatura externa
plt.ylim([-40, 30])  # Establece el rango del eje y
plt.xlabel('timestamp (s)')  # Etiqueta del eje x
plt.ylabel('temperature (ºC)')  # Etiqueta del eje y
plt.legend()  # Muestra la leyenda

# Bucle principal del experimento
try:
    while True:
        timestamp += steptime  # Incrementa el tiempo de experimentación
        
        # Almacena los datos de temperatura en el DataFrame
        data = pd.concat([data, pd.DataFrame(data={
                                'timestamp': [timestamp],
                                't_set': [ins.thermostat.get_t_set()],
                                't_int': [ins.thermostat.get_t_int()],
                                't_ext': [ins.thermostat.get_t_ext()]})],
                                ignore_index=True)
        
        # Actualiza y muestra los datos en tiempo real
        print(f'{data["timestamp"].iloc[-1]}\t{data["t_set"].iloc[-1]}\t{data["t_int"].iloc[-1]}\t{data["t_ext"].iloc[-1]}')
        line1.set_xdata(data["timestamp"])
        line1.set_ydata(data['t_set'])    
        line2.set_xdata(data["timestamp"])
        line2.set_ydata(data['t_int']) 
        line3.set_xdata(data["timestamp"])
        line3.set_ydata(data['t_ext']) 
        plt.xlim([0, data["timestamp"].iloc[-1]])
        plt.draw()
        plt.pause(steptime)
        time.sleep(steptime)
except KeyboardInterrupt:  # Manejo de la interrupción del teclado para detener el experimento
    pass

# Guarda la figura del gráfico de series temporales y los datos en archivos
plt.savefig('time_series.jpg')
data.to_csv('time_series.csv')
