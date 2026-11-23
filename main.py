import pygame
import sys
import tetrisBoard

WIDTH = 600
HEIGHT = 700
FPS = 60

CLOCKWISE = 1
ANTI_CLOCKWISE = -1

BG_COLOR = (30,30,30)

pygame.init()
    
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tetris")
    
clock = pygame.time.Clock()

board = tetrisBoard.Board(WIDTH/2, HEIGHT/2, screen)
    
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                board.rotatePiece(CLOCKWISE)
                    
    screen.fill(BG_COLOR)
    
    board.render()
    board.update()
    
    pygame.display.flip()

pygame.quit()
sys.exit()