import pygame

test = pygame.Rect(0,200,32,32)

print(test.centerx + 16)
print(test.y+32)

# import pygame
# 
# class Board:
#     def __init__(self):
#         self.WIDTH, self.HEIGHT = 320, 640
#         self.boardPiece = []
#         self.boardRect = []
#         self.rectColor = {}
# 
#     def addPiece(self, piece):
#         self.boardPiece.append(piece)
#         for pieceRect in piece.rect_list:
#             self.boardRect.append(pieceRect)
#             self.rectColor[len(self.boardRect)-1] = piece.color
# 
#     def draw(self, screen):
#         for i, rect in enumerate(self.boardRect):
#             pygame.draw.rect(screen, self.rectColor[i], rect)
# 
#     def collide(self, piece, moveRight):
#         rightMost = piece.rect_list[piece.bounds["rightMostPiece"]]
#         leftMost = piece.rect_list[piece.bounds["leftMostPiece"]]
#         for rect in self.boardRect:
#             for pieceRect in piece.lastRowRect:
#                 if moveRight:
#                     if (pieceRect.right == rect.left and pieceRect.y == rect.y) or (rightMost.right == rect.left and rightMost.y == rect.y):
#                         return True
#                 else:
#                     if (pieceRect.left == rect.right and pieceRect.y == rect.y) or (leftMost.left == rect.right and leftMost.y == rect.y):
#                         return True
# 
#         return False
# 
#     def colliderect(self, piece):
#         for rect in self.boardRect:
#             for pieceRect in piece.rect_list:
#                 if rect.colliderect(pieceRect):
#                     return True
#         return False
# 
#     def lands(self, piece):
#         for rect in self.boardRect:
#             for pieceRect in piece.lastRowRect:
#                 if pieceRect.bottom == rect.top and pieceRect.x == rect.x:
#                     return True
#         return False
# 
