#include <algorithm>
#include <array>
#include <iostream>
#include <optional>
#include <random>
#include <sstream>
#include <string>
#include <vector>

struct Position {
    struct Piece {
        enum class Type { Pawn, Rook, Knight, Bishop, Queen, King };
        enum class Color { White, Black };

        Type type;
        Color color;
        std::pair<int, int> square;
        std::vector<std::vector<std::pair<int, int>>> operations;
        bool is_captured;
        int move_cnt;
    };

    Piece::Color player;
    std::vector<Piece> white_pieces, black_pieces;
    std::vector<std::string> moves;
    std::vector<std::pair<std::vector<Piece>, std::vector<Piece>>> positions;
    bool white_kingside_flag, white_queenside_flag, black_kingside_flag, black_queenside_flag;

    void StartPosition(std::string fen) {
        this->white_pieces.clear();
        this->black_pieces.clear();
        this->moves.clear();
        this->positions.clear();
        this->white_kingside_flag = false;
        this->white_queenside_flag = false;
        this->black_kingside_flag = false;
        this->black_queenside_flag = false;
        std::string token;
        std::istringstream iss(fen);
        iss >> token;
        int y = 8, x = 1;
        for (auto ch : token) {
            if (ch == '/') {
                y--;
                x = 1;
                continue;
            } else if (1 <= static_cast<int>(ch) - static_cast<int>('0') &&
                       static_cast<int>(ch) - static_cast<int>('0') <= 8) {
                x += static_cast<int>(ch) - static_cast<int>('0');
                continue;
            } else if (ch == 'r') {
                Piece rook = {Piece::Type::Rook,
                              Piece::Color::Black,
                              {y, x},
                              {{{1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}},
                               {{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}},
                               {{-1, 0}, {-2, 0}, {-3, 0}, {-4, 0}, {-5, 0}, {-6, 0}, {-7, 0}},
                               {{0, -1}, {0, -2}, {0, -3}, {0, -4}, {0, -5}, {0, -6}, {0, -7}}},
                              false,
                              0};
                this->black_pieces.push_back(rook);
            } else if (ch == 'n') {
                Piece knight = {
                    Piece::Type::Knight,
                    Piece::Color::Black,
                    {y, x},
                    {{{1, -2}}, {{1, 2}}, {{2, -1}}, {{2, 1}}, {{-1, 2}}, {{-1, -2}}, {{-2, 1}}, {{-2, -1}}},
                    false,
                    0};
                this->black_pieces.push_back(knight);
            } else if (ch == 'b') {
                Piece bishop = {Piece::Type::Bishop,
                                Piece::Color::Black,
                                {y, x},
                                {{{1, 1}, {2, 2}, {3, 3}, {4, 4}, {5, 5}, {6, 6}, {7, 7}},
                                 {{1, -1}, {2, -2}, {3, -3}, {4, -4}, {5, -5}, {6, -6}, {7, -7}},
                                 {{-1, -1}, {-2, -2}, {-3, -3}, {-4, -4}, {-5, -5}, {-6, -6}, {-7, -7}},
                                 {{-1, 1}, {-2, 2}, {-3, 3}, {-4, 4}, {-5, 5}, {-6, 6}, {-7, 7}}},
                                false,
                                0};
                this->black_pieces.push_back(bishop);
            } else if (ch == 'q') {
                Piece queen = {Piece::Type::Queen,
                               Piece::Color::Black,
                               {y, x},
                               {{{1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}},
                                {{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}},
                                {{-1, 0}, {-2, 0}, {-3, 0}, {-4, 0}, {-5, 0}, {-6, 0}, {-7, 0}},
                                {{0, -1}, {0, -2}, {0, -3}, {0, -4}, {0, -5}, {0, -6}, {0, -7}},
                                {{1, 1}, {2, 2}, {3, 3}, {4, 4}, {5, 5}, {6, 6}, {7, 7}},
                                {{1, -1}, {2, -2}, {3, -3}, {4, -4}, {5, -5}, {6, -6}, {7, -7}},
                                {{-1, -1}, {-2, -2}, {-3, -3}, {-4, -4}, {-5, -5}, {-6, -6}, {-7, -7}},
                                {{-1, 1}, {-2, 2}, {-3, 3}, {-4, 4}, {-5, 5}, {-6, 6}, {-7, 7}}},
                               false,
                               0};
                this->black_pieces.push_back(queen);
            } else if (ch == 'k') {
                Piece king = {Piece::Type::King,
                              Piece::Color::Black,
                              {y, x},
                              {{{0, 1}}, {{1, -1}}, {{1, 0}}, {{1, 1}}, {{0, -1}}, {{-1, -1}}, {{-1, 0}}, {{-1, 1}}},
                              false,
                              0};
                this->black_pieces.push_back(king);
            } else if (ch == 'p') {
                Piece pawn = {Piece::Type::Pawn, Piece::Color::Black, {y, x}, {{{-1, -1}}, {{-1, 1}}}, false, 0};
                this->black_pieces.push_back(pawn);
            } else if (ch == 'R') {
                Piece rook = {Piece::Type::Rook,
                              Piece::Color::White,
                              {y, x},
                              {{{1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}},
                               {{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}},
                               {{-1, 0}, {-2, 0}, {-3, 0}, {-4, 0}, {-5, 0}, {-6, 0}, {-7, 0}},
                               {{0, -1}, {0, -2}, {0, -3}, {0, -4}, {0, -5}, {0, -6}, {0, -7}}},
                              false,
                              0};
                this->white_pieces.push_back(rook);
            } else if (ch == 'N') {
                Piece knight = {
                    Piece::Type::Knight,
                    Piece::Color::White,
                    {y, x},
                    {{{1, -2}}, {{1, 2}}, {{2, -1}}, {{2, 1}}, {{-1, 2}}, {{-1, -2}}, {{-2, 1}}, {{-2, -1}}},
                    false,
                    0};
                this->white_pieces.push_back(knight);
            } else if (ch == 'B') {
                Piece rook = {Piece::Type::Bishop,
                              Piece::Color::White,
                              {y, x},
                              {{{1, 1}, {2, 2}, {3, 3}, {4, 4}, {5, 5}, {6, 6}, {7, 7}},
                               {{1, -1}, {2, -2}, {3, -3}, {4, -4}, {5, -5}, {6, -6}, {7, -7}},
                               {{-1, -1}, {-2, -2}, {-3, -3}, {-4, -4}, {-5, -5}, {-6, -6}, {-7, -7}},
                               {{-1, 1}, {-2, 2}, {-3, 3}, {-4, 4}, {-5, 5}, {-6, 6}, {-7, 7}}},
                              false,
                              0};
                this->white_pieces.push_back(rook);
            } else if (ch == 'Q') {
                Piece queen = {Piece::Type::Queen,
                               Piece::Color::White,
                               {y, x},
                               {{{1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}},
                                {{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}},
                                {{-1, 0}, {-2, 0}, {-3, 0}, {-4, 0}, {-5, 0}, {-6, 0}, {-7, 0}},
                                {{0, -1}, {0, -2}, {0, -3}, {0, -4}, {0, -5}, {0, -6}, {0, -7}},
                                {{1, 1}, {2, 2}, {3, 3}, {4, 4}, {5, 5}, {6, 6}, {7, 7}},
                                {{1, -1}, {2, -2}, {3, -3}, {4, -4}, {5, -5}, {6, -6}, {7, -7}},
                                {{-1, -1}, {-2, -2}, {-3, -3}, {-4, -4}, {-5, -5}, {-6, -6}, {-7, -7}},
                                {{-1, 1}, {-2, 2}, {-3, 3}, {-4, 4}, {-5, 5}, {-6, 6}, {-7, 7}}},
                               false,
                               0};
                this->white_pieces.push_back(queen);
            } else if (ch == 'K') {
                Piece king = {Piece::Type::King,
                              Piece::Color::White,
                              {y, x},
                              {{{0, 1}}, {{1, -1}}, {{1, 0}}, {{1, 1}}, {{0, -1}}, {{-1, -1}}, {{-1, 0}}, {{-1, 1}}},
                              false,
                              0};
                this->white_pieces.push_back(king);
            } else if (ch == 'P') {
                Piece pawn = {Piece::Type::Pawn, Piece::Color::White, {y, x}, {{{1, -1}}, {{1, 1}}}, false, 0};
                this->white_pieces.push_back(pawn);
            }
            x++;
        }
        iss >> token;
        if (token == "w") {
            this->player = Piece::Color::White;
        } else {
            this->player = Piece::Color::Black;
        }
        iss >> token;
        for (auto ch : token) {
            if (ch == 'K') {
                this->white_kingside_flag = true;
            } else if (ch == 'Q') {
                this->white_queenside_flag = true;
            } else if (ch == 'k') {
                this->black_kingside_flag = true;
            } else if (ch == 'q') {
                this->black_queenside_flag = true;
            }
        }
        iss >> token;
        if (token != "-") {
            std::string start, end;
            start.push_back(token[0]);
            end.push_back(token[0]);
            if (ColorTransition(this->player) == Piece::Color::White) {
                start.push_back(static_cast<char>(static_cast<int>(token[1]) - 1));
                end.push_back(static_cast<char>(static_cast<int>(token[1]) + 1));
            } else {
                start.push_back(static_cast<char>(static_cast<int>(token[1]) + 1));
                end.push_back(static_cast<char>(static_cast<int>(token[1]) - 1));
            }
            this->moves.push_back(start + end);
        }
        this->positions.push_back({this->white_pieces, this->black_pieces});
    }

    std::pair<std::pair<int, int>, std::pair<int, int>> ParseMove(std::string move) {
        std::pair<int, int> start, end;
        start = {static_cast<int>(move[1]) - static_cast<int>('0'),
                 static_cast<int>(move[0]) - static_cast<int>('a') + 1};
        end = {static_cast<int>(move[3]) - static_cast<int>('0'),
               static_cast<int>(move[2]) - static_cast<int>('a') + 1};
        return {start, end};
    }

    std::string GetMove(std::pair<int, int> start, std::pair<int, int> end) {
        std::string move;
        move += static_cast<char>(start.second - 1 + static_cast<int>('a'));
        move += static_cast<char>(start.first + static_cast<int>('0'));
        move += static_cast<char>(end.second - 1 + static_cast<int>('a'));
        move += static_cast<char>(end.first + static_cast<int>('0'));
        return move;
    }

    Piece::Color ColorTransition(Piece::Color color) {
        return static_cast<Piece::Color>((static_cast<int>(color) + 1) % 2);
    }

    std::vector<Piece>& Pieces(Piece::Color player) {
        if (player == Piece::Color::White) {
            return this->white_pieces;
        } else {
            return this->black_pieces;
        }
    }

    void Move(std::string move) {
        Piece::Color player = this->player, opponent = ColorTransition(this->player);
        auto parsed_move = ParseMove(move);
        auto start = parsed_move.first, end = parsed_move.second;
        Piece& piece = Pieces(player)[FindPiece(start, player)];
        if (piece.type == Piece::Type::Pawn) {
            if (piece.color == Piece::Color::White) {
                auto en_passant = EnPassant(player);
                if (end.first == 8) {
                    piece.type = Piece::Type::Queen;
                    piece.operations = {{{1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}},
                                        {{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}},
                                        {{-1, 0}, {-2, 0}, {-3, 0}, {-4, 0}, {-5, 0}, {-6, 0}, {-7, 0}},
                                        {{0, -1}, {0, -2}, {0, -3}, {0, -4}, {0, -5}, {0, -6}, {0, -7}},
                                        {{1, 1}, {2, 2}, {3, 3}, {4, 4}, {5, 5}, {6, 6}, {7, 7}},
                                        {{1, -1}, {2, -2}, {3, -3}, {4, -4}, {5, -5}, {6, -6}, {7, -7}},
                                        {{-1, -1}, {-2, -2}, {-3, -3}, {-4, -4}, {-5, -5}, {-6, -6}, {-7, -7}},
                                        {{-1, 1}, {-2, 2}, {-3, 3}, {-4, 4}, {-5, 5}, {-6, 6}, {-7, 7}}};
                } else if (std::find(en_passant.begin(), en_passant.end(), end) != en_passant.end()) {
                    Pieces(opponent)[FindPiece({end.first - 1, end.second}, opponent)].is_captured = true;
                }
            } else {
                auto en_passant = EnPassant(player);
                if (end.first == 1) {
                    piece.type = Piece::Type::Queen;
                    piece.operations = {{{1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}},
                                        {{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}},
                                        {{-1, 0}, {-2, 0}, {-3, 0}, {-4, 0}, {-5, 0}, {-6, 0}, {-7, 0}},
                                        {{0, -1}, {0, -2}, {0, -3}, {0, -4}, {0, -5}, {0, -6}, {0, -7}},
                                        {{1, 1}, {2, 2}, {3, 3}, {4, 4}, {5, 5}, {6, 6}, {7, 7}},
                                        {{1, -1}, {2, -2}, {3, -3}, {4, -4}, {5, -5}, {6, -6}, {7, -7}},
                                        {{-1, -1}, {-2, -2}, {-3, -3}, {-4, -4}, {-5, -5}, {-6, -6}, {-7, -7}},
                                        {{-1, 1}, {-2, 2}, {-3, 3}, {-4, 4}, {-5, 5}, {-6, 6}, {-7, 7}}};
                } else if (std::find(en_passant.begin(), en_passant.end(), end) != en_passant.end()) {
                    Pieces(opponent)[FindPiece({end.first + 1, end.second}, opponent)].is_captured = true;
                }
            }
        } else if (piece.type == Piece::Type::King) {
            if (end.second - start.second == 2) {
                Piece& rook = Pieces(player)[FindPiece({start.first, start.second + 3}, player)];
                rook.square.second -= 2;
                rook.move_cnt++;
            } else if (end.second - start.second == -2) {
                Piece& rook = Pieces(player)[FindPiece({start.first, start.second - 4}, player)];
                rook.square.second += 3;
                rook.move_cnt++;
            }
        }
        piece.square = end;
        piece.move_cnt++;
        int index = FindPiece(end, opponent);
        if (index != -1) {
            Pieces(opponent)[index].is_captured = true;
        }
    }

    bool Check(Piece::Color player) {
        Piece::Color opponent = ColorTransition(player);
        for (auto piece : Pieces(player)) {
            if (piece.is_captured) {
                continue;
            }
            if (piece.type == Piece::Type::King) {
                return IsControlled(piece.square, opponent);
            }
        }
        return false;
    }

    bool Checkmate(Piece::Color player) {
        Piece::Color opponent = ColorTransition(player);
        for (auto piece : Pieces(player)) {
            if (piece.is_captured) {
                continue;
            }
            if (piece.type == Piece::Type::King) {
                if (IsControlled(piece.square, opponent) == false) {
                    return false;
                }
                if (AvailableSquares(piece).size() == 0) {
                    return true;
                }
                return false;
            }
        }
        return false;
    }

    bool IsControlled(std::pair<int, int> square, Piece::Color player) {
        for (auto piece : Pieces(player)) {
            if (piece.is_captured) {
                continue;
            }
            auto controlled_squares = ControlledSquares(piece);
            if (std::find(controlled_squares.begin(), controlled_squares.end(), square) != controlled_squares.end()) {
                return true;
            }
        }
        return false;
    }

    bool IsOccupied(std::pair<int, int> square, Piece::Color player) {
        for (auto piece : Pieces(player)) {
            if (piece.is_captured) {
                continue;
            }
            if (piece.square == square) {
                return true;
            }
        }
        return false;
    }

    std::vector<std::pair<int, int>> ControlledSquares(Piece& piece) {
        Piece::Color player = piece.color, opponent = ColorTransition(piece.color);
        std::vector<std::pair<int, int>> squares;
        for (auto ops : piece.operations) {
            for (auto op : ops) {
                std::pair<int, int> square = {piece.square.first + op.first, piece.square.second + op.second};
                if (1 <= square.first && square.first <= 8 && 1 <= square.second && square.second <= 8) {
                    squares.push_back(square);
                    if (IsOccupied(square, player) || IsOccupied(square, opponent)) {
                        break;
                    }
                } else {
                    break;
                }
            }
        }
        return squares;
    }

    int FindPiece(std::pair<int, int> square, Piece::Color player) {
        for (int i = 0; i < int(Pieces(player).size()); i++) {
            if (Pieces(player)[i].is_captured) {
                continue;
            }
            if (Pieces(player)[i].square == square) {
                return i;
            }
        }
        return -1;
    }

    bool Castling(Piece& king, std::string side) {
        Piece::Color player = king.color, opponent = ColorTransition(king.color);
        if (king.color == Piece::Color::White) {
            if (king.square != std::pair{1, 5} || IsControlled({1, 5}, opponent) || king.move_cnt > 0) {
                return false;
            }
            if (side == "kingside") {
                if (this->white_kingside_flag == false) {
                    return false;
                }
                if (IsOccupied({1, 6}, player) || IsOccupied({1, 6}, opponent) || IsOccupied({1, 7}, player) ||
                    IsOccupied({1, 7}, opponent)) {
                    return false;
                } else if (IsControlled({1, 6}, opponent) || IsControlled({1, 7}, opponent)) {
                    return false;
                }
                int index = FindPiece({1, 8}, player);
                if (index == -1) {
                    return false;
                }
                auto piece = Pieces(player)[index];
                if (piece.type == Piece::Type::Rook && piece.move_cnt == 0) {
                    return true;
                }
            } else if (side == "queenside") {
                if (this->white_queenside_flag == false) {
                    return false;
                }
                if (IsOccupied({1, 4}, player) || IsOccupied({1, 4}, opponent) || IsOccupied({1, 3}, player) ||
                    IsOccupied({1, 3}, opponent) || IsOccupied({1, 2}, player) || IsOccupied({1, 2}, opponent)) {
                    return false;
                } else if (IsControlled({1, 4}, opponent) || IsControlled({1, 3}, opponent)) {
                    return false;
                }
                int index = FindPiece({1, 1}, player);
                if (index == -1) {
                    return false;
                }
                auto piece = Pieces(player)[index];
                if (piece.type == Piece::Type::Rook && piece.move_cnt == 0) {
                    return true;
                }
            }
        } else if (king.color == Piece::Color::Black) {
            if (king.square != std::pair{8, 5} || IsControlled({8, 5}, opponent) || king.move_cnt > 0) {
                return false;
            }
            if (side == "kingside") {
                if (this->black_kingside_flag == false) {
                    return false;
                }
                if (IsOccupied({8, 6}, player) || IsOccupied({8, 6}, opponent) || IsOccupied({8, 7}, player) ||
                    IsOccupied({8, 7}, opponent)) {
                    return false;
                } else if (IsControlled({8, 6}, opponent) || IsControlled({8, 7}, opponent)) {
                    return false;
                }
                int index = FindPiece({8, 8}, player);
                if (index == -1) {
                    return false;
                }
                auto piece = Pieces(player)[index];
                if (piece.type == Piece::Type::Rook && piece.move_cnt == 0) {
                    return true;
                }
            } else if (side == "queenside") {
                if (this->black_queenside_flag == false) {
                    return false;
                }
                if (IsOccupied({8, 4}, player) || IsOccupied({8, 4}, opponent) || IsOccupied({8, 3}, player) ||
                    IsOccupied({8, 3}, opponent) || IsOccupied({8, 2}, player) || IsOccupied({8, 2}, opponent)) {
                    return false;
                } else if (IsControlled({8, 4}, opponent) || IsControlled({8, 3}, opponent)) {
                    return false;
                }
                int index = FindPiece({8, 1}, player);
                if (index == -1) {
                    return false;
                }
                auto piece = Pieces(player)[index];
                if (piece.type == Piece::Type::Rook && piece.move_cnt == 0) {
                    return true;
                }
            }
        }
        return false;
    }

    std::vector<std::pair<int, int>> EnPassant(Piece::Color player) {
        Piece::Color opponent = ColorTransition(player);
        std::vector<std::pair<int, int>> squares;
        for (auto piece : Pieces(player)) {
            if (piece.is_captured) {
                continue;
            }
            if (piece.type == Piece::Type::Pawn) {
                for (auto ops : piece.operations) {
                    for (auto op : ops) {
                        std::pair<int, int> square = {piece.square.first + op.first, piece.square.second + op.second};
                        if (moves.size() > 0) {
                            auto parsed_move = ParseMove(moves.back());
                            auto opponent_start = parsed_move.first, opponent_end = parsed_move.second;
                            bool pawn_flag = false;
                            int index = FindPiece(opponent_end, opponent);
                            if (index != -1) {
                                auto opponent_piece = Pieces(opponent)[index];
                                if (opponent_piece.type == Piece::Type::Pawn) {
                                    pawn_flag = true;
                                }
                            }
                            if (piece.color == Piece::Color::White) {
                                if (pawn_flag && opponent_start.first == 7 && opponent_end.first == 5 &&
                                    piece.square.first == 5 && opponent_end.second == square.second) {
                                    squares.push_back(square);
                                }
                            } else {
                                if (pawn_flag && opponent_start.first == 2 && opponent_end.first == 4 &&
                                    piece.square.first == 4 && opponent_end.second == square.second) {
                                    squares.push_back(square);
                                }
                            }
                        }
                    }
                }
            }
        }
        return squares;
    }

    std::vector<std::pair<int, int>> AvailableSquares(Piece& piece) {
        Piece::Color player = piece.color, opponent = ColorTransition(piece.color);
        std::vector<std::pair<int, int>> squares;
        if (piece.type == Piece::Type::King) {
            if (Castling(piece, "kingside")) {
                squares.push_back({piece.square.first, 7});
            }
            if (Castling(piece, "queenside")) {
                squares.push_back({piece.square.first, 3});
            }
            for (auto square : ControlledSquares(piece)) {
                if (IsControlled(square, opponent) == false && IsOccupied(square, player) == false) {
                    squares.push_back(square);
                }
            }
        } else if (piece.type == Piece::Type::Pawn) {
            for (auto ops : piece.operations) {
                for (auto op : ops) {
                    std::pair<int, int> square = {piece.square.first + op.first, piece.square.second + op.second};
                    auto en_passant = EnPassant(player);
                    if (IsOccupied(square, opponent) ||
                        std::find(en_passant.begin(), en_passant.end(), square) != en_passant.end()) {
                        squares.push_back(square);
                    }
                }
            }
            if (piece.color == Piece::Color::White) {
                if (1 <= piece.square.first + 1 && piece.square.first + 1 <= 8 &&
                    IsOccupied({piece.square.first + 1, piece.square.second}, player) == false &&
                    IsOccupied({piece.square.first + 1, piece.square.second}, opponent) == false) {
                    squares.push_back({piece.square.first + 1, piece.square.second});
                    if (piece.square.first == 2 &&
                        IsOccupied({piece.square.first + 2, piece.square.second}, player) == false &&
                        IsOccupied({piece.square.first + 2, piece.square.second}, opponent) == false) {
                        squares.push_back({piece.square.first + 2, piece.square.second});
                    }
                }
            } else {
                if (1 <= piece.square.first - 1 && piece.square.first - 1 <= 8 &&
                    IsOccupied({piece.square.first - 1, piece.square.second}, player) == false &&
                    IsOccupied({piece.square.first - 1, piece.square.second}, opponent) == false) {
                    squares.push_back({piece.square.first - 1, piece.square.second});
                    if (piece.square.first == 7 &&
                        IsOccupied({piece.square.first - 2, piece.square.second}, player) == false &&
                        IsOccupied({piece.square.first - 2, piece.square.second}, opponent) == false) {
                        squares.push_back({piece.square.first - 2, piece.square.second});
                    }
                }
            }
        } else {
            for (auto square : ControlledSquares(piece)) {
                if (FindPiece(square, player) != -1) {
                    continue;
                }
                squares.push_back(square);
            }
        }
        return squares;
    }

    int PositionEvaluation() {
        if (Checkmate(Piece::Color::White)) {
            return -100;
        } else if (Checkmate(Piece::Color::Black)) {
            return 100;
        }
        int eval = 0;
        for (int i = 0; i < int(this->white_pieces.size()); i++) {
            if (white_pieces[i].is_captured) {
                continue;
            }
            if (white_pieces[i].type == Piece::Type::Rook) {
                eval += 5;
            } else if (white_pieces[i].type == Piece::Type::Knight) {
                eval += 3;
            } else if (white_pieces[i].type == Piece::Type::Bishop) {
                eval += 3;
            } else if (white_pieces[i].type == Piece::Type::Queen) {
                eval += 9;
            } else if (white_pieces[i].type == Piece::Type::Pawn) {
                eval += 1;
            }
        }
        for (int i = 0; i < int(this->black_pieces.size()); i++) {
            if (black_pieces[i].is_captured) {
                continue;
            }
            if (black_pieces[i].type == Piece::Type::Rook) {
                eval -= 5;
            } else if (black_pieces[i].type == Piece::Type::Knight) {
                eval -= 3;
            } else if (black_pieces[i].type == Piece::Type::Bishop) {
                eval -= 3;
            } else if (black_pieces[i].type == Piece::Type::Queen) {
                eval -= 9;
            } else if (black_pieces[i].type == Piece::Type::Pawn) {
                eval -= 1;
            }
        }
        return eval;
    }

    std::pair<long long, std::pair<int, std::string>> Go(std::mt19937& gen, int depth) {
        if (depth == 0) {
            return {1ll, {PositionEvaluation(), ""}};
        }
        std::vector<std::pair<int, std::string>> moves;
        long long node_count = 0;
        for (auto piece : Pieces(this->player)) {
            if (piece.is_captured) {
                continue;
            }
            for (auto square : AvailableSquares(piece)) {
                std::string move = GetMove(piece.square, square);
                Move(move);
                this->moves.push_back(move);
                this->positions.push_back({this->white_pieces, this->black_pieces});
                if (Check(this->player) == false) {
                    this->player = ColorTransition(this->player);
                    auto res = Go(gen, depth - 1);
                    node_count += res.first;
                    int eval = res.second.first;
                    this->player = ColorTransition(this->player);
                    if (moves.size() > 0) {
                        if ((this->player == Piece::Color::White && eval > moves[0].first) ||
                            (this->player == Piece::Color::Black && eval < moves[0].first)) {
                            moves.clear();
                            moves.push_back({eval, move});
                        } else if (eval == moves[0].first) {
                            moves.push_back({eval, move});
                        }
                    } else {
                        moves.push_back({eval, move});
                    }
                }
                this->moves.pop_back();
                this->positions.pop_back();
                this->white_pieces = this->positions.back().first;
                this->black_pieces = this->positions.back().second;
            }
        }
        std::uniform_int_distribution<int> dist(0, static_cast<int>(moves.size()) - 1);
        return {node_count, moves[dist(gen)]};
    }
};

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::string line, token;
    Position position;
    std::string startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    position.StartPosition(startpos);
    while (std::getline(std::cin, line)) {
        std::istringstream iss(line);
        iss >> token;
        if (token == "uci") {
            std::cout << "id name ChessEngine" << std::endl;
            std::cout << "id author agresh775" << std::endl;
            std::cout << "uciok" << std::endl;
        } else if (token == "isready") {
            std::cout << "readyok" << std::endl;
        } else if (token == "ucinewgame") {
            position.StartPosition(startpos);
        } else if (token == "position") {
            iss >> token;
            if (token == "fen") {
                iss >> token;
                std::string fen = token;
                for (int i = 0; i < 5; i++) {
                    iss >> token;
                    fen += " " + token;
                }
                position.StartPosition(fen);
            } else {
                position.StartPosition(startpos);
            }
            iss >> token;
            while (iss >> token) {
                position.Move(token);
                position.player = position.ColorTransition(position.player);
                position.moves.push_back(token);
                position.positions.push_back({position.white_pieces, position.black_pieces});
            }
        } else if (token == "go") {
            int depth;
            iss >> token >> depth;
            if (token == "perft") {
                std::cout << "nodes " << position.Go(gen, depth).first << std::endl;
            } else {
                std::cout << "bestmove " << position.Go(gen, depth).second.second << std::endl;
            }
        } else if (token == "quit") {
            break;
        }
    }
    return 0;
}
