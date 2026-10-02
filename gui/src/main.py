#!/usr/bin/env python3
import subprocess

import pygame

pygame.init()

from board import Board
from settings import Settings


def send(cmd):
    engine.stdin.write(cmd + "\n")
    engine.stdin.flush()


def get(answer):
    line = engine.stdout.readline().strip()
    return line == answer


info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF
)
pygame.display.set_caption("Chess")
icon = pygame.image.load("../assets/pieces/white_pawn.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
board = Board(screen_width, screen_height, "white")
settings = Settings(50, 50, screen_width // 2, screen_height // 2)
engine = subprocess.Popen(
    ["../../build/engine"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    bufsize=1,
)
send("uci")
while get("uciok") == False:
    pass

while True:
    if board.position.result == "unknown":
        if board.mode == "white":
            if board.position.move_count % 2 == 1:
                send("position startpos moves " + " ".join(board.position.get()))
                if (
                    settings.button_difficulty.text == "DIFFICULTY: 1"
                    or settings.button_difficulty.text == "DIFFICULTY: 2"
                ):
                    send("go depth 1")
                line = engine.stdout.readline().strip()
                board.position.move(line.split()[1], "engine")
                board.position.append_position()
                board.position.check_end("human")

        else:
            if board.position.move_count % 2 == 0:
                send("position startpos moves " + " ".join(board.position.get()))
                if (
                    settings.button_difficulty.text == "DIFFICULTY: 1"
                    or settings.button_difficulty.text == "DIFFICULTY: 2"
                ):
                    send("go depth 1")
                line = engine.stdout.readline().strip()
                board.position.move(line.split()[1], "engine")
                board.position.append_position()
                board.position.check_end("human")
    exit_flag = False
    mouse_click = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_flag = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit_flag = True
                break
            elif event.key == pygame.K_F11:
                pygame.display.iconify()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = event
    if exit_flag:
        break
    if mouse_click is not None:
        x, y = mouse_click.pos
        settings_click = settings.click(x, y)
        if settings_click != "close":
            if settings_click == "white":
                board = Board(screen_width, screen_height, "white")
                send("ucinewgame")
                send("isready")
                get("readyok")
            elif settings_click == "black":
                board = Board(screen_width, screen_height, "black")
                send("ucinewgame")
                send("isready")
                get("readyok")
            elif settings_click == "reset":
                board = Board(screen_width, screen_height, board.mode)
                send("ucinewgame")
                send("isready")
                get("readyok")
            elif settings_click == "exit":
                break
        else:
            if board.position.result != "unknown":
                continue
            if board.mode == "white":
                if board.position.move_count % 2 == 0:
                    board.click(x, y)
            else:
                if board.position.move_count % 2 == 1:
                    board.click(x, y)
    screen.fill((255, 255, 255))
    board.draw(screen)
    settings.draw(screen)
    pygame.display.flip()
    clock.tick(60)

try:
    send("quit")
    engine.wait(timeout=5)
except subprocess.TimeoutExpired:
    engine.kill()
    engine.wait()

pygame.quit()
