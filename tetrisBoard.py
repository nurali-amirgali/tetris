import pygame
import time
import random

EMPTY = (0,0,0)
RED = (240, 0, 0)
GREEN = (0, 240, 0)
CYAN = (0, 240, 240)
YELLOW = (240, 240, 0)
PURPLE = (160, 0, 240)
DARK_BLUE = (0, 0, 240)
ORANGE = (240, 160, 0)

BORDER_COLOR = (128, 126, 124)

I_PIECE = [[0,0,0,0],
           [1,1,1,1],
           [0,0,0,0],
           [0,0,0,0]]

O_PIECE = [[1,1],
           [1,1]]

T_PIECE = [[0,1,0],
           [1,1,1],
           [0,0,0]]

S_PIECE = [[0,1,1],
           [1,1,0],
           [0,0,0]]

Z_PIECE = [[1,1,0],
           [0,1,1],
           [0,0,0]]

J_PIECE = [[1,0,0],
           [1,1,1],
           [0,0,0]]

L_PIECE = [[0,0,1],
           [1,1,1],
           [0,0,0]]

PIECES = {
    "I": (I_PIECE, CYAN),
    "O": (O_PIECE, YELLOW),
    "T": (T_PIECE, PURPLE),
    "S": (S_PIECE, GREEN),
    "Z": (Z_PIECE, RED),
    "J": (J_PIECE, DARK_BLUE),
    "L": (L_PIECE, ORANGE),
}

class piece:
    def __init__(self):
        pass

class Board:
    def __init__(self, x, y, screen, numTilesX = 10, numTilesY = 20, tileSize = 30, borderWidth = 1, outerBorderWidth = 7):
        self.x = x
        self.y = y
        
        self.hiddenTilesY = 4
        self.numTilesX = numTilesX
        self.numTilesY = numTilesY + self.hiddenTilesY
        
        self.visibleTilesY = numTilesY
        self.visibleTilesX = numTilesX
        
        self.screen = screen
        self.tileSize = tileSize
        self.borderWidth = borderWidth
        self.outerBorderWidth = outerBorderWidth
        self.tiles = [[EMPTY] * numTilesX for _ in range(numTilesY + self.hiddenTilesY)]
        
        self.lastUpdateTime = time.perf_counter()
        self.updateDelay = 500
        
        self.isPieceActive = False
        self.activePiece = None
        self.nextPieces = [list(PIECES.keys())]
        self.currentPieceIndex = 0
        
        self.piecePos = (0,0)
        
    def randomizePieces(self):
        random.shuffle(self.nextPieces)
    
    def renderGridLines(self, x, y):
        for row in range(self.visibleTilesY + 1):
            drawY = (row * self.tileSize) + y
            pygame.draw.line(self.screen, BORDER_COLOR, (x, drawY), (x + (self.tileSize * self.visibleTilesX), drawY), self.borderWidth)
        
        for col in range(self.visibleTilesX + 1):
            drawX = (col * self.tileSize) + x
            pygame.draw.line(self.screen, BORDER_COLOR, (drawX, y), (drawX, y + (self.tileSize * self.visibleTilesY)), self.borderWidth)
        
    
    def render(self):
        x = self.x - (self.visibleTilesX * self.tileSize)/2
        y = self.y - (self.visibleTilesY * self.tileSize)/2
        
        borderW = self.outerBorderWidth
        bgW = (self.tileSize * self.visibleTilesX) + (borderW * 2)
        bgH = (self.tileSize * self.visibleTilesY) + (borderW * 2)
        bgX = x - borderW
        bgY = y - borderW
        pygame.draw.rect(self.screen, BORDER_COLOR, (bgX, bgY, bgW, bgH), border_radius=5)
        
        for row in range(self.visibleTilesY):
            for col in range(self.visibleTilesX):
                tile = self.tiles[row + self.hiddenTilesY][col]
                
                tileX = (col * self.tileSize) + x
                tileY = (row * self.tileSize) + y
                
                pygame.draw.rect(self.screen, tile, (tileX, tileY, self.tileSize, self.tileSize))
        self.renderGridLines(x, y)
    
    def update(self):
        now = time.perf_counter()
        if (now - self.lastUpdateTime) >= (self.updateDelay/1000):
            self.lastUpdateTime = now
            if not self.activePiece:
                self.activePiece = True
                self.activePiece = self.nextPieces[self.currentPieceIndex]
                self.currentPieceIndex += 1
            print("tick")
                        