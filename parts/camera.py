from base64 import encode
import os
import shlex
import shutil

import cv2
import numpy as np
import pandas as pd

import time
from datetime import datetime, timedelta
from const.config import *
import threading

import subprocess
from subprocess import PIPE

# IMPORTANT: windows는 https://www.wikihow.com/Install-FFmpeg-on-Windows따라 ffmpeg프로그램 설치
# IMPORTANT: ubuntu 는 apt-get install ffmpeg
import ffmpeg

from PyQt5.QtCore import pyqtSignal, QObject


class Webcam:
    def __init__(self, camera_index=0):
        self.proc = None
        self.recording = False
        
    def ready(self):
        pass
    def stream(self):
        print("Start Webcam Streaming")
        while True:
            pass

        
    def record(self, save_path):
        self.recording = True
        print(save_path)
        if self.recording:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            self.start_time = datetime.utcnow() + timedelta(hours=9)
            start_time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")\
                                .replace('/', '')\
                                .replace(',', '_')\
                                .replace(' ', '')\
                                .replace(':', '')
            save_path = save_path.replace('\\','/')
            # self.proc = subprocess.Popen(args=[
            #     'ffmpeg,' '-f', 'dshow', '-y', '-rtbufsize', '100M', '-framerate', '30',
            #     '-probesize', '10M', '-i', 'video="JOYTRON HD20"', '-c:v', 'libx264', '-r', '30', '-preset', 'ultrafast', 
            #     '-tune', 'zerolatency', '-crf', '25', '-pix_fmt', 'yuv420p', SAVE_PATH + '/' + 'output2.mp4'
            #     ], startupinfo=startupinfo, stdout=PIPE, shell=False)
            self.proc = subprocess.Popen(shlex.split('ffmpeg -f dshow -y -rtbufsize 100M -framerate 30 -probesize 10M -i video="JOYTRON HD20" -c:v libx264 -r 30 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p ' + save_path +'/' + 'webcam.mp4'),
            stdin=subprocess.PIPE, shell=False)

    def stop_record(self):
        self.recording = False
        _, _ = self.proc.communicate(input=b'q')

        self.end_time = datetime.utcnow() + timedelta(hours=9)
    

    def save_data(self, save_path):
        print("Saving camera")
        df = pd.DataFrame()
        df['time'] = pd.date_range(start = self.start_time, end = self.end_time, freq='0.033333S')

        df.to_csv(save_path + "/webcam_timetable.csv", index=False)

        print("Camera is saved")
        self.clear()

    def terminate(self):
        print('terminating camera')
        print('camera is terminated')

    def clear(self):
        pass