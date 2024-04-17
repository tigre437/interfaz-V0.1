""" Class Camera operates the camera connected via USB
The camera tested is a ELP USB8MP02G-SFV on Windows 11
"""

import os
import numpy as np
import cv2

class Camera():
    def __init__(self, port=None, shape=[1280, 960]):
        self.camera = None
        self.frame = None
        self.frame_average = None
        self.frame_median = None
        self.frame_width = shape[0]
        self.frame_height = shape[1]
        # self.frame1 = None
        # self.roi1 = roi1
        # self.frame2 = None
        # self.roi2 = roi2

        
        if port is not None:
            self.open(port)
    

    def open(self, port):
        self.camera = cv2.VideoCapture(port, cv2.CAP_DSHOW)
        if not self.camera.isOpened():
            print('camera not found')

        else:
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)       # 0 for manual mode / 1 for autoexposure mode
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)


    def close(self):
        if self.camera:
            self.camera.release()

 
    def get_frame(self):
        if self.camera.isOpened():
            result, self.frame = self.camera.read()
            self.frame_average = self.frame.mean()
            self.frame_median = np.median(self.frame)
            # self.frame1 = self.frame[self.roi1[0]:self.roi1[2],self.roi1[1]:self.roi1[3]]
            if not result:
                self.frame = None
                self.frame_average = None
    
    def save_frame(self, path, timestamp, watermark=None):
        
        file_path = os.path.join(path, f'{timestamp:%H%M%S}' + '.jpg')        

        if watermark:
            self.frame = cv2.putText(self.frame, watermark, org=(25, 25) ,fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)

        cv2.imwrite(file_path, self.frame)


    def setup(self):
        self.camera.set(cv2.CAP_PROP_SETTINGS, 1)
        while True:
            self.get_frame()
            watermark = f'AVG: {int(self.frame_average)} -- MEDIAN: {int(self.frame_median)}'
            cv2.putText(self.frame, watermark, org=(25, 25) ,fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)
            cv2.imshow('setup',self.frame)
            key = cv2.waitKeyEx(1)

            if key == 13:
                break

        cv2.destroyAllWindows()

    def showroi1(self):
        while True:
            self.get_frame()
            cv2.imshow('PCR1',self.frame1)
            key = cv2.waitKeyEx(1)

            if key == 13:
                break

        cv2.destroyAllWindows()

    def detect_circles(self):
        threshold = 127
        while True:
            self.get_frame()
            frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            # self.frame = cv2.blur(self.frame, (3, 3)) 

            _, binary = cv2.threshold(frame, threshold, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            circle_list = []
            for cnt in contours:
                approx = cv2.approxPolyDP(cnt, .03 * cv2.arcLength(cnt, True), True)
                # cv2.drawContours(self.frame, cnt, -1, (0, 0, 255), 2, cv2.LINE_AA)
                if len(approx)>=6:
                    if cv2.isContourConvex(approx):
                        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
                        if radius >=14 and radius <= 16:
                            circle_list.append([cx, cy, radius])
                            cv2.circle(self.frame, (int(cx), int(cy)), int(radius), (0, 255, 0), 2)
                            cv2.circle(self.frame, (int(cx), int(cy)), 1, (0, 0, 255), 3)

            if circle_list:
                circles = np.asarray(circle_list)
                circles = circles[np.lexsort((circles[:,1], circles[:,0]))]
                idx = 1
                for row in circles:
                    cv2.putText(self.frame, str(idx), (int(row[0]), int(row[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
                    idx += 1

            watermark = f'THRESHOLD: {threshold}'
            cv2.putText(self.frame, watermark, org=(25, 25) ,fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)
            cv2.imshow(f'circles', self.frame)

            key = cv2.waitKeyEx(1)

            if key == 2490368:      # arrow key UP
                threshold += 1
            elif key == 2621440:    # arrow key DOWN
                threshold -= 1
            if key == 13:         # ENTER
                break

        cv2.destroyAllWindows()
        # TODO: return circulos posiciones
