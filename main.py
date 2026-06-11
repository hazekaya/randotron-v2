import sys

from PySide6 import QtCore, QtGui, QtWidgets

class Randotron(QtWidgets.QMainWindow):
    def __init__(self):
        super(Randotron, self).__init__()

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        # create widgets to add to layout
        self.button = QtWidgets.QPushButton("Randotron Activate")
        self.text = QtWidgets.QLabel("RANDOTRON", alignment=QtCore.Qt.AlignCenter)

        # create layout and add widgets
        self.layout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        # set layout
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = Randotron()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())