from PyQt5.QtWidgets import *


class UiFileSelectWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setWindowTitle('file process')
        self.resize(800, 500)
        self.center()

        self.local_path_label = QLabel('local path', self)
        self.remote_path_label = QLabel('SSH path', self)

        self.select_local_path_btn = QPushButton("Select Local File", self)
        self.select_remote_path_btn = QPushButton("Select Remote Directory", self)
        self.upload_btn = QPushButton("Upload File", self)
        self.exit = QPushButton("Exit", self)

        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.local_path_label)
        h_box1.addWidget(self.select_local_path_btn)

        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.remote_path_label)
        h_box2.addWidget(self.select_remote_path_btn)

        v_box = QVBoxLayout()
        v_box.addLayout(h_box1)
        v_box.addLayout(h_box2)
        v_box.addWidget(self.upload_btn)
        v_box.addWidget(self.exit)

        # self.setLayout(v_box)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(v_box)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
