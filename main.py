import os
import random
import sys
import requests
from dotenv import load_dotenv
from PySide6 import QtCore, QtGui, QtWidgets

load_dotenv()

JELLYFIN_URL = os.getenv("JELLYFIN_URL")
JELLYFIN_KEY = os.getenv("JELLYFIN_KEY")
JELLYFIN_USER = os.getenv("JELLYFIN_USER")

TMDB_URL = os.getenv("TMDB_URL")
TMDB_KEY = os.getenv("TMDB_KEY")


class Randotron(QtWidgets.QMainWindow):
    def __init__(self):
        super(Randotron, self).__init__()
        self.rng_movie_title = None

        self.setWindowTitle("RANDOTRON")

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        # create widgets to add to layout
        self.button = QtWidgets.QPushButton("Randotron Activate")
        self.text = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)

        # image from url
        self.image_label = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap()

        # create layout and add widgets
        self.layout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.button)

        # set layout
        self.setLayout(self.layout)

        self.button.clicked.connect(self.randotron)

    def randotron(self):
        movie_list = []

        headers = {
            "X-Emby-Token": JELLYFIN_KEY,
            "Accept": "application/json"
        }

        url = f"{JELLYFIN_URL}/Users/{JELLYFIN_USER}/Items?IncludeItemTypes=Movie&Filters=IsUnplayed&Recursive=true&Fields=Path"

        try:
            response = requests.get(url=url, headers=headers)
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

        if movie_list is not None:
            self.tmdb_image(random.choice(movie_list))

    def tmdb_image(self, movie_title):
        tmdb_url = TMDB_URL + movie_title
        headers = {
            "authorization": "Bearer " + TMDB_KEY,
            "accept": "application/json",
        }

        try:
            response = requests.get(url=tmdb_url, headers=headers)
            response.raise_for_status()

            data = response.json()
            results = data.get("results")
            poster_path = results[0].get("poster_path")

            poster_url = f"https://image.tmdb.org/t/p/w342{poster_path}"

            self.text.setText(movie_title)

            self.pixmap.loadFromData(requests.get(poster_url).content)
            self.image_label.setPixmap(self.pixmap)
            self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        except requests.exceptions.HTTPError as err:
            print(err)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = Randotron()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
