import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMainWindow, QApplication, QStackedWidget, QVBoxLayout

from ui.first_page import FirstPageWidget
from ui.recording_page import RecordingPageWidget
from ui.connection_status_widget import ConnectionStatusWidget
from ui.custom_signals import GoToRecordingPage, BackToFirstPage, ChangeStatus
from core.monitor import Monitor


class UIWindow(QMainWindow):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

        # 사용자 정의 시그널 연결 (특정 이벤트 발생 시 해당 시그널 방출되도록 할 수 있음)
        self.gtr = GoToRecordingPage()
        self.gtr.go_to_record_page.connect(self.go_recording)
        self.btf = BackToFirstPage()
        self.btf.back_to_first_page.connect(self.back_first_page)
        self.cs = ChangeStatus()
        self.cs.change_status.connect(self.change_status)
        
        # 위젯 정의
        _widget = QWidget()
        vbox = QVBoxLayout(_widget)
        self.connection_widget = ConnectionStatusWidget(monitor)
        self.widgets = QStackedWidget()
        self.first_page = FirstPageWidget(self.gtr, self.cs, monitor)
        self.recording_page = RecordingPageWidget(self.btf, self.cs, monitor)
        self.widgets.addWidget(self.first_page)
        self.widgets.addWidget(self.recording_page)
        vbox.addWidget(self.connection_widget)
        vbox.addWidget(self.widgets)

        self.setLayout(vbox)
        self.setCentralWidget(_widget)
        self.change_status('Set experiment information')

        self.setWindowTitle("sensor signal collector")
        self.resize(400, 400)
        self._center()
        self.show()

    def change_status(self, status_msg):
        self.statusBar().showMessage(status_msg)

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def go_recording(self):
        self.recording_page.partc_label.setText(self.first_page.partc_line.text())
        self.recording_page.game_label.setText(self.first_page.game_cb.currentText())
        # self.recording_page.music_label.setText(self.first_page.music_cb.currentText())
        # self.recording_page.start_record()

        self.recording_page.create_save_path()

        self.widgets.setCurrentIndex(self.widgets.currentIndex() + 1)

    def back_first_page(self):
        self.first_page.partc_line.setText('')
        self.first_page.game_cb.setCurrentIndex(0)
        # self.first_page.music_cb.setCurrentIndex(0)
        self.widgets.setCurrentIndex(self.widgets.currentIndex() - 1)
        self.change_status('Set experiment information')


if __name__ == '__main__':
    monitor = Monitor()
    # gsr = GSR('CD36CD')
    # eeg = EEG()
    # webcam = WebcamRecorder(camera_index=0)
    # screen = ScreenRecorder(monitor_num=1, left=0, top=0, width=3840, height=2160)

    print('Instances are generated')

    # monitor.add_padded')
    # monitor.add_part(eeg)
    # print('eeg is added')
    # monitor.add_part(webcam)
    # print('webcam is added')
    # monitor.add_part(screen)
    # print('screen is added')

    monitor.ready_parts()
    monitor.stream()
    app = QApplication(sys.argv)
    ui = UIWindow(monitor)
    sys.exit(app.exec_())
