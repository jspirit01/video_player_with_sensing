import os
import time
from datetime import datetime, timedelta

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import QTimer
from const.config import *


class RecordingPageWidget(QWidget):
    def __init__(self, btf, cs, monitor):
        super().__init__()
        
        self.partc_label = QLabel('', self)
        self.game_label = QLabel('', self)
        # self.music_label = QLabel('', self)
        self.calibration_label = QLabel('', self)
        self.timer_label = QLabel('', self)

        self.cs = cs
        self.btf = btf

        self.monitor = monitor
        self.save_path = None
        self.record_start = None
        self.record_start_time = None

        self.calibrate_btn = None
        self.stop_btn = None
        self.save_btn = None
        self.start_btn = None
        self.back_btn = None

        self.recording = False

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timeout)
        self.sec_counter = 0

        self.init_ui()


    def init_ui(self):
        partc_hobx = QHBoxLayout()
        partc_hobx.addStretch(1)
        partc_hobx.addWidget(QLabel('Participant:', self))
        partc_hobx.addWidget(self.partc_label)
        partc_hobx.addStretch(1)

        game_hbox = QHBoxLayout()
        game_hbox.addStretch(1)
        game_hbox.addWidget(QLabel('Game Genre:', self))
        game_hbox.addWidget(self.game_label)
        game_hbox.addStretch(1)

        music_hbox = QHBoxLayout()
        music_hbox.addStretch(1)
        music_hbox.addWidget(QLabel('Music Genre:', self))
        music_hbox.addWidget(self.music_label)
        music_hbox.addStretch(1)

        calibrate_hbox = QHBoxLayout()
        calibrate_hbox.addStretch(1)
        calibrate_hbox.addWidget(QLabel('Calibration Result:', self))
        calibrate_hbox.addWidget(self.calibration_label)
        calibrate_hbox.addStretch(1)

        timer_hbox = QHBoxLayout()
        timer_hbox.addStretch(1)
        timer_hbox.addWidget(QLabel('Recording time:', self))
        timer_hbox.addWidget(self.timer_label)
        timer_hbox.addStretch(1)


        # 센서 중에 gaze가 있다면 recording 전 calibrate 먼저 시작
        for sensor in self.monitor.parts:
            if sensor['device'] == 'gaze':
                self.trackerObj = sensor['part']
                self.calibrate_btn = QPushButton("Start Calibrating")
                self.calibrate_btn.clicked.connect(self.start_calibrate)

        self.start_btn = QPushButton('Start record')
        self.start_btn.clicked.connect(self.start_record)        
        self.start_btn.setEnabled(False)
        self.stop_btn = QPushButton('Stop record')
        self.stop_btn.clicked.connect(self.stop_record)
        self.stop_btn.setEnabled(False)
        self.save_btn = QPushButton('Save recorded data')
        self.save_btn.clicked.connect(self.save_record)
        self.save_btn.setEnabled(False)
    
    
        self.back_btn = QPushButton('Back')
        self.back_btn.clicked.connect(self.back_to_first_page)

        btn_hbox = QHBoxLayout()
        btn_hbox.addStretch(1)
        btn_hbox.addWidget(self.calibrate_btn)
        btn_hbox.addWidget(self.start_btn)
        btn_hbox.addWidget(self.stop_btn)
        btn_hbox.addWidget(self.save_btn)
        btn_hbox.addStretch(1)

        back_hbox = QHBoxLayout()
        back_hbox.addStretch(5)
        back_hbox.addWidget(self.back_btn)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(partc_hobx)
        vbox.addLayout(game_hbox)
        vbox.addLayout(music_hbox)
        vbox.addLayout(calibrate_hbox)
        vbox.addLayout(timer_hbox)
        vbox.addStretch(3)
        vbox.addLayout(btn_hbox)
        vbox.addStretch(1)
        vbox.addLayout(back_hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

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
        print('start calibrateing')
        calibration_result = self.trackerObj.calibrate()
        if calibration_result:
            self.calibration_label.setText("Success")
            
        else: 
            self.calibration_label.setText("Fail")
            
        self.calibrate_btn.setText("Re-calibrate")
        self.back_btn.setText('back')
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        


    def start_record(self):
        print('start recording')
        self.recording = True
        self.set_record_start_time()
        self.monitor.start_record()

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

        partc = self.partc_label.text()
        if not os.path.exists(os.path.join(SAVE_PATH, partc)):
            os.mkdir(os.path.join(SAVE_PATH, partc))
        if not os.path.exists(os.path.join(SAVE_PATH, partc, self.get_save_file_name())):
            os.mkdir(os.path.join(SAVE_PATH, partc, self.get_save_file_name()))

        self.monitor.save_data(os.path.join(SAVE_PATH, partc, self.get_save_file_name()))

        self.back_btn.setText('Finish')
        self.cs.change_status.emit(f'Recorded data is saved in {os.path.join(SAVE_PATH, partc, self.get_save_file_name())}')

    def get_save_file_name(self):
        game = self.game_label.text()
        music = self.music_label.text()

        return f'{game}_{music}_{self.record_start}'

    def set_record_start_time(self):
        self.timer.start()
        self.sec_counter = 0
        self.record_start_time = time.time()
        self.record_start = datetime.now().strftime('%y%m%d_%H-%M-%S.%f')

    def timeout(self):
        self.sec_counter += 100
        self.timer_label.setText(str(timedelta(milliseconds=self.sec_counter))[:-3])

