from PyQt5 import QtGui


class Piece:
    def __init__(self, player, color):
        self.moveNumber = 0
        self.color = color
        self.player = player

        if color == "green":
            self.image_url = "assets/CV.png"
        else:
            self.image_url = "assets/CBl.png"

    def getImage(self):
        pixmap = QtGui.QPixmap()
        pixmap.load(self.image_url)
        pixmap = pixmap.scaledToHeight(50) #
        return pixmap

    def getColor(self):
        return self.color

    def getPlayer(self):
        return self.player

    def getMoveNumber(self):
        return self.moveNumber

    def nextMove(self):
        self.moveNumber += 1
