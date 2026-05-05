#!/usr/bin/env python3
import pygame

pygame.init()

from Board import Board
from Settings import Settings

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

board = Board(screen_width // 2, screen_height // 2, "white")
settings = Settings(50, 50, screen_width // 2, screen_height // 2)

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            settings_click = settings.click(x, y)
            if settings_click != "nothing":
                if settings_click == "white":
                    board = Board(screen_width // 2, screen_height // 2, "white")
                elif settings_click == "black":
                    board = Board(screen_width // 2, screen_height // 2, "black")
                elif settings_click == "reset":
                    board = Board(screen_width // 2, screen_height // 2, board.mode)
                elif settings_click == "exit":
                    running = False
            elif board.start_x < x < board.start_x + 8 * board.SQUARE_SIZE and board.start_y < y < board.start_y + 8 * board.SQUARE_SIZE:
                board.click(x, y)
    screen.fill((255, 255, 255))
    board.draw(screen)
    settings.draw(screen)
    pygame.display.flip()
    
pygame.quit()
