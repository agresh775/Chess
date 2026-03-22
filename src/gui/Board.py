import pygame
from converter import convert

pygame.init()

class Board:

    SQUARE_SIZE = 80
    WHITE = (213, 201, 193)
    BLACK = (128, 74, 38)
    FONT = pygame.font.Font(None, 30)
    
    def __init__(self, center_x, center_y, mode):
        self.board = [[0]*8 for i in range(8)]
        self.mode = mode
        start_x = center_x - 4 * self.SQUARE_SIZE
        start_y = center_y - 4 * self.SQUARE_SIZE
        cur_pos_x = start_x
        cur_pos_y = start_y
        for y_step in range(8):
            for x_step in range(8):
                self.board[y_step][x_step] = pygame.Rect(cur_pos_x, cur_pos_y, self.SQUARE_SIZE, self.SQUARE_SIZE)
                if x_step == 7:
                    cur_pos_x = start_x
                else:
                    cur_pos_x += self.SQUARE_SIZE
            cur_pos_y += self.SQUARE_SIZE

    def draw(self, surface):
        cur_color = self.WHITE
        for y_step in range(8):
            for x_step in range(8):
                pygame.draw.rect(surface, cur_color, self.board[y_step][x_step], 0)
                if x_step == 0:
                    char_x, char_y = self.board[y_step][x_step].center
                    char_x -= self.SQUARE_SIZE * 0.75
                    text = self.FONT.render(convert(x_step, y_step, self.mode)[1], True, (0, 0, 0))
                    text_rect = text.get_rect(center = (char_x, char_y))
                    surface.blit(text, text_rect)
                if y_step == 7:
                    char_x, char_y = self.board[y_step][x_step].center
                    char_y += self.SQUARE_SIZE * 0.75
                    text = self.FONT.render(convert(x_step, y_step, self.mode)[0], True, (0, 0, 0))
                    text_rect = text.get_rect(center = (char_x, char_y))
                    surface.blit(text, text_rect)
                if x_step < 7:
                    if cur_color == self.WHITE:
                        cur_color = self.BLACK
                    else:
                        cur_color = self.WHITE
