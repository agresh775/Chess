import copy
import pygame
import pygame.gfxdraw

from converter import convert, parse_move


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
            new = Board.Piece.__new__(Board.Piece)
            new.__dict__.update(self.__dict__)
            new.__dict__["square"] = copy.copy(self.square)
            return new

        def set_rect(self):
            y, x = self.square
            self.rect.center = self.board.board[y][x][1].center

    class Position:
        def __init__(self, board):
            self.board = board
            self.move_count = 0
            self.fifty_move_count = 0
            self.moves = []
            self.positions = []
            self.result = "unknown"
            self.board.Piece(
                board,
                "white",
                "rook",
                [1, 1],
                [
                    [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
                    [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
                    [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]],
                    [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
                ],
            )
            self.board.Piece(
                board,
                "white",
                "knight",
                [1, 2],
                [
                    [[1, -2]],
                    [[1, 2]],
                    [[2, -1]],
                    [[2, 1]],
                    [[-1, 2]],
                    [[-1, -2]],
                    [[-2, 1]],
                    [[-2, -1]],
                ],
            )
            self.board.Piece(
                board,
                "white",
                "bishop",
                [1, 3],
                [
                    [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
                    [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
                    [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]],
                    [
                        [-1, -1],
                        [-2, -2],
                        [-3, -3],
                        [-4, -4],
                        [-5, -5],
                        [-6, -6],
                        [-7, -7],
                    ],
                ],
            )
            self.board.Piece(
                board,
                "white",
                "queen",
                [1, 4],
                [
                    [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
                    [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
                    [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]],
                    [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
                    [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
                    [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
                    [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]],
                    [
                        [-1, -1],
                        [-2, -2],
                        [-3, -3],
                        [-4, -4],
                        [-5, -5],
                        [-6, -6],
                        [-7, -7],
                    ],
                ],
            )
            self.board.Piece(
                board,
                "white",
                "king",
                [1, 5],
                [
                    [[0, 1]],
                    [[1, -1]],
                    [[1, 0]],
                    [[1, 1]],
                    [[0, -1]],
                    [[-1, -1]],
                    [[-1, 0]],
                    [[-1, 1]],
                ],
            )
            self.board.Piece(
                board,
                "white",
                "bishop",
                [1, 6],
                [
                    [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
                    [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
                    [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]],
                    [
                        [-1, -1],
                        [-2, -2],
                        [-3, -3],
                        [-4, -4],
                        [-5, -5],
                        [-6, -6],
                        [-7, -7],
                    ],
                ],
            )
            self.board.Piece(
                board,
                "white",
                "knight",
                [1, 7],
                [
                    [[1, -2]],
                    [[1, 2]],
                    [[2, -1]],
                    [[2, 1]],
                    [[-1, 2]],
                    [[-1, -2]],
                    [[-2, 1]],
                    [[-2, -1]],
                ],
            )
            self.board.Piece(
                board,
                "white",
                "rook",
                [1, 8],
                [
                    [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
                    [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
                    [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]],
                    [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
                ],
            )
            self.board.Piece(board, "white", "pawn", [2, 1], [[[1, -1]], [[1, 1]]])
            self.board.Piece(board, "white", "pawn", [2, 2], [[[1, -1]], [[1, 1]]])
            self.board.Piece(board, "white", "pawn", [2, 3], [[[1, -1]], [[1, 1]]])
            self.board.Piece(board, "white", "pawn", [2, 4], [[[1, -1]], [[1, 1]]])
            self.board.Piece(board, "white", "pawn", [2, 5], [[[1, -1]], [[1, 1]]])
            self.board.Piece(board, "white", "pawn", [2, 6], [[[1, -1]], [[1, 1]]])
            self.board.Piece(board, "white", "pawn", [2, 7], [[[1, -1]], [[1, 1]]])
            self.board.Piece(board, "white", "pawn", [2, 8], [[[1, -1]], [[1, 1]]])
            self.board.Piece(board, "black", "pawn", [7, 1], [[[-1, -1]], [[-1, 1]]])
            self.board.Piece(board, "black", "pawn", [7, 2], [[[-1, -1]], [[-1, 1]]])
            self.board.Piece(board, "black", "pawn", [7, 3], [[[-1, -1]], [[-1, 1]]])
            self.board.Piece(board, "black", "pawn", [7, 4], [[[-1, -1]], [[-1, 1]]])
            self.board.Piece(board, "black", "pawn", [7, 5], [[[-1, -1]], [[-1, 1]]])
            self.board.Piece(board, "black", "pawn", [7, 6], [[[-1, -1]], [[-1, 1]]])
            self.board.Piece(board, "black", "pawn", [7, 7], [[[-1, -1]], [[-1, 1]]])
            self.board.Piece(board, "black", "pawn", [7, 8], [[[-1, -1]], [[-1, 1]]])
            self.board.Piece(
                board,
                "black",
                "rook",
                [8, 1],
                [
                    [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
                    [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
                    [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]],
                    [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
                ],
            )
            self.board.Piece(
                board,
                "black",
                "knight",
                [8, 2],
                [
                    [[1, -2]],
                    [[1, 2]],
                    [[2, -1]],
                    [[2, 1]],
                    [[-1, 2]],
                    [[-1, -2]],
                    [[-2, 1]],
                    [[-2, -1]],
                ],
            )
            self.board.Piece(
                board,
                "black",
                "bishop",
                [8, 3],
                [
                    [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
                    [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
                    [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]],
                    [
                        [-1, -1],
                        [-2, -2],
                        [-3, -3],
                        [-4, -4],
                        [-5, -5],
                        [-6, -6],
                        [-7, -7],
                    ],
                ],
            )
            self.board.Piece(
                board,
                "black",
                "queen",
                [8, 4],
                [
                    [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
                    [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
                    [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]],
                    [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
                    [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
                    [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
                    [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]],
                    [
                        [-1, -1],
                        [-2, -2],
                        [-3, -3],
                        [-4, -4],
                        [-5, -5],
                        [-6, -6],
                        [-7, -7],
                    ],
                ],
            )
            self.board.Piece(
                board,
                "black",
                "king",
                [8, 5],
                [
                    [[0, 1]],
                    [[1, -1]],
                    [[1, 0]],
                    [[1, 1]],
                    [[0, -1]],
                    [[-1, -1]],
                    [[-1, 0]],
                    [[-1, 1]],
                ],
            )
            self.board.Piece(
                board,
                "black",
                "bishop",
                [8, 6],
                [
                    [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
                    [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
                    [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]],
                    [
                        [-1, -1],
                        [-2, -2],
                        [-3, -3],
                        [-4, -4],
                        [-5, -5],
                        [-6, -6],
                        [-7, -7],
                    ],
                ],
            )
            self.board.Piece(
                board,
                "black",
                "knight",
                [8, 7],
                [
                    [[1, -2]],
                    [[1, 2]],
                    [[2, -1]],
                    [[2, 1]],
                    [[-1, 2]],
                    [[-1, -2]],
                    [[-2, 1]],
                    [[-2, -1]],
                ],
            )
            self.board.Piece(
                board,
                "black",
                "rook",
                [8, 8],
                [
                    [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
                    [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
                    [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]],
                    [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
                ],
            )
            self.append_position()

        def get(self):
            return self.moves

        def append_position(self):
            human_pieces_copy = pygame.sprite.Group()
            engine_pieces_copy = pygame.sprite.Group()
            for piece in self.board.human:
                piece_copy = copy.copy(piece)
                human_pieces_copy.add(piece_copy)
            for piece in self.board.engine:
                piece_copy = copy.copy(piece)
                engine_pieces_copy.add(piece_copy)
            self.positions.append(
                [
                    human_pieces_copy,
                    engine_pieces_copy,
                    self.move_count,
                    self.fifty_move_count,
                ]
            )

        def pop_position(self):
            self.positions.pop()
            human_pieces_copy = pygame.sprite.Group()
            engine_pieces_copy = pygame.sprite.Group()
            for piece in self.positions[-1][0]:
                piece_copy = copy.copy(piece)
                human_pieces_copy.add(piece_copy)
            for piece in self.positions[-1][1]:
                piece_copy = copy.copy(piece)
                engine_pieces_copy.add(piece_copy)
            self.board.human = human_pieces_copy
            self.board.engine = engine_pieces_copy
            self.move_count = self.positions[-1][2]
            self.fifty_move_count = self.positions[-1][3]
            self.moves.pop()

        def move(self, move, player):
            if player == "human":
                opponent = "engine"
                player_pieces = self.board.human
                opponent_pieces = self.board.engine
            else:
                opponent = "human"
                player_pieces = self.board.engine
                opponent_pieces = self.board.human
            start, end = parse_move(move)
            piece = self.find_piece(start, player)
            if piece.piece_type == "pawn":
                self.fifty_move_count = 0
                if piece.color == "white":
                    if end[0] == 8:
                        queen = self.board.Piece(
                            self.board,
                            "white",
                            "queen",
                            end,
                            [
                                [
                                    [1, 0],
                                    [2, 0],
                                    [3, 0],
                                    [4, 0],
                                    [5, 0],
                                    [6, 0],
                                    [7, 0],
                                ],
                                [
                                    [0, 1],
                                    [0, 2],
                                    [0, 3],
                                    [0, 4],
                                    [0, 5],
                                    [0, 6],
                                    [0, 7],
                                ],
                                [
                                    [-1, 0],
                                    [-2, 0],
                                    [-3, 0],
                                    [-4, 0],
                                    [-5, 0],
                                    [-6, 0],
                                    [-7, 0],
                                ],
                                [
                                    [0, -1],
                                    [0, -2],
                                    [0, -3],
                                    [0, -4],
                                    [0, -5],
                                    [0, -6],
                                    [0, -7],
                                ],
                                [
                                    [1, 1],
                                    [2, 2],
                                    [3, 3],
                                    [4, 4],
                                    [5, 5],
                                    [6, 6],
                                    [7, 7],
                                ],
                                [
                                    [1, -1],
                                    [2, -2],
                                    [3, -3],
                                    [4, -4],
                                    [5, -5],
                                    [6, -6],
                                    [7, -7],
                                ],
                                [
                                    [-1, 1],
                                    [-2, 2],
                                    [-3, 3],
                                    [-4, 4],
                                    [-5, 5],
                                    [-6, 6],
                                    [-7, 7],
                                ],
                                [
                                    [-1, -1],
                                    [-2, -2],
                                    [-3, -3],
                                    [-4, -4],
                                    [-5, -5],
                                    [-6, -6],
                                    [-7, -7],
                                ],
                            ],
                        )
                        queen.move_cnt = piece.move_cnt + 1
                        player_pieces.remove(piece)
                        player_pieces.add(queen)
                    elif end in self.en_passant(player):
                        opponent_pieces.remove(
                            self.find_piece([end[0] - 1, end[1]], opponent)
                        )
                else:
                    if end[0] == 1:
                        queen = self.board.Piece(
                            self.board,
                            "black",
                            "queen",
                            end,
                            [
                                [
                                    [1, 0],
                                    [2, 0],
                                    [3, 0],
                                    [4, 0],
                                    [5, 0],
                                    [6, 0],
                                    [7, 0],
                                ],
                                [
                                    [0, 1],
                                    [0, 2],
                                    [0, 3],
                                    [0, 4],
                                    [0, 5],
                                    [0, 6],
                                    [0, 7],
                                ],
                                [
                                    [-1, 0],
                                    [-2, 0],
                                    [-3, 0],
                                    [-4, 0],
                                    [-5, 0],
                                    [-6, 0],
                                    [-7, 0],
                                ],
                                [
                                    [0, -1],
                                    [0, -2],
                                    [0, -3],
                                    [0, -4],
                                    [0, -5],
                                    [0, -6],
                                    [0, -7],
                                ],
                                [
                                    [1, 1],
                                    [2, 2],
                                    [3, 3],
                                    [4, 4],
                                    [5, 5],
                                    [6, 6],
                                    [7, 7],
                                ],
                                [
                                    [1, -1],
                                    [2, -2],
                                    [3, -3],
                                    [4, -4],
                                    [5, -5],
                                    [6, -6],
                                    [7, -7],
                                ],
                                [
                                    [-1, 1],
                                    [-2, 2],
                                    [-3, 3],
                                    [-4, 4],
                                    [-5, 5],
                                    [-6, 6],
                                    [-7, 7],
                                ],
                                [
                                    [-1, -1],
                                    [-2, -2],
                                    [-3, -3],
                                    [-4, -4],
                                    [-5, -5],
                                    [-6, -6],
                                    [-7, -7],
                                ],
                            ],
                        )
                        queen.move_cnt = piece.move_cnt + 1
                        player_pieces.remove(piece)
                        player_pieces.add(queen)
                    elif end in self.en_passant(player):
                        opponent_pieces.remove(
                            self.find_piece([end[0] + 1, end[1]], opponent)
                        )
            elif piece.piece_type == "king":
                if end[1] - start[1] == 2:
                    rook = self.find_piece([start[0], start[1] + 3], player)
                    rook.square[1] -= 2
                    rook.move_cnt += 1
                elif end[1] - start[1] == -2:
                    rook = self.find_piece([start[0], start[1] - 4], player)
                    rook.square[1] += 3
                    rook.move_cnt += 1
            piece.square = end
            piece.move_cnt += 1
            piece = self.find_piece(end, opponent)
            if piece is not None:
                self.fifty_move_count = 0
                opponent_pieces.remove(piece)
            self.move_count += 1
            self.fifty_move_count += 1
            self.moves.append(move)

        def check_end(self, player):
            if self.check_checkmate(player) == True:
                if player == "engine":
                    self.result = "win"
                elif player == "human":
                    self.result = "loss"
            elif self.check_draw(player) == True:
                self.result = "draw"
            else:
                self.result = "unknown"

        def check_check(self, player):
            if player == "human":
                opponent = "engine"
                player_pieces = self.board.human
            else:
                opponent = "human"
                player_pieces = self.board.engine
            for piece in player_pieces:
                if piece.piece_type == "king":
                    king = piece
                    break
            return self.is_controlled(king.square, opponent)

        def check_checkmate(self, player):
            if player == "human":
                player_pieces = self.board.human
            else:
                player_pieces = self.board.engine
            if self.check_check(player) == False:
                return False
            available_moves = []
            for piece in player_pieces:
                for square in self.available_squares(piece, player):
                    available_moves.append(
                        convert(piece.square[1], piece.square[0])
                        + convert(square[1], square[0])
                    )
            for move in available_moves:
                flag = False
                self.move(move, player)
                self.append_position()
                flag = self.check_check(player)
                self.pop_position()
                if flag == False:
                    return False
            return True

        def check_draw(self, player):
            if self.fifty_move_count == 50:
                return True
            if player == "human":
                player_pieces = self.board.human
            else:
                player_pieces = self.board.engine
            stalemate_flag = True
            for piece in player_pieces:
                stalemate_flag = stalemate_flag and (
                    len(self.available_squares(piece, player)) == 0
                )
            if stalemate_flag:
                return True
            set1 = set()
            set2 = set()
            for piece in self.board.human:
                set1.add(piece.piece_type)
            for piece in self.board.engine:
                set2.add(piece.piece_type)
            return (
                set1 == {"king"}
                and set2 == {"king"}
                or set1 == {"king"}
                and set2 == {"king", "knight"}
                or set1 == {"king", "knight"}
                and set2 == {"king"}
                or set1 == {"king"}
                and set2 == {"king", "bishop"}
                or set1 == {"king", "bishop"}
                and set2 == {"king"}
            )

        def is_controlled(self, square, player):
            if player == "human":
                player_pieces = self.board.human
            else:
                player_pieces = self.board.engine
            for piece in player_pieces:
                if square in self.controlled_squares(piece, player):
                    return True
            return False

        def is_occupied(self, square, player):
            if player == "human":
                player_pieces = self.board.human
            else:
                player_pieces = self.board.engine
            for piece in player_pieces:
                if piece.square == square:
                    return True
            return False

        def controlled_squares(self, piece, player):
            if player == "human":
                opponent = "engine"
            else:
                opponent = "human"
            squares = []
            for ops in piece.operations:
                for op in ops:
                    square = [piece.square[0] + op[0], piece.square[1] + op[1]]
                    if 1 <= square[0] <= 8 and 1 <= square[1] <= 8:
                        squares.append(square)
                        if self.is_occupied(square, player) or self.is_occupied(
                            square, opponent
                        ):
                            break
                    else:
                        break
            return squares

        def find_piece(self, square, player):
            if player == "human":
                player_pieces = self.board.human
            else:
                player_pieces = self.board.engine
            for piece in player_pieces:
                if piece.square == square:
                    return piece

        def castling(self, king, side, player):
            if player == "human":
                opponent = "engine"
            else:
                opponent = "human"
            if king.color == "white":
                if (
                    king.square != [1, 5]
                    or self.is_controlled([1, 5], opponent)
                    or king.move_cnt > 0
                ):
                    return False
                if side == "kingside":
                    if (
                        self.is_occupied([1, 6], player)
                        or self.is_occupied([1, 6], opponent)
                        or self.is_occupied([1, 7], player)
                        or self.is_occupied([1, 7], opponent)
                        or self.is_controlled([1, 6], opponent)
                        or self.is_controlled([1, 7], opponent)
                    ):
                        return False
                    piece = self.find_piece([1, 8], player)
                    if piece.piece_type == "rook" and piece.move_cnt == 0:
                        return True
                elif side == "queenside":
                    if (
                        self.is_occupied([1, 4], player)
                        or self.is_occupied([1, 4], opponent)
                        or self.is_occupied([1, 3], player)
                        or self.is_occupied([1, 3], opponent)
                        or self.is_occupied([1, 2], player)
                        or self.is_occupied([1, 2], opponent)
                        or self.is_controlled([1, 4], opponent)
                        or self.is_controlled([1, 3], opponent)
                    ):
                        return False
                    piece = self.find_piece([1, 1], player)
                    if piece.piece_type == "rook" and piece.move_cnt == 0:
                        return True
            elif king.color == "black":
                if (
                    king.square != [8, 5]
                    or self.is_controlled([8, 5], opponent)
                    or king.move_cnt > 0
                ):
                    return False
                if side == "kingside":
                    if (
                        self.is_occupied([8, 6], player)
                        or self.is_occupied([8, 6], opponent)
                        or self.is_occupied([8, 7], player)
                        or self.is_occupied([8, 7], opponent)
                        or self.is_controlled([8, 6], opponent)
                        or self.is_controlled([8, 7], opponent)
                    ):
                        return False
                    piece = self.find_piece([8, 8], player)
                    if piece.piece_type == "rook" and piece.move_cnt == 0:
                        return True
                elif side == "queenside":
                    if (
                        self.is_occupied([8, 4], player)
                        or self.is_occupied([8, 4], opponent)
                        or self.is_occupied([8, 3], player)
                        or self.is_occupied([8, 3], opponent)
                        or self.is_occupied([8, 2], player)
                        or self.is_occupied([8, 2], opponent)
                        or self.is_controlled([8, 4], opponent)
                        or self.is_controlled([8, 3], opponent)
                    ):
                        return False
                    piece = self.find_piece([8, 1], player)
                    if piece.piece_type == "rook" and piece.move_cnt == 0:
                        return True
            return False

        def en_passant(self, player):
            if player == "human":
                opponent = "engine"
                player_pieces = self.board.human
            else:
                opponent = "human"
                player_pieces = self.board.engine
            squares = []
            for piece in player_pieces:
                if piece.piece_type == "pawn":
                    for ops in piece.operations:
                        for op in ops:
                            square = [piece.square[0] + op[0], piece.square[1] + op[1]]
                            if len(self.moves) > 0:
                                opponent_start, opponent_end = parse_move(
                                    self.moves[-1]
                                )
                                pawn_flag = False
                                opponent_piece = self.find_piece(opponent_end, opponent)
                                if (
                                    opponent_piece is not None
                                    and opponent_piece.piece_type == "pawn"
                                ):
                                    pawn_flag = True
                                if (
                                    piece.color == "white"
                                    and pawn_flag == True
                                    and opponent_start[0] == 7
                                    and opponent_end[0] == 5
                                    and piece.square[0] == 5
                                    and opponent_end[1] == square[1]
                                ) or (
                                    piece.color == "black"
                                    and pawn_flag == True
                                    and opponent_start[0] == 2
                                    and opponent_end[0] == 4
                                    and piece.square[0] == 4
                                    and opponent_end[1] == square[1]
                                ):
                                    squares.append(square)
            return squares

        def available_squares(self, piece, player):
            if player == "human":
                opponent = "engine"
            else:
                opponent = "human"
            squares = []
            if piece.piece_type == "king":
                if self.castling(piece, "kingside", player):
                    squares.append([piece.square[0], 7])
                if self.castling(piece, "queenside", player):
                    squares.append([piece.square[0], 3])
                for square in self.controlled_squares(piece, player):
                    if (
                        self.is_controlled(square, opponent) == False
                        and self.is_occupied(square, player) == False
                    ):
                        squares.append(square)
            elif piece.piece_type == "pawn":
                for ops in piece.operations:
                    for op in ops:
                        square = [piece.square[0] + op[0], piece.square[1] + op[1]]
                        if self.is_occupied(
                            square, opponent
                        ) or square in self.en_passant(player):
                            squares.append(square)
                if piece.color == "white" and (
                    1 <= piece.square[0] + 1 <= 8
                    and self.is_occupied([piece.square[0] + 1, piece.square[1]], player)
                    == False
                    and self.is_occupied(
                        [piece.square[0] + 1, piece.square[1]], opponent
                    )
                    == False
                ):
                    squares.append([piece.square[0] + 1, piece.square[1]])
                    if (
                        piece.square[0] == 2
                        and self.is_occupied(
                            [piece.square[0] + 2, piece.square[1]], player
                        )
                        == False
                        and self.is_occupied(
                            [piece.square[0] + 2, piece.square[1]], opponent
                        )
                        == False
                    ):
                        squares.append([piece.square[0] + 2, piece.square[1]])
                elif piece.color == "black" and (
                    1 <= piece.square[0] - 1 <= 8
                    and self.is_occupied([piece.square[0] - 1, piece.square[1]], player)
                    == False
                    and self.is_occupied(
                        [piece.square[0] - 1, piece.square[1]], opponent
                    )
                    == False
                ):
                    squares.append([piece.square[0] - 1, piece.square[1]])
                    if (
                        piece.square[0] == 7
                        and self.is_occupied(
                            [piece.square[0] - 2, piece.square[1]], player
                        )
                        == False
                        and self.is_occupied(
                            [piece.square[0] - 2, piece.square[1]], opponent
                        )
                        == False
                    ):
                        squares.append([piece.square[0] - 2, piece.square[1]])
            else:
                for square in self.controlled_squares(piece, player):
                    if self.find_piece(square, player) is not None:
                        continue
                    squares.append(square)
            return squares

    def __init__(self, screen_width, screen_height, mode):
        center_x, center_y = screen_width // 2, screen_height // 2
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board = [[None] * 9 for i in range(9)]
        self.mode = mode
        self.human = pygame.sprite.Group()
        self.engine = pygame.sprite.Group()
        self.position = self.Position(self)
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
        return self.screen_height - y

    def reset_flags(self):
        for y_step in range(1, 9):
            for x_step in range(1, 9):
                self.board[y_step][x_step][2] = 0

    def click(self, mouse_x, mouse_y):
        mouse_y = self.convert_y(mouse_y)
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
        elif self.board[y][x][2] == 1:
            self.reset_flags()
        elif self.position.find_piece([y, x], "human") is not None:
            self.reset_flags()
            self.board[y][x][2] = 1
            for square in self.position.available_squares(
                self.position.find_piece([y, x], "human"), "human"
            ):
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
                if self.board[y_step][x_step][2] == 1:
                    pygame.draw.rect(
                        surface, self.GREEN, self.board[y_step][x_step][1], 0
                    )
                elif self.board[y_step][x_step][2] == 2:
                    x, y = self.board[y_step][x_step][1].center
                    radius = self.SQUARE_SIZE // 8
                    pygame.gfxdraw.aacircle(surface, x, y, radius, self.GREEN)
                    pygame.gfxdraw.filled_circle(surface, x, y, radius, self.GREEN)
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
