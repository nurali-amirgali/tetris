import pygame 

EMPTY = (0,0,0)
RED = (240, 0, 0)
GREEN = (0, 240, 0)
CYAN = (0, 240, 240)
YELLOW = (240, 240, 0)
PURPLE = (160, 0, 240)
DARK_BLUE = (0, 0, 240)
ORANGE = (240, 160, 0)

BORDER_COLOR = (128, 126, 124)

class Board:
    def __init__(self, x, y, screen, numTilesX = 10, numTilesY = 20, tileSize = 30, borderWidth = 1, outerBorderWidth = 5):
        self.x = x
        self.y = y
        self.numTilesX = numTilesX
        self.numTilesY = numTilesY
        self.screen = screen
        self.tileSize = tileSize
        self.borderWidth = borderWidth
        self.outerBorderWidth = outerBorderWidth
        self.tiles = [[EMPTY] * numTilesX for _ in range(numTilesY)]
    
    def render(self):
        x = self.x - (self.numTilesX * self.tileSize)/2
        y = self.y - (self.numTilesY * self.tileSize)/2
        
        borderW = self.outerBorderWidth
        bgW = (self.tileSize * self.numTilesX) + (borderW * 2)
        bgH = (self.tileSize * self.numTilesY) + (borderW * 2)
        bgX = x - borderW
        bgY = y - borderW
        pygame.draw.rect(self.screen, BORDER_COLOR, (bgX, bgY, bgW, bgH))
        
        for row in range(self.numTilesY):
            for col in range(self.numTilesX):
                tile = self.tiles[row][col]
                
                tileX = (col * self.tileSize) + x
                tileY = (row * self.tileSize) + y
                
                pygame.draw.rect(self.screen, tile, (tileX, tileY, self.tileSize, self.tileSize))
                pygame.draw.rect(self.screen, BORDER_COLOR, (tileX, tileY, self.tileSize, self.tileSize), self.borderWidth)