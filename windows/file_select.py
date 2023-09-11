import os
from PyQt5.QtWidgets import *
from .init_UI.UI_file_select import UiFileSelectWindow
from .get_SSH_file import GetSshFileWindow


class FileSelectWindow(UiFileSelectWindow):
    def __init__(self, ssh_client):
        super().__init__()
        self.initUI()

        self.upload_btn.setDisabled(True)
        self.local_path = ""
        self.remote_path = "."
        self.json_file_path = os.path.join(os.getcwd(), "ssh_init.json")
        self.ssh = ssh_client
        self.sftp = self.ssh.open_sftp()

        self.connect_signals()
        self.activate_upload_btn()

    def connect_signals(self):
        self.select_local_path_btn.clicked.connect(self.select_local_path)
        self.select_remote_path_btn.clicked.connect(self.select_remote_path)
        self.upload_btn.clicked.connect(self.upload_file)
        self.exit.clicked.connect(self.close)

    def activate_upload_btn(self):
        self.upload_btn.setEnabled(bool(self.local_path) and self.remote_path != ".")

    def select_local_path(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a File to Upload", "/", "All Files (*)")
        if not file_name == "":
            self.local_path = file_name
            self.local_path_label.setText(self.local_path)
            self.activate_upload_btn()

    def select_remote_path(self):
        self.dialog = GetSshFileWindow(self.ssh, self.remote_path)
        self.dialog.exec()
        if not self.dialog.remote_path == "":
            self.remote_path = self.dialog.remote_path
            self.remote_path_label.setText(self.remote_path)
            self.activate_upload_btn()

    def upload_file(self):
        hostname = self.ssh.get_transport().sock.getpeername()
        upload_path = f"{self.remote_path}/{os.path.basename(self.local_path)}"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setWindowTitle("Upload File Message")
        msgBox.setText(f"check the host and path\t\t\t\t\nhost : {hostname[0]}:{hostname[1]}\npath : {upload_path}")
        msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        retval = msgBox.exec_()

        if retval == QMessageBox.Ok:
            self.sftp.put(self.local_path, upload_path)



