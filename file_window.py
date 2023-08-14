import sys
import os
from PyQt5.QtWidgets import *
import paramiko
import json


class file_window(QDialog, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('file process')
        self.resize(600, 400)
        self.center()

        self.select_file_btn = QPushButton("Select Local File", self)
        self.select_file_btn.clicked.connect(self.select_local_file)

        self.select_ssh_path_btn = QPushButton("Select Remote Directory", self)
        self.select_ssh_path_btn.clicked.connect(self.select_ssh_directory)

        self.upload_btn = QPushButton("Upload File", self)
        self.upload_btn.clicked.connect(self.upload_file)

        self.exit = QPushButton("Exit", self)
        self.exit.clicked.connect(self.home)

        layout = QVBoxLayout()
        layout.addWidget(self.select_file_btn)
        layout.addWidget(self.select_ssh_path_btn)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.exit)
        self.setLayout(layout)

        self.local_file_path = ""
        self.remote_path = ""

    def home(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def select_local_file(self):
        self.local_file_path, _ = QFileDialog.getOpenFileName(self, "Select a File to Upload", "/", "All Files (*)")

    def select_ssh_directory(self):
        path = os.getcwd()
        json_file = os.path.join(path, "ssh_init.json")
        if os.path.isfile(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
                ip = data["ip"]
                port = data["port"]
                id = data["id"]
                pw = data["pw"]

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(ip, port=port, username=id, password=pw)
            stdin, stdout, stderr = ssh.exec_command('pwd')
            output = ''.join(stdout.readlines()).strip()
            print(output)

        self.remote_path = QFileDialog.getExistingDirectory(self, "Select Remote Directory Path", "/")

    def upload_file(self):
        if not self.local_file_path:
            QMessageBox.critical(self, 'Upload Error', 'No local file selected.')
            return

        if not self.remote_path:
            QMessageBox.critical(self, 'Upload Error', 'No remote directory selected.')
            return

        print("Local File Path:", self.local_file_path)
        print("Remote Directory Path:", self.remote_path)

        # Connect to the remote server using SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        path = os.getcwd()
        json_file = os.path.join(path, "ssh_init.json")
        if os.path.isfile(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
                ip = data["ip"]
                port = data["port"]
                id = data["id"]
                pw = data["pw"]

        try:
            ssh.connect(ip, port=port, username=id, password=pw)  # Use values from JSON or user input
        except Exception as e:
            QMessageBox.critical(self, 'SSH Connection Error', f"Error: {e}")
            return

        try:
            sftp = ssh.open_sftp()
            remote_file_path = os.path.join(self.remote_path, os.path.basename(self.local_file_path))

            if not os.path.exists(self.local_file_path):
                QMessageBox.critical(self, 'Upload Error', f"Local file does not exist: {self.local_file_path}")
            else:
                sftp.put(self.local_file_path, remote_file_path)
                sftp.close()
                QMessageBox.information(self, 'Upload Complete', 'File uploaded successfully.')
        except Exception as e:
            QMessageBox.critical(self, 'Upload Error', f"Error: {e}")
        finally:
            ssh.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = file_window()
    ex.show()
    sys.exit(app.exec_())
