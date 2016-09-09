import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from fs_model import CheckedFsModel


def main():
    app = QApplication(sys.argv)
    window = uic.loadUi("mainwindow.ui")

    model = CheckedFsModel()
    window.fileTreeView.setModel(model)
    model.setRootPath("C:/projects/bsysnc/testrepo/src")
    window.fileTreeView.setRootIndex(model.setRootPath("C:/projects/bsync/testrepo/src"))

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
