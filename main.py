import pygame
import sys
import tetrisBoard

WIDTH = 600
HEIGHT = 700
FPS = 60

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
                    
    screen.fill(BG_COLOR)
    
    board.render()
    
    pygame.display.flip()

pygame.quit()
sys.exit()