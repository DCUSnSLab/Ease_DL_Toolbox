from PyQt5.QtWidgets import *


class UiSshConnectWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setWindowTitle('SSH connect')
        self.resize(800, 500)
        self.center()

        grid = QGridLayout()

        grid.addWidget(QLabel('Host:'), 0, 0)
        grid.addWidget(QLabel('Port:'), 1, 0)
        grid.addWidget(QLabel('Username:'), 2, 0)
        grid.addWidget(QLabel('password:'), 3, 0)

        self.ip_edit = QLineEdit(self)
        self.port_edit = QLineEdit(self)
        self.id_edit = QLineEdit(self)
        self.pw_edit = QLineEdit(self)
        self.pw_edit.setEchoMode(QLineEdit.Password)

        grid.addWidget(self.ip_edit, 0, 1)
        grid.addWidget(self.port_edit, 1, 1)
        grid.addWidget(self.id_edit, 2, 1)
        grid.addWidget(self.pw_edit, 3, 1)

        self.json_btn = QPushButton("get json file", self)
        self.connect_btn = QPushButton("connect", self)

        h_box = QHBoxLayout()
        h_box.addWidget(self.json_btn)
        h_box.addWidget(self.connect_btn)

        widget = QWidget()
        v_box = QVBoxLayout(widget)
        v_box.addLayout(grid)
        v_box.addLayout(h_box)
        self.setCentralWidget(widget)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
