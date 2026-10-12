import copy

import pygame

from converter import convert, parse_move


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
                if piece != None and piece.piece_type == "rook" and piece.move_cnt == 0:
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
                if piece != None and piece.piece_type == "rook" and piece.move_cnt == 0:
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
                if piece != None and piece.piece_type == "rook" and piece.move_cnt == 0:
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
                if piece != None and piece.piece_type == "rook" and piece.move_cnt == 0:
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
                            opponent_start, opponent_end = parse_move(self.moves[-1])
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
                    if self.is_occupied(square, opponent) or square in self.en_passant(
                        player
                    ):
                        squares.append(square)
            if piece.color == "white" and (
                1 <= piece.square[0] + 1 <= 8
                and self.is_occupied([piece.square[0] + 1, piece.square[1]], player)
                == False
                and self.is_occupied([piece.square[0] + 1, piece.square[1]], opponent)
                == False
            ):
                squares.append([piece.square[0] + 1, piece.square[1]])
                if (
                    piece.square[0] == 2
                    and self.is_occupied([piece.square[0] + 2, piece.square[1]], player)
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
                and self.is_occupied([piece.square[0] - 1, piece.square[1]], opponent)
                == False
            ):
                squares.append([piece.square[0] - 1, piece.square[1]])
                if (
                    piece.square[0] == 7
                    and self.is_occupied([piece.square[0] - 2, piece.square[1]], player)
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
