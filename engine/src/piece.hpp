#pragma once

#include <utility>
#include <vector>

struct Piece {
    enum class Type { Pawn, Rook, Knight, Bishop, Queen, King };
    enum class Color { White, Black };

    Type type;
    Color color;
    std::pair<int, int> square;
    std::vector<std::vector<std::pair<int, int>>> operations;
    bool is_captured;
    int move_cnt;

    Piece(Type t, Color c, std::pair<int, int> sq, std::vector<std::vector<std::pair<int, int>>> ops);
    void captured();
};

const std::vector<std::vector<std::pair<int, int>>>& rook_operations();
const std::vector<std::vector<std::pair<int, int>>>& knight_operations();
const std::vector<std::vector<std::pair<int, int>>>& bishop_operations();
const std::vector<std::vector<std::pair<int, int>>>& queen_operations();
const std::vector<std::vector<std::pair<int, int>>>& king_operations();
const std::vector<std::vector<std::pair<int, int>>>& black_pawn_operations();
const std::vector<std::vector<std::pair<int, int>>>& white_pawn_operations();
