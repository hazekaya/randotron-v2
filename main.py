import random
import sys
import urllib

import requests
from PySide6 import QtCore, QtGui, QtWidgets

JELLYFIN_KEY = "e9e4559fe74a4466b197b0955355cf67"
JELLYFIN_URL = "http://192.168.0.253:8096"
JELLYFIN_USER = "aa01a24ed1344f6993d1176fff245d14"
API_URL = f"{JELLYFIN_URL}/Users/{JELLYFIN_USER}/Items?IncludeItemTypes=Movie&Filters=IsUnplayed&Recursive=true&Fields=Path"
HEADERS = {
    "X-Emby-Token": JELLYFIN_KEY,
    "Accept": "application/json"
}

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

        self.button.clicked.connect(self.randotron)

    def randotron(self):
        movie_list = []
        print(API_URL)

        try:
            response = requests.get(url=API_URL, headers=HEADERS)
            response.raise_for_status()

            data = response.json()
            movies = data.get("Items", [])

            if movies is not None:
                for movie in movies:
                    title = movie.get("Name")

                    # print(movie)
                    movie_list.append(title)

        except requests.exceptions.HTTPError as err:
            print(err)

        print(random.choice(movie_list))



if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = Randotron()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())