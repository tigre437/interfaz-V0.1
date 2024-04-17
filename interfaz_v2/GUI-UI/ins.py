"""A small wrapper  / driver / to control the Lauda RP 250 E circulation thermostat
Defines a class for the instrument and stablish connection via raw TCP/IP serial 
"""

import os
import time
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from camera import Camera
from lauda import Lauda
import yaml

DATA_PATH = 'data'
IMAGE_PATH = 'images'


def setup_interactive_plot(data, steptime, title=None):
    ylim = max([data['t_set'].iloc[0], data['t_int'].iloc[0], data['t_ext'].iloc[0]])+5
    plt.ion()
    line1, = plt.plot(data["timestamp"], data['t_set'], 'k', label='t_set')
    line2, = plt.plot(data["timestamp"], data['t_int'], 'b', label='t_int')
    line3, = plt.plot(data["timestamp"], data['t_ext'], 'r', label='t_ext')
    plt.ylim([data['t_set'].iloc[-1]-10, ylim])
    plt.ylim([-3, 3])
    plt.xlabel('timestamp (s)')
    plt.ylabel('temperature (ºC)')
    plt.title(title)
    plt.legend()
    plt.pause(steptime)
    return (line1, line2, line3)


def update_plot(lines, data, steptime):
    ylim = max([data['t_set'].iloc[0], data['t_int'].iloc[0], data['t_ext'].iloc[0]])+5
    line1 = lines[0]
    line2 = lines[1]
    line3 = lines[2]
    line1.set_xdata(data["timestamp"])
    line1.set_ydata(data['t_set'])    
    line2.set_xdata(data["timestamp"])
    line2.set_ydata(data['t_int']) 
    line3.set_xdata(data["timestamp"])
    line3.set_ydata(data['t_ext'])
    plt.ylim([data["t_set"].iloc[-1]-10, ylim])
    # plt.ylim([-3, 3])
    plt.xlim([0, data["timestamp"].iloc[-1]])
    plt.draw()
    plt.pause(steptime)


class Ins():
    def __init__(self, thermostat_port=None, camera_port=None, image_shape=[1280, 960], steptime=5):
        self.thermostat = Lauda(url=thermostat_port)
        self.camera = Camera(port=camera_port, shape=image_shape)

        self.steptime = steptime
        self.experiment_name = None
        self.reference_time = None
        self.data = None
        self.pcr1 = np.array([8, 12])
        self.pcr2 = np.array([8, 12])
        self.pcr_rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.pcr_cols = list(range(1,13))
        self.circles = None

    def close(self):
        self.camera.close()
        self.thermostat.close()
    

    def setup_experiment(self, name=None):
        self.reference_time = dt.datetime.now()
        self.experiment_name = f'{self.reference_time:%y%m%d_%H%M%S}'
        if name:
            self.experiment_name += f'_{name}'

        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)
        os.mkdir(os.path.join(DATA_PATH, self.experiment_name))
        os.mkdir(os.path.join(DATA_PATH, self.experiment_name, IMAGE_PATH))
    
        return self.experiment_name


    def run_experiment(self, name):
        if not os.path.exists(os.path.join(DATA_PATH, name)):
            exit('setup the experiment before running it.')
        # if not self.camera.camera:
        #     exit('camera not connected')
        if not self.thermostat.conn:
            exit('thermostat not connected')

        self.camera.setup()
            
        # TODO: llamar a camera.detect_circles --> devuelve la lista de circulos (self.circles)
        self.circles = self.camera.detect_circles()
        # self.camera.setup()
        # self.camera.set_exposure()
        self.thermostat.start()

        timestamp = 0
        self.data = pd.DataFrame(data={'timestamp': [timestamp],
                                       't_set': [float(self.thermostat.get_t_set())],
                                       't_int': [float(self.thermostat.get_t_int())],
                                       't_ext': [float(self.thermostat.get_t_ext())]})
        lines = setup_interactive_plot(self.data, self.steptime, self.experiment_name)
        start_ramp = False
        countdown = None
        try:
            while(True):
                timestamp += self.steptime
                self.data = pd.concat([self.data, pd.DataFrame(data={'timestamp': [timestamp],
                                                                     't_set': [float(self.thermostat.get_t_set())],
                                                                     't_int': [float(self.thermostat.get_t_int())],
                                                                     't_ext':  [float(self.thermostat.get_t_ext())]})],
                                                                     ignore_index=True)
                print(f'{self.data["timestamp"].iloc[-1]}\t{self.data["t_int"].iloc[-1]}')
                update_plot(lines, self.data, self.steptime)
                self.data.to_csv(os.path.join(DATA_PATH, self.experiment_name, 'time_series.csv'))
                # self.camera.get_frame()
                # self.camera.save_frame(f'./data/{self.experiment_name}/images', dt.datetime.now(), watermark=str(self.thermostat.t_ext))
                if start_ramp and self.thermostat.t_ext < -1:
                    self.camera.get_frame()
                    self.camera.save_frame(f'./data/{self.experiment_name}/images', dt.datetime.now(), watermark=str(self.thermostat.t_ext))

                if not start_ramp:
                    if self.thermostat.t_ext < 0.1 and countdown == None:
                        countdown = 60/self.steptime
                
                    if countdown != None and countdown > 0:
                        print('---', countdown)
                        countdown -=1
                
                    if countdown != None and countdown <= 0:
                        start_ramp = True
                else:
                    if timestamp % 60 == 0:
                        self.thermostat.set_t_set(self.thermostat.t_set-1)


        except KeyboardInterrupt:
            pass

        self.thermostat.stop()

        plt.savefig(os.path.join(DATA_PATH, self.experiment_name, 'time_series.jpg'))
        # self.data.to_csv(os.path.join(DATA_PATH, self.experiment_name, 'time_series.csv'))


