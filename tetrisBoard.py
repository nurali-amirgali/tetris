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
        self.tiles = [[EMPTY] * numTilesX for _ in range(numTilesY + self.hiddenTilesY)] #y, x
        
        self.lastUpdateTime = time.perf_counter()
        self.updateDelay = 100 #1000
        
        self.nextPieces = list(PIECES.keys())
        self.randomizePieces()
        self.currentPieceIndex = 0
        
        self.piecePos = (0,0)
        self.pieceArray = []
        self.pieceType = None
        self.isPieceActive = False
        self.pieceColor = None
        self.spawnNextPiece()
        
    def randomizePieces(self):
        random.shuffle(self.nextPieces)
    
    def renderGridLines(self, x, y):
        for row in range(self.visibleTilesY + 1):
            drawY = (row * self.tileSize) + y
            pygame.draw.line(self.screen, BORDER_COLOR, (x, drawY), (x + (self.tileSize * self.visibleTilesX), drawY), self.borderWidth)
        
        for col in range(self.visibleTilesX + 1):
            drawX = (col * self.tileSize) + x
            pygame.draw.line(self.screen, BORDER_COLOR, (drawX, y), (drawX, y + (self.tileSize * self.visibleTilesY)), self.borderWidth)
    
    def combineLists(self, list1, list2):
        newList = [[EMPTY] * self.numTilesX for _ in range(self.numTilesY)]
        for row in range(self.numTilesY):
                for col in range(self.numTilesX):
                    item1 = list1[row][col]
                    item2 = list2[row][col]
                    if item1 == EMPTY:
                        newList[row][col] = item2
                    else:
                        newList[row][col] = item1
        return newList
                        
    def pieceToList(self):
        newList = [[EMPTY] * self.numTilesX for _ in range(self.numTilesY)]
        belowFloor = False
        for row, rowList in enumerate(self.pieceArray):
            for col, tile in enumerate(rowList):
                if tile:
                    globalY = row + self.piecePos[1] + self.hiddenTilesY
                    globalX = col + self.piecePos[0]
                    if globalY >= self.numTilesY:
                        belowFloor = True
                    try:
                        newList[globalY][globalX] = self.pieceColor
                    except IndexError:
                        continue
        return newList, belowFloor
                        
    def checkGrounding(self):
        pieceList, isBelowFloor = self.pieceToList()
        isGrounded = isBelowFloor
        
        for row in range(self.numTilesY):
            for col in range(self.numTilesX):
                existingTile = self.tiles[row][col]
                pieceTile = pieceList[row][col]
                if existingTile != EMPTY and pieceTile != EMPTY:
                    isGrounded = True
                    break
            if isGrounded: break
        
        if isGrounded:
            self.piecePos = (self.piecePos[0], self.piecePos[1]-1)
            pieceList, isBelowFloor = self.pieceToList()
            self.spawnNextPiece()
            self.tiles = self.combineLists(pieceList, self.tiles)
    
    def renderPiece(self, x, y, tileSize, pieceList, color):
        for row, rowList in enumerate(pieceList):
            for col, tile in enumerate(rowList):
                tileX = (col * tileSize) + x
                tileY = (row * tileSize) + y
                
                if tile:
                    pygame.draw.rect(self.screen, color, (tileX, tileY, tileSize, tileSize))
    
    def spawnNextPiece(self):
        pieceType = self.nextPieces[self.currentPieceIndex]
        print(pieceType)
        
        self.currentPieceIndex += 1
        if self.currentPieceIndex > len(self.nextPieces) - 1:
            self.currentPieceIndex = 0
            self.randomizePieces()
            
        self.pieceColor = PIECES[pieceType][1]
        self.pieceArray = PIECES[pieceType][0]
        width = len(self.pieceArray[0])
        spawnX = round(self.visibleTilesX/2 - width/2)
        
        self.piecePos = (spawnX, -self.hiddenTilesY)
    
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
        
        
        pieceX = x + (self.piecePos[0] * self.tileSize)
        pieceY = y + (self.piecePos[1] * self.tileSize)
        self.renderPiece(pieceX, pieceY, self.tileSize, self.pieceArray, self.pieceColor)
        
        self.renderGridLines(x, y)
    
    def update(self):
        now = time.perf_counter()
        if (now - self.lastUpdateTime) >= (self.updateDelay/1000):
            self.lastUpdateTime = now
            self.piecePos = (self.piecePos[0], self.piecePos[1] + 1)
            self.checkGrounding()
            #print(self.piecePos)
                        