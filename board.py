import pygame

class Board:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 320, 640
        self.boardRect = []
        self.rectColor = {}

    def clear(self):
        self.boardRect.clear()
        self.rectColor.clear()

    def addPiece(self, piece):
        for pieceRect in piece.rect_list:
            self.boardRect.append(pieceRect)
            self.rectColor[len(self.boardRect)-1] = piece.color

    def draw(self, screen):
        for i, rect in enumerate(self.boardRect):
            pygame.draw.rect(screen, self.rectColor[i], rect)

    def collide(self, piece, moveRight):
        rightMost = piece.rect_list[piece.bounds["rightMostPiece"]]
        leftMost = piece.rect_list[piece.bounds["leftMostPiece"]]
        for rect in self.boardRect:
            for pieceRect in piece.lastRowRect:
                if moveRight:
                    if (pieceRect.right == rect.left and pieceRect.y == rect.y) or (rightMost.right == rect.left and rightMost.y == rect.y):
                        return True
                else:
                    if (pieceRect.left == rect.right and pieceRect.y == rect.y) or (leftMost.left == rect.right and leftMost.y == rect.y):
                        return True

        return False

    def colliderect(self, piece):
        for rect in self.boardRect:
            for pieceRect in piece.rect_list:
                if pieceRect.colliderect(rect):
                    return True
        return False

    def lands(self, piece):
        for rect in self.boardRect:
            for pieceRect in piece.lastRowRect:
                if pieceRect.bottom == rect.top and pieceRect.x == rect.x:
                    return True
        return False

    def project(self, piece):
        tempPiece = piece
        lastPiece = tempPiece.rect_list[len(tempPiece.rect_list)-1]
        while lastPiece.bottom < self.HEIGHT and not self.lands(tempPiece):
            for rect in tempPiece.rect_list:
                rect.y += 32
            tempPiece.y += 1

        tempPiece.color = tempPiece.colorDark
        return tempPiece
    
    def checkGameOver(self):
        for rect in self.boardRect:
            if rect.y <= 32:
                return True
        return False


    def clearLines(self):
        for y in reversed(range(0,self.HEIGHT,32)):
            global numLinesCleared
            global lineFull
            lineFull = False
            numLinesCleared = 0
            counter = 0
            for x in range(32,self.WIDTH+32,32):
                for rect in self.boardRect:
                    if rect.y == y and rect.centerx+16 == x:
                        counter += 1
                    if counter == 10:
                        lineFull = True
                        break
            if lineFull:
                for i, rect in enumerate(self.boardRect):
                    if rect.y == y:
                        self.boardRect[i] = pygame.Rect(1000, 1000,0,0)
                        self.rectColor[i] = (0,0,0)

                for i, rect in enumerate(self.boardRect):
                    if rect.y < y:
                        rect.y += 32

