import pygame
import pygame.gfxdraw
from converter import convert

class Board:

    SQUARE_SIZE = 80
    WHITE = (213, 201, 193)
    BLACK = (128, 74, 38)
    GREEN = (63, 140, 84)
    FONT = pygame.font.Font(None, 30)
    START_POSITION = [["black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_bishop", "black_knight", "black_rook"],
                      ["black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn"],
                      ["nothing", "nothing", "nothing", "nothing", "nothing", "nothing", "nothing", "nothing"],
                      ["nothing", "nothing", "nothing", "nothing", "nothing", "nothing", "nothing", "nothing"],
                      ["nothing", "nothing", "nothing", "nothing", "nothing", "nothing", "nothing", "nothing"],
                      ["nothing", "nothing", "nothing", "nothing", "nothing", "nothing", "nothing", "nothing"],
                      ["white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn"],
                      ["white_rook", "white_knight", "white_bishop", "white_queen", "white_king", "white_bishop", "white_knight", "white_rook"]]

    class Piece(pygame.sprite.Sprite):
    
        def __init__(self, x, y, piece):
            super().__init__()
            self.piece = piece
            original_image = pygame.image.load(f"../assets/pieces/{piece}.png")
            scaled_image = pygame.transform.smoothscale(original_image, (Board.SQUARE_SIZE, Board.SQUARE_SIZE))
            self.image = scaled_image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        
        def move(self, x, y):
            self.rect.x = x
            self.rect.y = y
                
    def __init__(self, center_x, center_y, mode):
        self.board = [[0]*8 for i in range(8)]
        self.mode = mode
        self.clicked = None
        self.player = pygame.sprite.Group()
        self.opponent = pygame.sprite.Group()
        self.start_x = center_x - 4 * self.SQUARE_SIZE
        self.start_y = center_y - 4 * self.SQUARE_SIZE
        cur_pos_x = self.start_x
        cur_pos_y = self.start_y
        for y_step in range(8):
            for x_step in range(8):
                piece = None
                if self.mode == "white":
                    if "white" in self.START_POSITION[y_step][x_step]:
                        piece = Board.Piece(cur_pos_x, cur_pos_y, self.START_POSITION[y_step][x_step])
                        self.player.add(piece)
                    if "black" in self.START_POSITION[y_step][x_step]:
                        piece = Board.Piece(cur_pos_x, cur_pos_y, self.START_POSITION[y_step][x_step])
                        self.opponent.add(piece)
                else:
                    if "white" in self.START_POSITION[y_step][x_step]:
                        if self.START_POSITION[y_step][x_step] == "white_queen":
                            piece = Board.Piece(cur_pos_x, cur_pos_y, "black_king")
                        elif self.START_POSITION[y_step][x_step] == "white_king":
                            piece = Board.Piece(cur_pos_x, cur_pos_y, "black_queen")
                        else:
                            piece = Board.Piece(cur_pos_x, cur_pos_y, "black" + self.START_POSITION[y_step][x_step][5:])
                        self.player.add(piece)
                    if "black" in self.START_POSITION[y_step][x_step]:
                        if self.START_POSITION[y_step][x_step] == "black_queen":
                            piece = Board.Piece(cur_pos_x, cur_pos_y, "white_king")
                        elif self.START_POSITION[y_step][x_step] == "black_king":
                            piece = Board.Piece(cur_pos_x, cur_pos_y, "white_queen")
                        else:
                            piece = Board.Piece(cur_pos_x, cur_pos_y, "white" + self.START_POSITION[y_step][x_step][5:])
                        self.opponent.add(piece)
                self.board[y_step][x_step] = [pygame.Rect(cur_pos_x, cur_pos_y, self.SQUARE_SIZE, self.SQUARE_SIZE), piece, False]
                if x_step == 7:
                    cur_pos_x = self.start_x
                else:
                    cur_pos_x += self.SQUARE_SIZE
            cur_pos_y += self.SQUARE_SIZE

    def click(self, mouse_x, mouse_y):
        mouse_x -= self.start_x
        mouse_y -= self.start_y
        x = mouse_x // self.SQUARE_SIZE
        y = mouse_y // self.SQUARE_SIZE
        if self.clicked != None:
            if self.board[y][x][1] != self.clicked:
                if self.board[y][x][2]:
                    self.board[(self.clicked.rect.y - self.start_y) // self.SQUARE_SIZE][(self.clicked.rect.x - self.start_x) // self.SQUARE_SIZE][1] = None
                    if self.clicked.piece in ["black_pawn", "white_pawn"] and (y == 0 or y == 7):
                        self.player.remove(self.clicked)
                        self.clicked = Board.Piece(self.start_x + x * self.SQUARE_SIZE, self.start_y + y * self.SQUARE_SIZE, self.clicked.piece[:6] + "queen")
                        self.player.add(self.clicked)
                    else:
                        self.clicked.move(self.start_x + x * self.SQUARE_SIZE, self.start_y + y * self.SQUARE_SIZE)
                    if self.board[y][x][1] in self.opponent:
                        self.opponent.remove(self.board[y][x][1])
                    self.board[y][x][1] = self.clicked
                    self.clicked = None
                    for y_step in range(8):
                        for x_step in range(8):
                            self.board[y_step][x_step][2] = False
                    self.player, self.opponent = self.opponent, self.player
                    return
                else:
                    self.clicked = None
                    for y_step in range(8):
                        for x_step in range(8):
                            self.board[y_step][x_step][2] = False
            else:
                self.clicked = None
                for y_step in range(8):
                    for x_step in range(8):
                        self.board[y_step][x_step][2] = False
                return
        if self.board[y][x][1] in self.player:
            self.clicked = self.board[y][x][1]
            current_piece = self.clicked.piece
            self.board[y][x][2] = True
            if current_piece == "black_pawn":
                if self.mode == "white":
                    if y + 1 < 8:
                        if self.board[y + 1][x][1] == None:
                            self.board[y + 1][x][2] = True
                            if y + 2 == 3 and self.board[y + 2][x][1] == None:
                                self.board[y + 2][x][2] = True
                        if x - 1 >= 0 and self.board[y + 1][x - 1][1] in self.opponent:
                            self.board[y + 1][x - 1][2] = True
                        if x + 1 < 8 and self.board[y + 1][x + 1][1] in self.opponent:
                            self.board[y + 1][x + 1][2] = True
                else:
                    if y - 1 >= 0:
                        if self.board[y - 1][x][1] == None:
                            self.board[y - 1][x][2] = True
                            if y - 2 == 4 and self.board[y - 2][x][1] == None:
                                self.board[y - 2][x][2] = True
                        if x - 1 >= 0 and self.board[y - 1][x - 1][1] in self.opponent:
                            self.board[y - 1][x - 1][2] = True
                        if x + 1 < 8 and self.board[y - 1][x + 1][1] in self.opponent:
                            self.board[y - 1][x + 1][2] = True
            if current_piece == "white_pawn":
                if self.mode == "white":
                    if y - 1 >= 0:
                        if self.board[y - 1][x][1] == None:
                            self.board[y - 1][x][2] = True
                            if y - 2 == 4 and self.board[y - 2][x][1] == None:
                                self.board[y - 2][x][2] = True
                        if x - 1 >= 0 and self.board[y - 1][x - 1][1] in self.opponent:
                            self.board[y - 1][x - 1][2] = True
                        if x + 1 < 8 and self.board[y - 1][x + 1][1] in self.opponent:
                            self.board[y - 1][x + 1][2] = True
                else:
                    if y + 1 < 8:
                        if self.board[y + 1][x][1] == None:
                            self.board[y + 1][x][2] = True
                            if y + 2 == 3 and self.board[y + 2][x][1] == None:
                                self.board[y + 2][x][2] = True
                        if x - 1 >= 0 and self.board[y + 1][x - 1][1] in self.opponent:
                            self.board[y + 1][x - 1][2] = True
                        if x + 1 < 8 and self.board[y + 1][x + 1][1] in self.opponent:
                            self.board[y + 1][x + 1][2] = True
            if current_piece in ["black_knight", "white_knight"]:
                if y + 2 < 8 and x + 1 < 8 and self.board[y + 2][x + 1][1] not in self.player:
                    self.board[y + 2][x + 1][2] = True
                if y + 1 < 8 and x + 2 < 8 and self.board[y + 1][x + 2][1] not in self.player:
                    self.board[y + 1][x + 2][2] = True
                if y - 1 >= 0 and x + 2 < 8 and self.board[y - 1][x + 2][1] not in self.player:
                    self.board[y - 1][x + 2][2] = True
                if y - 1 >= 0 and x + 2 < 8 and self.board[y - 1][x + 2][1] not in self.player:
                    self.board[y - 1][x + 2][2] = True    
                if y - 2 >= 0 and x + 1 < 8 and self.board[y - 2][x + 1][1] not in self.player:
                    self.board[y - 2][x + 1][2] = True
                if y - 2 >= 0 and x - 1 >= 0 and self.board[y - 2][x - 1][1] not in self.player:
                    self.board[y - 2][x - 1][2] = True
                if y - 1 >= 0 and x - 2 >= 0 and self.board[y - 1][x - 2][1] not in self.player:
                    self.board[y - 1][x - 2][2] = True
                if y + 1 < 8 and x - 2 >= 0 and self.board[y + 1][x - 2][1] not in self.player:
                    self.board[y + 1][x - 2][2] = True
                if y + 2 < 8 and x - 1 >= 0 and self.board[y + 2][x - 1][1] not in self.player:
                    self.board[y + 2][x - 1][2] = True
            if current_piece in ["black_king", "white_king"]:
                if y + 1 < 8 and self.board[y + 1][x][1] not in self.player:
                    self.board[y + 1][x][2] = True
                if y - 1 >= 0 and self.board[y - 1][x][1] not in self.player:
                    self.board[y - 1][x][2] = True
                if x + 1 < 8 and self.board[y][x + 1][1] not in self.player:
                    self.board[y][x + 1][2] = True
                if x - 1 >= 0 and self.board[y][x - 1][1] not in self.player:
                    self.board[y][x - 1][2] = True
                if y + 1 < 8 and x + 1 < 8 and self.board[y + 1][x + 1][1] not in self.player:
                    self.board[y + 1][x + 1][2] = True
                if y - 1 >= 0 and x - 1 >= 0 and self.board[y - 1][x - 1][1] not in self.player:
                    self.board[y - 1][x - 1][2] = True
                if y + 1 < 8 and x - 1 >= 0 and self.board[y + 1][x - 1][1] not in self.player:
                    self.board[y + 1][x - 1][2] = True
                if y - 1 >= 0 and x + 1 < 8 and self.board[y - 1][x + 1][1] not in self.player:
                    self.board[y - 1][x + 1][2] = True
            if current_piece in ["black_queen", "white_queen", "black_rook", "white_rook"]:
                for y_step in range(1, 8):
                    if y + y_step < 8 and self.board[y + y_step][x][1] not in self.player:
                        self.board[y + y_step][x][2] = True
                        if self.board[y + y_step][x][1] in self.opponent:
                            break
                    else:
                        break
                for y_step in range(1, 8):
                    if y - y_step >= 0 and self.board[y - y_step][x][1] not in self.player:
                        self.board[y - y_step][x][2] = True
                        if self.board[y - y_step][x][1] in self.opponent:
                            break
                    else:
                        break
                for x_step in range(1, 8):
                    if x + x_step < 8 and self.board[y][x + x_step][1] not in self.player:
                        self.board[y][x + x_step][2] = True
                        if self.board[y][x + x_step][1] in self.opponent:
                            break
                    else:
                        break
                for x_step in range(1, 8):
                    if x - x_step >= 0 and self.board[y][x - x_step][1] not in self.player:
                        self.board[y][x - x_step][2] = True
                        if self.board[y][x - x_step][1] in self.opponent:
                            break
                    else:
                        break
            if current_piece in ["black_queen", "white_queen", "black_bishop", "white_bishop"]:
                for step in range(1, 8):
                    if y + step < 8 and x + step < 8 and self.board[y + step][x + step][1] not in self.player:
                        self.board[y + step][x + step][2] = True
                        if self.board[y + step][x + step][1] in self.opponent:
                            break
                    else:
                        break
                for step in range(1, 8):
                    if y - step >= 0 and x - step >= 0 and self.board[y - step][x - step][1] not in self.player:
                        self.board[y - step][x - step][2] = True
                        if self.board[y - step][x - step][1] in self.opponent:
                            break
                    else:
                        break
                for step in range(1, 8):
                    if y + step < 8 and x - step >= 0 and self.board[y + step][x - step][1] not in self.player:
                        self.board[y + step][x - step][2] = True
                        if self.board[y + step][x - step][1] in self.opponent:
                            break
                    else:
                        break
                for step in range(1, 8):
                    if y - step >= 0 and x + step < 8 and self.board[y - step][x + step][1] not in self.player:
                        self.board[y - step][x + step][2] = True
                        if self.board[y - step][x + step][1] in self.opponent:
                            break
                    else:
                        break

    def draw(self, surface):
        cur_color = self.WHITE
        for y_step in range(8):
            for x_step in range(8):
                pygame.draw.rect(surface, cur_color, self.board[y_step][x_step][0], 0)
                if self.board[y_step][x_step][2]:
                    if self.board[y_step][x_step][1] == self.clicked:
                        pygame.draw.rect(surface, self.GREEN, self.board[y_step][x_step][0], 0)
                    elif self.board[y_step][x_step][1] in self.opponent:
                        x = self.board[y_step][x_step][0].x
                        y = self.board[y_step][x_step][0].y
                        rect_left_up = pygame.Rect(x, y, self.SQUARE_SIZE // 8, self.SQUARE_SIZE // 8)
                        rect_left_down = pygame.Rect(x, y + self.SQUARE_SIZE - self.SQUARE_SIZE // 8, self.SQUARE_SIZE // 8, self.SQUARE_SIZE // 8)
                        rect_right_up = pygame.Rect(x + self.SQUARE_SIZE - self.SQUARE_SIZE // 8, y, self.SQUARE_SIZE // 8, self.SQUARE_SIZE // 8)
                        rect_right_down = pygame.Rect(x + self.SQUARE_SIZE - self.SQUARE_SIZE // 8, y + self.SQUARE_SIZE - self.SQUARE_SIZE // 8, self.SQUARE_SIZE // 8, self.SQUARE_SIZE // 8)
                        pygame.draw.rect(surface, self.GREEN, rect_left_up, 0)
                        pygame.draw.rect(surface, self.GREEN, rect_left_down, 0)
                        pygame.draw.rect(surface, self.GREEN, rect_right_up, 0)
                        pygame.draw.rect(surface, self.GREEN, rect_right_down, 0)
                    else:
                        x, y = self.board[y_step][x_step][0].center
                        radius = self.SQUARE_SIZE // 8
                        pygame.gfxdraw.aacircle(surface, x, y, radius, self.GREEN)
                        pygame.gfxdraw.filled_circle(surface, x, y, radius, self.GREEN)
                if x_step == 0:
                    char_x, char_y = self.board[y_step][x_step][0].center
                    char_x -= self.SQUARE_SIZE * 0.75
                    text = self.FONT.render(convert(x_step, y_step, self.mode)[1], True, (0, 0, 0))
                    text_rect = text.get_rect(center = (char_x, char_y))
                    surface.blit(text, text_rect)
                if y_step == 7:
                    char_x, char_y = self.board[y_step][x_step][0].center
                    char_y += self.SQUARE_SIZE * 0.75
                    text = self.FONT.render(convert(x_step, y_step, self.mode)[0], True, (0, 0, 0))
                    text_rect = text.get_rect(center = (char_x, char_y))
                    surface.blit(text, text_rect)
                if x_step < 7:
                    if cur_color == self.WHITE:
                        cur_color = self.BLACK
                    else:
                        cur_color = self.WHITE
        self.player.draw(surface)
        self.opponent.draw(surface)
