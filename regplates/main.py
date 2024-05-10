import sys

from PyQt5 import QtWidgets

from .Window import Window

def main_function():
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.show()
    app.exec()

if __name__ == "__main__":
    main_function()
