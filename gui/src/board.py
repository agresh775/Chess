import copy

import pygame
import pygame.gfxdraw

from converter import convert
from position import Position


class Board:
    SQUARE_SIZE = 80
    WHITE = (213, 201, 193)
    BLACK = (128, 74, 38)
    GREEN = (63, 140, 84)
    RESULT_COLOR = (221, 228, 240)
    FONT = pygame.font.Font(None, 30)
    RESULT_FONT = pygame.font.Font(None, 100)

    class Piece(pygame.sprite.Sprite):
        def __init__(self, board, color, piece_type, square, operations):
            super().__init__()
            self.board = board
            self.color = color
            self.piece_type = piece_type
            self.move_cnt = 0
            self.square = square
            self.operations = operations
            if self.board.mode == self.color:
                self.board.human.add(self)
            else:
                self.board.engine.add(self)
            file_name = color + "_" + piece_type
            original_image = pygame.image.load(f"../assets/pieces/{file_name}.png")
            scaled_image = pygame.transform.smoothscale(
                original_image, (Board.SQUARE_SIZE, Board.SQUARE_SIZE)
            )
            self.image = scaled_image
            self.rect = self.image.get_rect()

        def __copy__(self):
            # Атрибут square полностью копируется, все остальные - по ссылке.
            new = Board.Piece.__new__(Board.Piece)
            new.__dict__.update(self.__dict__)
            new.__dict__["square"] = copy.copy(self.square)
            return new

        def set_rect(self):
            y, x = self.square
            self.rect.center = self.board.board[y][x][1].center

    def __init__(self, screen_width, screen_height, mode):
        center_x, center_y = screen_width // 2, screen_height // 2
        self.screen_width = screen_width
        self.screen_height = screen_height
        """
        Двумерный массив, содержащий тройки (<цвет>, <прямоугольник>, <флаг выделения>).
        Флаг выделения равен 0 - выделения нет.
        Флаг выделения равен 1 - выбрана фигура.
        Флаг выделения равен 2 - есть возможность для хода без взятия.
        Флаг выделения равен 3 - есть возможность для хода с взятием.
        """
        self.board = [[None] * 9 for i in range(9)]
        self.mode = mode
        self.human = pygame.sprite.Group()
        self.engine = pygame.sprite.Group()
        self.position = Position(self)
        self.start_x = center_x - 4 * self.SQUARE_SIZE
        self.start_y = self.convert_y(center_y + 4 * self.SQUARE_SIZE)
        cur_pos_x = self.start_x + 0.5 * self.SQUARE_SIZE
        cur_pos_y = self.start_y + 0.5 * self.SQUARE_SIZE
        cur_color = self.WHITE
        for y_step in range(1, 9):
            for x_step in range(1, 9):
                if cur_color == self.WHITE:
                    cur_color = self.BLACK
                else:
                    cur_color = self.WHITE
                rect = pygame.Rect(0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE)
                rect.center = (cur_pos_x, self.convert_y(cur_pos_y))
                if self.mode == "black":
                    # Поля чёрных отображаются зеркально главной диагонали, чтобы стартовая позиция была снизу.
                    x, y = rect.center
                    x = self.screen_width // 2 + (self.screen_width // 2 - x)
                    y = self.screen_height // 2 + (self.screen_height // 2 - y)
                    rect.center = (x, y)
                self.board[y_step][x_step] = [cur_color, rect, 0]
                if x_step == 8:
                    cur_pos_x = self.start_x + 0.5 * self.SQUARE_SIZE
                    if cur_color == self.WHITE:
                        cur_color = self.BLACK
                    else:
                        cur_color = self.WHITE
                else:
                    cur_pos_x += self.SQUARE_SIZE
            cur_pos_y += self.SQUARE_SIZE

    def convert_y(self, y):
        # y отсчитывается снизу вверх.
        return self.screen_height - y

    def reset_flags(self):
        for y_step in range(1, 9):
            for x_step in range(1, 9):
                self.board[y_step][x_step][2] = 0

    def click(self, mouse_x, mouse_y):
        mouse_y = self.convert_y(mouse_y)
        # Обрабатывается попадание клика по доске.
        if self.mode == "black":
            mouse_x = self.screen_width // 2 + (self.screen_width // 2 - mouse_x)
            mouse_y = self.screen_height // 2 + (self.screen_height // 2 - mouse_y)
        mouse_x -= self.start_x
        mouse_y -= self.start_y
        if mouse_x < 0 or mouse_y < 0:
            return
        x = mouse_x // self.SQUARE_SIZE + 1
        y = mouse_y // self.SQUARE_SIZE + 1
        if x > 8 or y > 8:
            return
        # Клик совершен по полю с возможностью хода - сделать ход.
        if self.board[y][x][2] in [2, 3]:
            for y_step in range(1, 9):
                for x_step in range(1, 9):
                    if self.board[y_step][x_step][2] == 1:
                        self.position.move(
                            convert(x_step, y_step) + convert(x, y), "human"
                        )
                        self.position.append_position()
                        self.position.check_end("engine")
                        break
            self.reset_flags()
        # Клик совершен по полю с выделенной фигурой - снять все выделения.
        elif self.board[y][x][2] == 1:
            self.reset_flags()
        # Клик совершен по полю с фигурой без выделения - выделить данное поле и все поля с возможностью хода.
        elif self.position.find_piece([y, x], "human") is not None:
            self.reset_flags()
            self.board[y][x][2] = 1
            for square in self.position.available_squares(
                self.position.find_piece([y, x], "human"), "human"
            ):
                # Выполняется проверка получения шаха после хода.
                flag = False
                self.position.move(
                    convert(x, y) + convert(square[1], square[0]), "human"
                )
                self.position.append_position()
                flag = self.position.check_check("human")
                self.position.pop_position()
                if flag == False:
                    if self.position.find_piece(square, "engine") is None:
                        self.board[square[0]][square[1]][2] = 2
                    else:
                        self.board[square[0]][square[1]][2] = 3

    def draw(self, surface):
        for y_step in range(1, 9):
            for x_step in range(1, 9):
                pygame.draw.rect(
                    surface,
                    self.board[y_step][x_step][0],
                    self.board[y_step][x_step][1],
                    0,
                )
                # Флаг выделения равен 1 - закрасить поле зелёным.
                if self.board[y_step][x_step][2] == 1:
                    pygame.draw.rect(
                        surface, self.GREEN, self.board[y_step][x_step][1], 0
                    )
                # Флаг выделения равен 2 - нарисовать зелёный круг.
                elif self.board[y_step][x_step][2] == 2:
                    x, y = self.board[y_step][x_step][1].center
                    radius = self.SQUARE_SIZE // 8
                    pygame.gfxdraw.aacircle(surface, x, y, radius, self.GREEN)
                    pygame.gfxdraw.filled_circle(surface, x, y, radius, self.GREEN)
                # Флаг выделения равен 3 - нарисовать по углам поля зелёные прямоугольники.
                elif self.board[y_step][x_step][2] == 3:
                    x = self.board[y_step][x_step][1].x
                    y = self.board[y_step][x_step][1].y
                    rect_left_up = pygame.Rect(
                        x, y, self.SQUARE_SIZE // 8, self.SQUARE_SIZE // 8
                    )
                    rect_left_down = pygame.Rect(
                        x,
                        y + self.SQUARE_SIZE - self.SQUARE_SIZE // 8,
                        self.SQUARE_SIZE // 8,
                        self.SQUARE_SIZE // 8,
                    )
                    rect_right_up = pygame.Rect(
                        x + self.SQUARE_SIZE - self.SQUARE_SIZE // 8,
                        y,
                        self.SQUARE_SIZE // 8,
                        self.SQUARE_SIZE // 8,
                    )
                    rect_right_down = pygame.Rect(
                        x + self.SQUARE_SIZE - self.SQUARE_SIZE // 8,
                        y + self.SQUARE_SIZE - self.SQUARE_SIZE // 8,
                        self.SQUARE_SIZE // 8,
                        self.SQUARE_SIZE // 8,
                    )
                    pygame.draw.rect(surface, self.GREEN, rect_left_up, 0)
                    pygame.draw.rect(surface, self.GREEN, rect_left_down, 0)
                    pygame.draw.rect(surface, self.GREEN, rect_right_up, 0)
                    pygame.draw.rect(surface, self.GREEN, rect_right_down, 0)
                # Слева от доски отображается (1, 2, 3, 4, 5, 6, 7, 8), снизу от доски отображается (a, b, c, d, e, f, g, h).
                if self.mode == "white":
                    if x_step == 1:
                        char_x, char_y = self.board[y_step][x_step][1].center
                        char_x -= self.SQUARE_SIZE * 0.75
                        text = self.FONT.render(
                            convert(x_step, y_step)[1], True, (0, 0, 0)
                        )
                        text_rect = text.get_rect(center=(char_x, char_y))
                        surface.blit(text, text_rect)
                    if y_step == 1:
                        char_x, char_y = self.board[y_step][x_step][1].center
                        char_y += self.SQUARE_SIZE * 0.75
                        text = self.FONT.render(
                            convert(x_step, y_step)[0], True, (0, 0, 0)
                        )
                        text_rect = text.get_rect(center=(char_x, char_y))
                        surface.blit(text, text_rect)
                else:
                    if x_step == 8:
                        char_x, char_y = self.board[y_step][x_step][1].center
                        char_x -= self.SQUARE_SIZE * 0.75
                        text = self.FONT.render(
                            convert(x_step, y_step)[1], True, (0, 0, 0)
                        )
                        text_rect = text.get_rect(center=(char_x, char_y))
                        surface.blit(text, text_rect)
                    if y_step == 8:
                        char_x, char_y = self.board[y_step][x_step][1].center
                        char_y += self.SQUARE_SIZE * 0.75
                        text = self.FONT.render(
                            convert(x_step, y_step)[0], True, (0, 0, 0)
                        )
                        text_rect = text.get_rect(center=(char_x, char_y))
                        surface.blit(text, text_rect)
        for piece in self.human:
            piece.set_rect()
        for piece in self.engine:
            piece.set_rect()
        self.human.draw(surface)
        self.engine.draw(surface)
        if self.position.result != "unknown":
            if self.position.result == "win":
                text = self.RESULT_FONT.render("WIN", True, self.RESULT_COLOR)
            elif self.position.result == "draw":
                text = self.RESULT_FONT.render("DRAW", True, self.RESULT_COLOR)
            elif self.position.result == "loss":
                text = self.RESULT_FONT.render("LOSS", True, self.RESULT_COLOR)
            text_rect = text.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2)
            )
            surface.blit(text, text_rect)
