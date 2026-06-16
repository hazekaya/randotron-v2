import requests
from PySide6 import QtGui, QtWidgets


def load_image(img_url, img_pixmap: QtGui.QPixmap, img_lbl: QtWidgets.QLabel):
    img_pixmap.loadFromData(requests.get(img_url).content)
    img_lbl.setPixmap(img_pixmap)