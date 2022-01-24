"""A driver file responsible for user input and displaying current game state."""
 
from os import truncate
import pygame as p 
import ChessEngine

p.init()
WIDTH = HEIGHT = 512 
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 #for animations later on 
IMAGES= {}

def loadImages():
    """
    Initialize a global dictionary of images, called exactly once in the main bc expensive operation.
    """
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        #we can access an image by saying "IMAGES['wp']"

def main():
    """
    Main driver, handle user input and updating graphics.
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made

    loadImages()
    running = True
    sqSelected = () #no square is selected, keep track of last click of user (tuple)
    playerClicks = [] #keep track of player clicks, two tuples

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #the user clicked the same square twice
                    sqSelected = () # deselect
                    playerClicks = [] # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append both 1st and 2nd clicks
                if len(playerClicks) == 2: # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () # reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo is Z
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    """ Responsible for all graphics within a current game state."""
    drawBoard(screen) # draw squares on the board
    # add piece highlighting or suggestions later
    drawPieces(screen, gs.board) # draw pieces on top of those squares

# top left always light (from any pov)
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION): 
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# if you ever import main somewhere else it won't run the file
if __name__== "__main__":
    main()