from PyQt5.QtWidgets import *
from PyQt5 import *

from gui.piece import Piece
from gui.square import Square
from gui.div import Div
from core import Board
from core import Color


class BoardGUI(QWidget):
    def __init__(self, shape, current_player=-1, parent=None):
        super(BoardGUI, self).__init__(parent)
        self.current_player = current_player
        self.color = ["white", "green"]
        self.score = {-1: 0, 1: 0}
        self.shape = shape
        self.setFixedSize(100 * shape[1], 100 * shape[0])
        self.squares = list()
        self._board = Board(shape)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        for i in range(shape[0]):
            temp = list()
            for j in range(shape[1]):
                square = Square(i, j)
                grid_layout.addWidget(square, shape[0] - i, j)
                temp.append(square)
            self.squares.append(temp)
        self.set_default_colors()
        self.setLayout(grid_layout)

    def get_board_state(self):
        return self._board

    def init_board(self, players):
        player1, player2 = -1, 1
        for x in range(self.shape[0]):
            if x < self.shape[0]-3:
                for y in range(self.shape[1]):
                    self.squares[x][y].set_piece(Piece(player1, Color(player1).name))
                    self._board.fill_cell((x, y), players[-1].color)
            elif x > self.shape[0]-3:
                for y in range(self.shape[1]):
                    self.squares[x][y].set_piece(Piece(player2, Color(player2).name))
                    self._board.fill_cell((x, y), players[1].color)
            elif x == self.shape[0]-3:
                for y in range(self.shape[1]):
                    if y in [0,2,5,7]:
                        self.squares[x][y].set_piece(Piece(player1, Color(player1).name))
                        self._board.fill_cell((x, y), players[-1].color)
                    if y in [1,3,6,8]:
                        self.squares[x][y].set_piece(Piece(player2, Color(player2).name))
                        self._board.fill_cell((x, y), players[1].color)

    def add_piece(self, cell, player):
        x, y = cell[0], cell[1]
        self.squares[x][y].set_piece(Piece(player, Color(player).name))

    def move_piece(self, at, to, player):
        x, y = to[0], to[1]
        self.squares[x][y].set_piece(Piece(player, Color(player).name))
        x, y = at[0], at[1]
        self.squares[x][y].remove_piece()

    def remove_piece(self, cell):
        x, y = cell[0], cell[1]
        self.squares[x][y].remove_piece()

    def set_default_colors(self):
        k= 5
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.squares[i][j].setStyleSheet("background-image : url(assets/board/22-{}{}.png)".format(k,j+1))
            k= k-1

    def set_current_player(self, player):
        self.current_player = player

    def reset_board(self):
        self._board = Board(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.squares[i][j].remove_piece()

    def enable_all_squares(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.squares[i][j].set_active(True)

    def disable_all_squares(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.squares[i][j].set_active(False)

    def putListBoard(self, listBoard):  # TODO: Need Update
        for i in range(len(self.self.squares)):
            for j in range(len(self.self.squares[0])):
                if listBoard[i][j] == None:
                    self.squares[i][j].removePiece()
                elif listBoard[i][j] == "black":
                    self.squares[i][j].setPiece(Piece(0, "white"))
                elif listBoard[i][j] == "green":
                    self.squares[i][j].setPiece(Piece(1, "green"))

    def get_board_array(self): # TODO: Need Update
        list_board = []
        for i in range(len(self.squares)):
            temp = []
            for j in range(len(self.squares[0])):
                if not self.squares[i][j].isPiece():
                    temp.append(None)
                else:
                    temp.append(self.squares[i][j].piece.getColor())
            list_board.append(temp)
        return list_board
