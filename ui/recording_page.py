import os
import cv2
import threading
from datetime import datetime, timedelta

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QUrl, QTimer

from PyQt5.QtGui import QPalette
from PyQt5.uic import loadUi
from ui.media import CMultiMedia

from ui.prompt_qt import Prompt
import time
from ui.utils import formatting_filename
import numpy as np
from const.config import *

event_dict = {
'video1': [883, 2065, 2342, 2616, 3116],
 'video2': [639, 1447, 2128, 2770, 3389],
 'video3': [632, 1220, 1522, 1759, 2616],
#  'video4': [717, 1675, 1919, 3021, 3272],
 'video5': [591, 968, 2088, 2528, 3114],
 'video6': [433, 1131, 1822, 2710],
#  'video7': [869, 1735, 2175, 3049, 3272]
}

class RecordingPageWidget(QWidget):
    def __init__(self, btf, cs, monitor):
        super().__init__()
        loadUi('ui/main_ver2.ui', self)

        # self.partc_label = QLabel('', self)
        # self.game_label = QLabel('', self)
        # self.music_label = QLabel('', self)
        # self.calibration_label = QLabel('', self)
        # self.timer_label = QLabel('', self)

        self.cs = cs
        self.btf = btf

        
        self.monitor = monitor
        

        self.record_start = None
        self.record_start_time = None
        
        self.recording = False

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timeout)
        self.sec_counter = 0




        # Multimedia Object
        self.mp = CMultiMedia(self, self.view)
        


        # video background color
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.black)
        self.view.setAutoFillBackground(True);
        self.view.setPalette(pal)

        # volume, slider
        self.vol.setRange(0, 100)
        self.vol.setValue(50)

        # play time
        self.duration = ''

        # signal
        self.calibrate_btn.hide()
        self.camview_btn.hide()
        self.start_btn.clicked.connect(self.start_record)        
        self.start_btn.setEnabled(True)
        self.stop_btn.clicked.connect(self.stop_record)
        self.stop_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_record)
        self.save_btn.setEnabled(False)
        self.back_btn.clicked.connect(self.back_to_first_page)
        
        # 센서별 필요  ui 기능 추가
        for sensor in self.monitor.parts:
            if sensor['device'] == 'gaze':
                self.trackerObj = sensor['part']
                self.calibrate_btn.clicked.connect(self.start_calibrate)
                self.calibrate_btn.show()
                # self.start_btn.setEnabled(False)
            if sensor['device'] == 'webcam':
                self.webcamObj = sensor['part']
                self.camview_btn.clicked.connect(self.webcam_preview)
                self.camview_btn.show()
        
        

        self.btn_add.clicked.connect(self.clickAdd)
        self.btn_del.clicked.connect(self.clickDel)
        self.btn_play.clicked.connect(self.clickPlay)
        self.btn_stop.clicked.connect(self.clickStop)
        self.btn_pause.clicked.connect(self.clickPause)
        self.btn_forward.clicked.connect(self.clickForward)
        self.btn_prev.clicked.connect(self.clickPrev)

        self.list.itemDoubleClicked.connect(self.dbClickList)
        self.vol.valueChanged.connect(self.volumeChanged)
        self.bar.sliderMoved.connect(self.barChanged)



        self.save_path = None
        # self.p_folder = "./participant/" + "pname "+'/'
        # if not os.path.exists(self.p_folder):
        #     os.makedirs(self.p_folder)


    def clickAdd(self):
        files, ext = QFileDialog.getOpenFileNames(self
                                                  , 'Select one or more files to open'
                                                  , ''
                                                  , 'Video (*.mp4 *.mpg *.mpeg *.avi *.wma)')
        print(files, ext)
        if files:
            cnt = len(files)
            row = self.list.count()
            for i in range(row, row + cnt):
                self.list.addItem(files[i - row])
            self.list.setCurrentRow(0)

            self.mp.addMedia(files)

            # 우선은 파일 하나만 add했을 때만 돌아감.
            
            # video_name = files[0].split('/')[-1].split('.')[0]     # video name만 추출
            self.makePromptWindow()
    
    def clickDel(self):
        # self.monitor_on = False
        # self.prompt_monitor = None
        row = self.list.currentRow()
        self.list.takeItem(row)
        self.mp.delMedia(row)

    def clickPlay(self):
        # 비디오가 변경된 경우 prompt 다시 생성
        # video_name = self.list.currentItem().text().split('/')[-1].split('.')[0]     # video name만 추출
        # print(video_name, self.prompt_win.current_video)
        # if video_name != self.prompt_win.current_video:
        #     self.makePromptWindow(video_name)

        index = self.list.currentRow()
        self.mp.playMedia(index)
        # self.monitor_on = True

    def clickStop(self):
        self.mp.stopMedia()
        # self.monitor_on = False
        # self.prompt_win.current_video = -1  # 모두 시청하거나 중단한 경우 prompt 초기화


    def clickPause(self):
        self.mp.pauseMedia()
        # self.monitor_on = False

    def clickForward(self):
        cnt = self.list.count()
        curr = self.list.currentRow()
        if curr < cnt - 1:
            self.list.setCurrentRow(curr + 1)
            self.mp.forwardMedia()
        else:
            self.list.setCurrentRow(0)
            self.mp.forwardMedia(end=True)

    def clickPrev(self):
        cnt = self.list.count()
        curr = self.list.currentRow()
        if curr == 0:
            self.list.setCurrentRow(cnt - 1)
            self.mp.prevMedia(begin=True)
        else:
            self.list.setCurrentRow(curr - 1)
            self.mp.prevMedia()

    def dbClickList(self, item):
        # # 비디오가 변경된 경우 prompt 다시 생성
        # video_name = self.list.currentItem().text().split('/')[-1].split('.')[0]     # video name만 추출
        # if video_name != self.prompt_win.current_video:
        #     self.makePromptWindow(video_name)

        row = self.list.row(item)
        self.mp.playMedia(row)
        # self.monitor_on = True

    def volumeChanged(self, vol):
        self.mp.volumeMedia(vol)

    def barChanged(self, pos):
        print(pos)
        self.mp.posMoveMedia(pos)

    def updateState(self, msg):
        self.state.setText(msg)

    def updateBar(self, duration):
        self.bar.setRange(0, duration)
        self.bar.setSingleStep(int(duration / 10))
        self.bar.setPageStep(int(duration / 10))
        self.bar.setTickInterval(int(duration / 10))
        td = timedelta(milliseconds=duration)
        stime = str(td)
        idx = stime.rfind('.')
        self.duration = stime[:idx]

    def updatePos(self, pos):
        self.bar.setValue(pos)
        td = timedelta(milliseconds=pos)
        stime = str(td)
        idx = stime.rfind('.')
        stime = f'{stime[:idx]} / {self.duration}'
        self.playtime.setText(stime)

    def makePromptWindow(self):
    #     # Prompt Object
        self.video_name = self.game_label.text()
        self.prompt_monitor = None
        self.prompt_win = Prompt(self)
        self.event_list = event_dict[self.video_name]
        print("make prompt")

        self.monitor_on = True
        self.prompt_monitor = threading.Thread(target=self.playMonitor)
        self.prompt_monitor.setDaemon(True)
        self.prompt_monitor.start()
        print("start monitoring")

    def playMonitor(self):
        event_count = 0

        while self.monitor_on:
            position = int(self.mp.player.position() / 1000)
            # print(position)
            if position in self.event_list:
                self.trackerObj.tracker.log("[SHOW PROMPT] count-%d" % event_count)
                print("[SHOW PROMPT] count - %d" % event_count)

                # remove event time at the list
                target = self.event_list.index(position)
                self.event_list[target] = 0

                # show prompt
                self.clickPause()
                r = self.prompt_win.showModal(position)
                # self.writeScore(position, value)
                # self.clickPlay()          # 여기서 하면 Timer 에러 남

                # move to next event
                event_count += 1
            
            if np.array(self.event_list).sum() ==0 :
                # 모든 prompt event가 끝나면 break
                print("There is no event. thread break")
                break


    def writeScore(self, position, value):
        self.trackerObj.tracker.log("[PROMPT ANSWER] time - %d, value - %d, %d, %d, %d"%  (position, value[0], value[1], value[2], value[3]))
        with open(os.path.join(self.save_path, 'score.txt'), 'a') as f:
            value = [str(v) for v in value]
            log = str(position) + ',' + ",".join(value) + '\n'
            f.write(log)  # [playtime_position] [user_answer]
            print("[PROMPT ANSWER] ", log)

    def back_to_first_page(self):
        if self.recording:
            reply = QMessageBox.question(
                self,
                'Confirm',
                'Recording is in progress.\n'
                'Are you sure to go back to the previous page?\n'
                'The currently recorded part is automatically saved',
            )

            if reply == QMessageBox.Yes:
                self.save_record()
                self.btf.back_to_first_page.emit()
            else:
                print('don\'t go back')
                pass

        else:
            self.btf.back_to_first_page.emit()

    def start_calibrate(self):
        self.recording = True
        
        # start calibrating 
        print('start calibrating')
        calibration_result = self.trackerObj.calibrate(self.save_path)

        if calibration_result:
            self.calibration_label.setText("Success")
            self.calibration_label.setStyleSheet('color: green;')
            
        else: 
            self.calibration_label.setText("Fail")
            self.calibration_label.setStyleSheet('color: red;')
            
        self.calibrate_btn.setText("Re-calibrate")
        self.back_btn.setText('back')
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        

        self.recording = True

    def start_record(self):
        print('start recording')
        self.recording = True
        self.start_timer()
        # self.set_record_start_time()
        self.monitor.start_record(self.save_path)

        self.back_btn.setText('back')
        self.calibrate_btn.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.save_btn.setEnabled(False)
        

        self.cs.change_status.emit('Recording ...')

    def stop_record(self):
        print('stop recording')
        self.timer.stop()
        self.recording = False
        self.monitor.stop_record()
        self.calibrate_btn.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.save_btn.setEnabled(True)
        

        self.cs.change_status.emit('Recording stopped')

    def save_record(self):
        print('save recording')
        if self.recording:
            self.stop_record()

        # recorded_save_path = self.create_save_path()
        # partc = self.partc_label.text()
        # if not os.path.exists(os.path.join(SAVE_PATH, partc)):
        #     os.mkdir(os.path.join(SAVE_PATH, partc))
        # if not os.path.exists(os.path.join(SAVE_PATH, partc, self.get_save_file_name())):
        #     os.mkdir(os.path.join(SAVE_PATH, partc, self.get_save_file_name()))
        try:
            self.monitor.save_data(self.save_path)
        except TypeError:
            print("Screen recording time is zero. It will be not saved.")
        

        self.back_btn.setText('Finish')
        self.cs.change_status.emit(f'Recorded data is saved in {self.save_path}')

    def create_save_path(self):
        self.set_record_start_time()
        # file formatting : pname/videoname_yymmdd_hh-mm-ss
        partc = self.partc_label.text()
        if not os.path.exists(os.path.join(SAVE_PATH, partc)):
            os.mkdir(os.path.join(SAVE_PATH, partc))
        if not os.path.exists(os.path.join(SAVE_PATH, partc, self.get_save_file_name())):
            os.mkdir(os.path.join(SAVE_PATH, partc, self.get_save_file_name()))

        self.save_path = os.path.join(SAVE_PATH, partc, self.get_save_file_name())
        print(self.save_path)
        # return self.save_path

    def set_record_start_time(self):
        # self.timer.start()
        # self.sec_counter = 0

        if self.record_start == None:
            self.record_start_time = time.time()
            self.record_start = datetime.now().strftime('%y%m%d_%H-%M-%S')  #미프
            # self.record_start = datetime.now().strftime('%y%m%d_%H-%M-%S.%f') #통합툴

    def get_save_file_name(self):
        game = self.game_label.text()
        # music = self.music_label.text()

        # return f'{game}_{music}_{self.record_start}'
        return f'{game}_{self.record_start}'

   

    def start_timer(self):
        self.timer.start()
        self.sec_counter = 0

    def timeout(self):
        self.sec_counter += 100
        self.timer_label.setText(str(timedelta(milliseconds=self.sec_counter))[:-3])


    def webcam_preview(self):
        # toggle
        if self.webcamObj._video_recorder.isPreview:
            print("WEBCAM OFF")
            self.camview_btn.setText("cam preview on")

            self.webcamObj._video_recorder.isPreview = False
            # cv2.destroyAllWindows()
            # cv2.destroyWindow("webcam")
        else:
            print("WEBCAM ON")
            self.camview_btn.setText("cam preview off")
            self.webcamObj._video_recorder.isPreview = True