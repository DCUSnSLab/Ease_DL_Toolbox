import json
import os
import paramiko
from PyQt5.QtWidgets import *
from .init_UI.UI_SSH_connect import UiSshConnectWindow
from .file_select import FileSelectWindow


class SshConnectWindow(UiSshConnectWindow):
    def __init__(self):
        super().__init__()
        self.ip = ""
        self.port = ""
        self.id = ""
        self.pw = ""
        self.json_file_path = os.path.join(os.getcwd(), "ssh_init.json")
        self.initUI()
        self.connect_signals()

    def connect_signals(self):
        self.json_btn.clicked.connect(self.get_json_file)
        self.connect_btn.clicked.connect(self.ssh_connect)

    def get_json_file(self):
        if os.path.isfile(self.json_file_path):
            with open(self.json_file_path, 'r') as f:
                data = json.load(f)
                self.ip_edit.setText(data["ip"])
                self.port_edit.setText(data["port"])
                self.id_edit.setText(data["id"])
                self.pw_edit.setText(data["pw"])
        else:
            QMessageBox.critical(self, 'not found json file', 'json 파일이 없습니다.')

    def save_json(self):
        with open(self.json_file_path, 'w') as f:
            data = {'ip': self.ip, 'port': self.port, 'id': self.id, 'pw': self.pw}
            json.dump(data, f, indent=4)

    def clear_input_fields(self):
        self.ip_edit.clear()
        self.port_edit.clear()
        self.id_edit.clear()
        self.pw_edit.clear()

    def ssh_connect(self):
        self.ip = self.ip_edit.text()
        self.port = self.port_edit.text()
        self.id = self.id_edit.text()
        self.pw = self.pw_edit.text()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        try:
            ssh.connect(self.ip, port=self.port, username=self.id, password=self.pw)
        except Exception:
            QMessageBox.critical(self, 'connect error', '접속 실패\n올바른 정보를 입력하세요.')
            self.clear_input_fields()
            return

        if ssh.get_transport() is not None and ssh.get_transport().is_active():
            print("Connected successfully")
            self.save_json()
            self.hide()
            self.file_select_window = FileSelectWindow(ssh)
            self.file_select_window.show()
            # self.close()
            # ssh.close()