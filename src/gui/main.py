#!/usr/bin/env python3
import pygame
from Board import Board

pygame.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

board = Board(screen_width // 2, screen_height // 2, "white")

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_F11:
                pygame.display.iconify()
    screen.fill((255, 255, 255))
    board.draw(screen)
    pygame.display.flip()
    
pygame.quit()
