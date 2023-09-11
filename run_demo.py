import sys
from PyQt5.QtWidgets import *
from windows.SSH_connect import SshConnectWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SshConnectWindow()
    main_window.show()
    sys.exit(app.exec_())