import time
import os
import json

parar = False
class LaudaSimulado:
    def __init__(self):
        self.t_int = 25  # Temperatura interna inicial

    def get_t_int(self):
        return self.t_int

    def set_t_set(self, temperatura):
        print(f"Cambiando la temperatura objetivo a: {temperatura}°C")
        # Simulamos el cambio de temperatura objetivo
        self.t_int = temperatura

class TuClase:
    def __init__(self):
        self.txtArchivos = "ruta/a/tus/archivos"
        self.comboBoxFiltro = "filtro"
        self.lauda = LaudaSimulado()

    def leer_json_camara(self, ruta):
        # Simulamos leer el archivo JSON de la cámara
        with open(ruta, 'r') as file:
            return json.load(file)

    def rampa_temperatura(self, objetivo):
       # datos_camara = self.leer_json_camara(
       #     os.path.join(self.txtArchivos, self.comboBoxFiltro, "camera.json")
       # )
        while not parar:
            if self.lauda.get_t_int() > objetivo:
                self.lauda.set_t_set(self.lauda.get_t_int() - 1)
            time.sleep(1)  # Simulamos esperar un segundo

# Crear una instancia de TuClase y probar la función rampa_temperatura
tu_instancia = TuClase()
tu_instancia.rampa_temperatura(20)  # Ejemplo: bajar la temperatura a 20°C
