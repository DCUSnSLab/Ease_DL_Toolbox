import sys
import json
import os
from PyQt5.QtWidgets import *
import paramiko
from file_window import file_window


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ip = ""
        self.port = ""
        self.id = ""
        self.pw = ""
        self.initUI()
        self.get_json()


    def initUI(self):
        self.setWindowTitle('SSH connect')
        self.resize(600, 400)
        self.center()
        self.get_json()

        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('Host:'), 0, 0)
        grid.addWidget(QLabel('Port:'), 1, 0)
        grid.addWidget(QLabel('Username:'), 2, 0)
        grid.addWidget(QLabel('password:'), 3, 0)

        self.IP = QLineEdit(self.ip, self)
        self.PORT = QLineEdit(self.port, self)
        self.ID = QLineEdit(self.id, self)
        self.PW = QLineEdit(self.pw, self)

        grid.addWidget(self.IP, 0, 1)
        grid.addWidget(self.PORT, 1, 1)
        grid.addWidget(self.ID, 2, 1)
        grid.addWidget(self.PW, 3, 1)

        self.connect_btn = QPushButton("connect", self)
        self.connect_btn.clicked.connect(self.connect_event)
        self.json_btn = QPushButton("get json file", self)
        self.json_btn.clicked.connect(self.json_event)

        h_box = QHBoxLayout()
        h_box.addWidget(self.json_btn)
        h_box.addWidget(self.connect_btn)

        widget = QWidget()
        v_box = QVBoxLayout(widget)
        v_box.addLayout(grid)
        v_box.addLayout(h_box)
        self.setCentralWidget(widget)

        self.show()

    def get_json(self):
        path = os.getcwd()
        json_file = os.path.join(path, "ssh_init.json")
        if os.path.isfile(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
                self.ip = data["ip"]
                self.port = data["port"]
                self.id = data["id"]
                self.pw = data["pw"]
        else:
            self.ip = ""
            self.port = ""
            self.id = ""
            self.pw = ""

    def write_json(self):
        path = os.getcwd()
        json_file = os.path.join(path, "ssh_init.json")
        with open(json_file, 'w') as f:
            data = {'ip': self.ip, 'port': self.port, 'id': self.id, 'pw': self.pw}
            json.dump(data, f, indent=4)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clear_input_fields(self):
        self.IP.clear()
        self.PORT.clear()
        self.ID.clear()
        self.PW.clear()

    def json_event(self):
        path = os.getcwd()
        json_file = os.path.join(path, "ssh_init.json")
        if os.path.isfile(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
                self.IP.setText(data["ip"])
                self.PORT.setText(data["port"])
                self.ID.setText(data["id"])
                self.PW.setText(data["pw"])
        else:
            QMessageBox.critical(self, 'not found json file', 'json 파일이 없습니다.')

    def connect_event(self):
        self.ip = self.IP.text()
        self.port = self.PORT.text()
        self.id = self.ID.text()
        self.pw = self.PW.text()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        try:
            ssh.connect(self.ip, port=self.port, username=self.id, password=self.pw)
        except Exception:
            QMessageBox.critical(self, 'connect error', '접속 실패\n올바른 정보를 입력하세요.')
            self.clear_input_fields()

        if ssh.get_transport() is not None and ssh.get_transport().is_active():
            print("Connected successfully")
            self.write_json()
            self.hide()
            self.file_dialog = file_window()
            self.file_dialog.exec()
            self.show()

        ssh.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_window()
    sys.exit(app.exec_())
