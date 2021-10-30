from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

class Div(QLabel) :
    def __init__(self, pic):
        super(Div, self).__init__()
        self.moveNumber = 0
        self.pic = pic
        self.setAlignment(QtCore.Qt.AlignTop)

        if pic == "h":
            self.image_url = "assets/haut.png"
        elif pic == "b":
            self.image_url = "assets/bas.png"
        elif pic == "ar":
            self.image_url = "assets/arriere.png"
        elif pic == "av":
            self.image_url = "assets/avant.png"
        elif pic == "db":
            self.image_url = "assets/droitebas.png"
        elif pic == "dh":
            self.image_url = "assets/droitehaut.png"
        elif pic == "gb":
            self.image_url = "assets/gauchebas.png"
        elif pic == "gh":
            self.image_url = "assets/gauchehaut.png"
        else :
            self.image_url = "assets/red.png"

    def getImage(self):
        pixmap = QtGui.QPixmap()
        pixmap.load(self.image_url)
        pixmap = pixmap.scaledToHeight(45)
        return pixmap

    def getColor(self):
        return self.color

    def getPlayer(self):
        return self.player

    def getMoveNumber(self):
        return self.moveNumber

    def nextMove(self):
        self.moveNumber += 1
