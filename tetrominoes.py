import pygame

class Tetrominoes:
    def __init__(self):
        self.x = 2
        self.y = -3
        self.piece = []
        self.color = (0,0,0)
        self.colorDark = (0,0,0)
        self.lastRow = 0

        self.bounds = {
            "leftMostPiece": 0,
            "rightMostPiece": 0
        }

        self.colorList = [(0,255,0),(255,0,0),(0,255,255),(255,255,0),(0,0,255),(255,128,0),(128,0,255)]
        self.colorListDark = [(0,125,0),(125,0,0),(0,125,125),(125,125,0),(0,0,125),(125,64,0),(64,0,125)]
        self.rect_list = []

        self.lastRowRect = []

        # List of all pieces
        self.S = [['.....',
                   '.....',
                   '..OO.',
                   '.OO..',
                   '.....'],
                  ['.....',
                   '..O..',
                   '..OO.',
                   '...O.',
                   '.....']]

        self.Z = [['.....',
                   '.....',
                   '.OO..',
                   '..OO.',
                   '.....'],
                  ['.....',
                   '..O..',
                   '.OO..',
                   '.O...',
                   '.....']]

        self.I = [['..O..',
                   '..O..',
                   '..O..',
                   '..O..',
                   '.....'],
                  ['.....',
                   '.....',
                   'OOOO.',
                   '.....',
                   '.....']]

        self.O = [['.....',
                   '.....',
                   '.OO..',
                   '.OO..',
                   '.....']]

        self.J = [['.....',
                   '.O...',
                   '.OOO.',
                   '.....',
                   '.....'],
                  ['.....',
                   '..OO.',
                   '..O..',
                   '..O..',
                   '.....'],
                  ['.....',
                   '.....',
                   '.OOO.',
                   '...O.',
                   '.....'],
                  ['.....',
                   '..O..',
                   '..O..',
                   '.OO..',
                   '.....']]

        self.L = [['.....',
                   '...O.',
                   '.OOO.',
                   '.....',
                   '.....'],
                  ['.....',
                   '..O..',
                   '..O..',
                   '..OO.',
                   '.....'],
                  ['.....',
                   '.....',
                   '.OOO.',
                   '.O...',
                   '.....'],
                  ['.....',
                   '.OO..',
                   '..O..',
                   '..O..',
                   '.....']]

        self.T = [['.....',
                   '..O..',
                   '.OOO.',
                   '.....',
                   '.....'],
                  ['.....',
                   '..O..',
                   '..OO.',
                   '..O..',
                   '.....'],
                  ['.....',
                   '.....',
                   '.OOO.',
                   '..O..',
                   '.....'],
                  ['.....',
                   '..O..',
                   '.OO..',
                   '..O..',
                   '.....']]

        # pieces are in array
        self.pieceList = [self.S,self.Z,self.I,self.O,self.J,self.L,self.T]

    # create a piece for pygame
    def generatePiece(self, pieceNum, rotation):
        self.rect_list = []
        self.lastRowRect = []
        tempPiece = self.pieceList[pieceNum]
        try:
            self.piece = tempPiece[rotation]
        except:
            self.piece = tempPiece[len(tempPiece)-1]
            rotation = 0

        self.color = self.colorList[pieceNum]
        self.colorDark = self.colorListDark[pieceNum]

        # loop through each row from bottom to top

        last = self.lastRowStr(self.piece)
        self.lastRow = self.lastRowIndex(last, self.piece)

        colNum = 0
        smallest = 0
        largest = 0

        # creates the list of rects for the piece
        for row_count, row in enumerate(self.piece):
            for col_count, col in enumerate(row):
                if col == 'O':
                    self.rect_list.append(pygame.Rect(((32 * col_count) + (self.x * 32), (32 * row_count) + (self.y * 32), 32, 32)))
                    if row_count == self.lastRow:
                        self.lastRowRect.append(self.rect_list[len(self.rect_list)-1])
                    if colNum >= largest:
                        largest = colNum
                        self.bounds["rightMostPiece"] = len(self.rect_list)-1
                    if colNum <= smallest:
                        smallest = colNum
                        self.bounds["leftMostPiece"] = len(self.rect_list)-1
                colNum += 1
            colNum = 0

        # for the last row
        for row_count, row in enumerate(self.piece):
            for col_count, col in enumerate(row):
                if row_count == self.lastRow:
                    if col == 'O':
                        self.lastRowRect.append(pygame.Rect(((32 * col_count) + (self.x * 32), (32 * row_count) + (self.y * 32), 32, 32)))

    def draw(self, screen):
        # displays all the rects from the list
        for rect in self.rect_list:
            pygame.draw.rect(screen, self.color, rect)

    def lastRowStr(self, piece):
        for i in reversed(piece):
            for j in reversed(i):
                if j == 'O':
                    return i

    def lastRowIndex(self, row, piece):
        for i in reversed(range(len(piece))):
            if piece[i] == row:
                return i

    def printPiece(self):
        for i in self.piece:
            print(i)
