import subprocess
from subprocess import PIPE
import os
from const.config import *
from datetime import datetime, timedelta

import pandas as pd
import ctypes


class ScreenRecorder:
    def __init__(self):
        self.proc = None
        self.recording = False

    def ready(self):
        pass

    def stream(self):
        while True:
            pass

    def record(self, save_path):
        self.recording = True

        if self.recording:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            self.start_time = datetime.utcnow() + timedelta(hours=9)

            save_path = save_path.replace('\\','/')
            start_time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")\
                                .replace('/', '')\
                                .replace(',', '_')\
                                .replace(' ', '')\
                                .replace(':', '')
            self.proc = subprocess.Popen(args=['ffmpeg', '-f', 'dshow', '-y', '-rtbufsize', '100M', "-f", 'gdigrab', '-framerate', '30',
                      '-probesize', '10M', '-draw_mouse', '1', '-offset_x', '0', '-offset_y',
                      '0', '-itsoffset', '1', '-i', 'desktop',
                      '-c:v', 'libx264', '-r', '30', '-preset', 'ultrafast', '-tune',
                      'zerolatency', '-crf', '25', '-pix_fmt', 'yuv420p', save_path + '/' + str(start_time) + '_screen.mp4',
                      ], startupinfo=startupinfo, stdin=PIPE, shell=False)

            

    def stop_record(self):
        self.recording = False
        _, _ = self.proc.communicate(input=b'q')

        self.end_time = datetime.utcnow() + timedelta(hours=9)

    def save_data(self, save_path):
        print("Saving screen")
        df = pd.DataFrame()
        df['time'] = pd.date_range(start = self.start_time, end = self.end_time, freq='0.033333S')

        df.to_csv(save_path + "/screen_timetable.csv", index=False)

        print("Screen is saved")
    def terminate(self):
        print('terminating screen')
        print('screen is terminated')

    def clear(self):
        pass