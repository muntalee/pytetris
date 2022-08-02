# imports
import sys, random
import pygame
from tetrominoes import Tetrominoes
from board import Board

# essentials
pygame.init()
fps = 20
fpsClock = pygame.time.Clock()
WIDTH, HEIGHT = 320, 640
screen = pygame.display.set_mode((WIDTH+200, HEIGHT))
pygame.display.set_caption("Pygame Tetris")

# main piece
global piece
piece = Tetrominoes()
dim = 32

# temp piece
tempPiece = Tetrominoes()

# board
global board
board = Board()

# values for piece
pieceNum = 0
rotation = 0
nextPieceNum = random.randrange(7)
savedPieceNum = -1

# start screen text
font = pygame.font.Font('Fami-Serif-Bold.otf', 32)
title = font.render('TETRIS', True, (255,255,255))
titleRect = title.get_rect()
titleRect.center = (WIDTH // 2 + 100, HEIGHT // 2 - 100)

# description
font2 = pygame.font.Font('Fami-Serif-Bold.otf', 20)
desc = font2.render('Press ENTER to Play', True, (255,255,255))
descRect = desc.get_rect()
descRect.center = (WIDTH // 2 + 100, HEIGHT // 2)

# game over text
gameOver = font.render('GAME OVER', True, (255,255,255))
gameOverRect = gameOver.get_rect()
gameOverRect.center = (WIDTH // 2 + 100, HEIGHT // 2 - 100)

# description
retryText = font2.render('Press ENTER to Retry', True, (255,255,255))
retryTextRect = retryText.get_rect()
retryTextRect.center = (WIDTH // 2 + 100, HEIGHT // 2)

# cooldown for the piece drop speed
last = pygame.time.get_ticks()
cooldown = 600

# generate new piece
def newPiece():
    global pieceNum, rotation, piece, nextPieceNum
    pieceNum = nextPieceNum
    nextPieceNum = random.randrange(7)

    if pieceNum == nextPieceNum:
        nextPieceNum = nextPieceNum + 1
        if nextPieceNum > 6:
            nextPieceNum = 0

    piece = Tetrominoes()
    piece.generatePiece(pieceNum, rotation)

# temp piece for projection
def newTempPiece():
    global pieceNum, rotation, piece, tempPiece
    tempPiece = Tetrominoes()
    tempPiece.x = piece.x
    tempPiece.y = piece.y
    tempPiece.generatePiece(pieceNum, rotation)

# drawing UI for next piece, and other stuff
def drawUI():
    pygame.draw.line(screen, (255,255,255), (WIDTH,0), (WIDTH,HEIGHT))

    # next piece display
    nextPiece = Tetrominoes()
    nextPiece.x += 9
    nextPiece.y += 6
    nextPiece.generatePiece(nextPieceNum, 0)
    nextPiece.draw(screen)

    # next piece display text
    uifont = pygame.font.Font('Fami-Serif-Bold.otf', 24)
    nextPieceText = uifont.render('NEXT', True, (255,255,255))
    nextPieceTextRect = nextPieceText.get_rect()
    nextPieceTextRect.center = (430, 50)

    # hold piece display text
    savedPieceText = uifont.render('HOLD', True, (255,255,255))
    savedPieceTextRect = savedPieceText.get_rect()
    savedPieceTextRect.center = (430, 290)

    # hold piece display
    if savedPieceNum != -1:
        savedPiece = Tetrominoes()
        savedPiece.x += 9
        savedPiece.y += 14
        savedPiece.generatePiece(savedPieceNum, 0)
        savedPiece.draw(screen)

    # add to screen
    screen.blit(nextPieceText, nextPieceTextRect)
    screen.blit(savedPieceText, savedPieceTextRect)


# rotates piece
def rotate(isClockWise):
    global pieceNum, rotation, screen, piece, tempPiece
    if isClockWise:
        rotation = rotation + 1
    else:
        rotation = rotation - 1
    if rotation < 0:
        rotation = len(piece.pieceList[pieceNum])-1
        piece.generatePiece(pieceNum, rotation)
    elif len(piece.pieceList[pieceNum]) > rotation:
        piece.generatePiece(pieceNum, rotation)
    else:
        rotation = 0
        piece.generatePiece(pieceNum, rotation)

# starts game with new piece
newPiece()
global startGame

# starts in start screen
startGame = False

# Game loop.
while True:
    screen.fill((15, 15, 15))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # once an ENTER is pressed, game starts (or starts over)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                startGame = True

    # title page
    if not startGame:
        screen.blit(title, titleRect)
        screen.blit(desc, descRect)
    
    # game over page
    if board.checkGameOver():
        title = gameOver
        desc = retryText
        titleRect = gameOverRect
        descRect = retryTextRect
        board.clear()
        savedPieceNum = -1
        startGame = False


    # if we start game and we havent lost, we play
    if startGame and not board.checkGameOver():
        keys = pygame.key.get_pressed()

        # control piece
        # move left with LEFT ARROW key
        if keys[pygame.K_LEFT]:
            piece.generatePiece(pieceNum, rotation)
            if piece.rect_list[piece.bounds["leftMostPiece"]].left > 0 and not(board.collide(piece, False)):
                for rect in piece.rect_list:
                    rect.x -= dim
                piece.x -= 1

        # move right with RIGHT ARROW key
        if keys[pygame.K_RIGHT]:
            piece.generatePiece(pieceNum, rotation)
            if piece.rect_list[piece.bounds["rightMostPiece"]].right < WIDTH and not(board.collide(piece, True)):
                for rect in piece.rect_list:
                    rect.x += dim
                piece.x += 1

        # rotate CW with UP ARROW key
        if keys[pygame.K_UP]:
            pygame.event.wait(0)
            rotate(True)

        # rotate CCW with Z key
        if keys[pygame.K_z]:
            pygame.event.wait(0)
            rotate(False)

        # increase drop speed of piece with DOWN ARROW key
        if keys[pygame.K_DOWN]:
            cooldown = 50
        else:
            cooldown = 600

        # hard drop with SPACE key
        if keys[pygame.K_SPACE]:
            pygame.event.wait(0)
            lastPiece = piece.rect_list[len(piece.rect_list)-1]
            while lastPiece.bottom < HEIGHT and not board.lands(piece):
                for rect in piece.rect_list:
                    rect.y += dim
                piece.y += 1
            board.addPiece(piece)
            newPiece()
            continue

        # save piece with SHIFT KEY
        if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
            pygame.event.wait(0)
            nextPieceNum = savedPieceNum
            savedPieceNum = pieceNum
            newPiece()
            continue

        # piece moves down normally
        now = pygame.time.get_ticks()
        if now - last >= cooldown:
            last = now
            lastPiece = piece.rect_list[len(piece.rect_list)-1]
            if lastPiece.bottom < HEIGHT and not board.lands(piece) or board.colliderect(piece):
                for rect in piece.rect_list:
                    rect.y += dim
                piece.y += 1
            else:
                board.addPiece(piece)
                newPiece()

        # draw projection
        newTempPiece()
        projected = tempPiece
        projected = board.project(tempPiece)
        projected.draw(screen)

        # draw piece
        piece.draw(screen)

        # clear board of any full lines
        board.clearLines()

        # draw board
        board.draw(screen)
        
        # draw the UI
        drawUI()

    # update display
    pygame.display.flip()
    fpsClock.tick(fps)
