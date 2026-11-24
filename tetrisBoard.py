import pygame
import time
import random
from dataclasses import dataclass
from constants import *

def rotateArray(array, direction):
    if direction == CLOCKWISE:
        return [list(row) for row in zip(*array[::-1])]
    elif direction == ANTI_CLOCKWISE:
        return [list(row) for row in zip(*array)][::-1]
    return array

@dataclass
class invalidTiles:
    underList: list
    collisionList: list
    aboveList: list
    sideList: list
    allList: list

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
        self.updateDelay = 1000 #1000
        
        self.nextPieces = list(PIECES.keys())
        self.randomizePieces()
        self.currentPieceIndex = 0
        
        self.piecePos = (0,0)
        self.pieceArray = []
        self.pieceType = None
        self.isPieceActive = False
        self.pieceColor = None
        self.spawnNextPiece()
        
        #i just took these values from the default tetr.io handling values
        #in Milliseconds
        self.delayedAutoShift = 167
        self.autoRepeatRate = 33
        self.lastShiftTime = time.perf_counter()
        self.shiftDir = 0 #right is 1 and left is -1
        self.delayOver = False
        self.initialPressTime = time.perf_counter()
        
    def randomizePieces(self):
        random.shuffle(self.nextPieces)
        
    def getTile(self, x, y):
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[y]):
            return self.tiles[y][x]
        return None
        
    def rotatePiece(self, direction):
        self.pieceArray = rotateArray(self.pieceArray, direction)
    
    def renderGridLines(self, x, y):
        for row in range(self.visibleTilesY + 1):
            drawY = (row * self.tileSize) + y
            pygame.draw.line(self.screen, BORDER_COLOR, (x, drawY), (x + (self.tileSize * self.visibleTilesX), drawY), self.borderWidth)
        
        for col in range(self.visibleTilesX + 1):
            drawX = (col * self.tileSize) + x
            pygame.draw.line(self.screen, BORDER_COLOR, (drawX, y), (drawX, y + (self.tileSize * self.visibleTilesY)), self.borderWidth)
                        
    
    #returns all the tiles that are out of bounds or collide with other tiles
    #this is like the most important function in this code
    def getInvalidTiles(self):
        collidingTiles = []
        belowTiles = []
        sideTiles = []
        aboveTiles = []
        allTiles = []
        for row, rowList in enumerate(self.pieceArray):
            for col, tile in enumerate(rowList):
                if tile:
                    globalY = row + self.piecePos[1] + self.hiddenTilesY
                    globalX = col + self.piecePos[0]
                    pos = (globalX, globalY)
                    
                    #if the tile goes out of bounds above the grid
                    if globalY < 0:
                        aboveTiles.append(pos)
                    
                    #if the tile goes out of bounds under the grid
                    if globalY > (self.numTilesY - 1):
                        belowTiles.append(pos)
                        
                    #if the tiles goes out of bounds on the left or right side
                    if 0 > globalX or globalX > (self.numTilesX - 1):
                        sideTiles.append(pos)

                    #if the tile collides with another
                    if self.getTile(globalX, globalY) != EMPTY and self.getTile(globalX, globalY) != None:
                        collidingTiles.append(pos)
                        
        #combine all these lists into one list
        allTiles = list(dict.fromkeys(belowTiles + collidingTiles + aboveTiles + sideTiles))
        return invalidTiles(belowTiles, collidingTiles, aboveTiles, sideTiles, allTiles)
        
    #it will put the tiles from the piece onto the global tiles list
    def connectPiece(self):
        for row, rowList in enumerate(self.pieceArray):
            for col, tile in enumerate(rowList):
                if tile:
                    globalY = row + self.piecePos[1] + self.hiddenTilesY
                    globalX = col + self.piecePos[0]
                    if self.getTile(globalX, globalY) != None:
                        self.tiles[globalY][globalX] = self.pieceColor
            
    def pieceTick(self):
        tiles = self.getInvalidTiles()
        print(tiles.allList)
        if tiles.underList or tiles.collisionList:
            self.piecePos = (self.piecePos[0], self.piecePos[1]-1)
            self.connectPiece()
            self.spawnNextPiece()
                        
    
    def renderPiece(self, x, y, tileSize, pieceList, color):
        for row, rowList in enumerate(pieceList):
            for col, tile in enumerate(rowList):
                tileX = (col * tileSize) + x
                tileY = (row * tileSize) + y
                
                if tile:
                    pygame.draw.rect(self.screen, color, (tileX, tileY, tileSize, tileSize))
    
    #1 = right, -1 = left
    def movePiece(self, dir):
        self.piecePos = (self.piecePos[0] + dir, self.piecePos[1])
        tiles = self.getInvalidTiles()
        if tiles.sideList or tiles.collisionList:
            self.piecePos = (self.piecePos[0] - dir, self.piecePos[1])
           
    def newInputStart(self, dir):
        self.shiftDir = dir
        self.delayOver = False
        self.initialPressTime = time.perf_counter()
        self.movePiece(dir)
    
    def handleInput(self):
        keys = pygame.key.get_pressed()
        
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.shiftDir = 0
        
        timeNow = time.perf_counter()
        keyDirs = {1:keys[pygame.K_RIGHT], -1:keys[pygame.K_LEFT]}
        for dir, keyList in keyDirs.items():
            if keyList:
                if self.shiftDir != dir:
                    self.newInputStart(dir)
                    
                if self.delayOver:
                    if (timeNow - self.lastShiftTime) >= self.autoRepeatRate/1000:
                        self.movePiece(dir)
                        self.lastShiftTime = timeNow
                else:
                    if (timeNow - self.initialPressTime) >= self.delayedAutoShift/1000:
                        self.delayOver = True

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
            self.pieceTick()
                        