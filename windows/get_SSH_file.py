import stat
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QBrush
from .init_UI.UI_get_SSH_file import UiGetSshFileWindow


class GetSshFileWindow(UiGetSshFileWindow):
    def __init__(self, ssh_client, remote_path):
        super().__init__()
        self.initUI()

        self.current_remote_path = remote_path
        self.remote_path = remote_path
        self.sftp = ssh_client.open_sftp()

        self.connect_signals()
        self.populate_remote_files()

    def connect_signals(self):
        self.remote_path_edit.setText(self.current_remote_path)
        self.file_list.itemClicked.connect(self.item_clicked)
        self.file_list.itemDoubleClicked.connect(self.item_double_clicked)
        self.back_btn.clicked.connect(self.go_up_one_level)
        self.open_btn.clicked.connect(self.ssh_path_open)
        self.cancel_btn.clicked.connect(self.close_window)

    def item_clicked(self, item):
        selected_item = item.text()

        if selected_item == '..':
            new_path = '/'.join(self.current_remote_path.split('/')[:-1])
        elif selected_item == '.':
            new_path = f"{self.current_remote_path}"
        else:
            new_path = f"{self.current_remote_path}/{selected_item}"

        self.remote_path_edit.setText(new_path)

    def item_double_clicked(self, item):
        selected_item = item.text()

        if selected_item == '..':
            new_path = '/'.join(self.current_remote_path.split('/')[:-1])
            self.remote_path_edit.setText(new_path)
            self.update_remote_files()
        elif selected_item == '.':
            new_path = f"{self.current_remote_path}"
            self.remote_path_edit.setText(new_path)
            # self.update_remote_files()
        else:
            new_path = f"{self.current_remote_path}/{selected_item}"
            file_attr = self.sftp.stat(new_path)
            if stat.S_ISDIR(file_attr.st_mode):
                self.remote_path_edit.setText(new_path)
                self.update_remote_files()

    def go_up_one_level(self):
        new_path = '/'.join(self.current_remote_path.split('/')[:-1])
        self.remote_path_edit.setText(new_path)
        self.update_remote_files()

    def update_remote_files(self):
        new_path = self.remote_path_edit.text()
        if new_path:
            self.current_remote_path = new_path
            self.populate_remote_files()

    def populate_remote_files(self):
        remote_files = self.sftp.listdir_attr(self.current_remote_path)

        self.file_list.clear()
        self.file_list.addItem('..')
        self.file_list.addItem('.')

        for file_attr in remote_files:
            if stat.S_ISDIR(file_attr.st_mode):
                item = QListWidgetItem(file_attr.filename)
                item.setForeground(QBrush(QColor(0, 0, 255)))
            else:
                item = QListWidgetItem(file_attr.filename)
                item.setForeground(QBrush(QColor(0, 0, 0)))
            self.file_list.addItem(item)

    def ssh_path_open(self):
        self.remote_path = self.remote_path_edit.text()

        try:
            file_attr = self.sftp.stat(self.remote_path)
            if stat.S_ISDIR(file_attr.st_mode):
                self.close()
            else:
                QMessageBox.critical(self, 'Invalid Path', 'Selected path is not a directory.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Error: {e}")
        finally:
            self.sftp.close()

    def close_window(self):
        self.remote_path = ""
        self.sftp.close()
        self.close()
