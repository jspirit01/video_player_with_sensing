import sys
import time

from core.monitor import Monitor
from parts.camthread import CamThread
from parts.gsr import GSR
from parts.eeg import EEG
from parts.gaze import Gaze
from parts.camera_b import WebcamRecorder
from parts.audio import Audio
# from parts.camera import Webcam
from parts.screen_recorder import ScreenRecorder    # csv
from parts.e4 import E4
# from parts.screen import ScreenRecorder

from PyQt5.QtWidgets import QApplication
from ui.ui_window import UIWindow

def main():

    monitor = Monitor()
    # gsr = GSR('A023A8')
    # eeg = EEG()
    gaze = Gaze()
    # e4 = E4()
    webcam = WebcamRecorder(camera_index=0)
    # screen = ScreenRecorder(monitor_num=0, left=0, top=0, width=3840, height=1080)
    # screen = ScreenRecorder(monitor_num=1, left=0, top=0, width=3840, height=2160)
    screen = ScreenRecorder()
    audio = Audio()

    print('Instances are generated')

    # monitor.add_pasdfasdfsadfart(eeg, 'eeg')
    # print('eeg is added')
    # monitor.add_part(gsr, 'gsr')
    # print('gsr is added')

    # monitor.add_part(e4, 'e4')
    # print('e4 is added')
    monitor.add_part(gaze, 'gaze')
    print('eyetracker is added')
    monitor.add_part(screen, 'screen')      
    print('screen is added')
    # monitor.add_part(webcam, 'webcam')
    # print('webcam is added')
    monitor.add_part(audio, 'audio')
    print('audio is added')
    
    ############################################################################################ 정리하기
    thread1 = CamThread("WebCam", 0)
    thread1.start()
    ############################################################################################

    monitor.ready_parts()
    time.sleep(1)
    monitor.stream()

    ui = QApplication(sys.argv)
    ex = UIWindow(monitor)
    sys.exit(ui.exec_())

if __name__ == '__main__':
    main()
