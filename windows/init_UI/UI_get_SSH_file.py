from PyQt5.QtWidgets import *


class UiGetSshFileWindow(QDialog):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setWindowTitle('File select on SSH')
        self.resize(600, 400)
        self.center()

        v_box = QVBoxLayout()
        h_box1 = QHBoxLayout()
        h_box2 = QHBoxLayout()

        self.back_btn = QPushButton('↑')
        self.remote_path_edit = QLineEdit()

        h_box1.addWidget(self.back_btn)
        h_box1.addWidget(self.remote_path_edit)

        self.file_list = QListWidget()

        self.cancel_btn = QPushButton('Cancel')
        self.open_btn = QPushButton('Open')

        h_box2.addWidget(self.cancel_btn)
        h_box2.addWidget(self.open_btn)

        v_box.addLayout(h_box1)
        v_box.addWidget(self.file_list)
        v_box.addLayout(h_box2)

        self.setLayout(v_box)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
