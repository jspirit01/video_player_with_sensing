from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QDesktopWidget, QRadioButton, \
    QLabel, QButtonGroup



class Prompt(QDialog):
    def __init__(self, master):
        super().__init__()
        self.master = master
        # self.save_path = save_path

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Post Annotation Prompt')
        monitor = QDesktopWidget().screenGeometry(1)
        self.move(monitor.left(), monitor.top())
        self.setGeometry(100, 100, 700, 500)

        # label + radio button layout
        layout = QVBoxLayout()
        label1 = QLabel('강의는 당신의 집중력을 얼마나 붙잡고 있었나요?')
        label2 = QLabel('강의를 시청하는 동안 바깥 현실 세계를 의식했나요?')
        label3 = QLabel('강의의 개념과 주제에 대해 얼마나 쉽게 이해했나요?')
        label4 = QLabel('당신의 감각이 현실세계 보다 강의 속 환경에 있다고 느끼는 정도는?')
        radio_layout1 = QHBoxLayout()
        radio_layout2 = QHBoxLayout()
        radio_layout3 = QHBoxLayout()
        radio_layout4 = QHBoxLayout()
        
        self.rbtn_list1 = [QRadioButton('1', self), QRadioButton('2', self), QRadioButton('3', self),
                     QRadioButton('4', self), QRadioButton('5', self), QRadioButton('6', self),
                     QRadioButton('7', self)]
        
        self.rbtn_list2 = [QRadioButton('1', self), QRadioButton('2', self), QRadioButton('3', self),
                     QRadioButton('4', self), QRadioButton('5', self), QRadioButton('6', self),
                     QRadioButton('7', self)]
        self.rbtn_list3 = [QRadioButton('1', self), QRadioButton('2', self), QRadioButton('3', self),
                    QRadioButton('4', self), QRadioButton('5', self), QRadioButton('6', self),
                    QRadioButton('7', self)]
        self.rbtn_list4 = [QRadioButton('1', self), QRadioButton('2', self), QRadioButton('3', self),
                    QRadioButton('4', self), QRadioButton('5', self), QRadioButton('6', self),
                    QRadioButton('7', self)]
        
        self.mood_button_group1 = QButtonGroup()
        self.mood_button_group2 = QButtonGroup()  
        self.mood_button_group3 = QButtonGroup()
        self.mood_button_group4 = QButtonGroup()
        
        
        for i, rbtn in enumerate(self.rbtn_list1, 1):
            radio_layout1.addWidget(rbtn)
            self.mood_button_group1.addButton(rbtn, i)
            
        for i, rbtn in enumerate(self.rbtn_list2, 1):
            radio_layout2.addWidget(rbtn)
            self.mood_button_group2.addButton(rbtn, i)
            
        for i, rbtn in enumerate(self.rbtn_list3, 1):
            radio_layout3.addWidget(rbtn)
            self.mood_button_group3.addButton(rbtn, i)
            
        for i, rbtn in enumerate(self.rbtn_list4, 1):
            radio_layout4.addWidget(rbtn)
            self.mood_button_group4.addButton(rbtn, i)


        # OK button layout
        button_layout = QHBoxLayout()
        btnOK = QPushButton("확인")
        btnOK.clicked.connect(self.onOKButtonClicked)

        # arrange layouts
        button_layout.addStretch(1)
        button_layout.addWidget(btnOK)
        button_layout.addStretch(1)

        layout.addWidget(label1)
        layout.addStretch(1)
        layout.addLayout(radio_layout1)
        layout.addStretch(1)
        
        layout.addWidget(label2)
        layout.addStretch(1)
        layout.addLayout(radio_layout2)
        layout.addStretch(1)
        
        layout.addWidget(label3)
        layout.addStretch(1)
        layout.addLayout(radio_layout3)
        layout.addStretch(1)
        
        layout.addWidget(label4)
        layout.addStretch(1)
        layout.addLayout(radio_layout4)
        layout.addStretch(1)
        
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def radio_button_clicked(self):
        return [self.mood_button_group1.checkedId(), self.mood_button_group2.checkedId(), self.mood_button_group3.checkedId(), self.mood_button_group4.checkedId()]

    def onOKButtonClicked(self):

        values = self.radio_button_clicked()
        
        if -1 in values:
            print("점수 매기지 않고 확인 누름.")
        else:
            
            self.master.writeScore(self.playtime, values)
            self.master.clickPlay()

            self.accept()
            self.resetRadioButtons(values)

    def resetRadioButtons(self, values):
        radio_value1, radio_value2, radio_value3, radio_value4 = values
        self.mood_button_group1.setExclusive(False)
        self.mood_button_group2.setExclusive(False)
        self.mood_button_group3.setExclusive(False)
        self.mood_button_group4.setExclusive(False)

        self.rbtn_list1[radio_value1-1].setChecked(False)
        self.rbtn_list2[radio_value2-1].setChecked(False)
        self.rbtn_list3[radio_value3-1].setChecked(False)
        self.rbtn_list4[radio_value4-1].setChecked(False)
        
        self.mood_button_group1.setExclusive(True)
        self.mood_button_group2.setExclusive(True)
        self.mood_button_group3.setExclusive(True)
        self.mood_button_group4.setExclusive(True)

    def onCancelButtonClicked(self):
        # Not use here
        self.reject()

    def showModal(self, playtime):
        self.playtime = playtime
        return super().exec_()
