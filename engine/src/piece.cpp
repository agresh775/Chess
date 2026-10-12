#include "piece.hpp"

#include <utility>
#include <vector>

Piece::Piece(Type t, Color c, std::pair<int, int> sq, std::vector<std::vector<std::pair<int, int>>> ops) {
    type = t;
    color = c;
    square = sq;
    operations = ops;
    is_captured = false;
    move_cnt = 0;
}

void Piece::captured() { is_captured = true; }

const std::vector<std::vector<std::pair<int, int>>>& rook_operations() {
    static const std::vector<std::vector<std::pair<int, int>>> data = {
        {{1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}},
        {{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}},
        {{-1, 0}, {-2, 0}, {-3, 0}, {-4, 0}, {-5, 0}, {-6, 0}, {-7, 0}},
        {{0, -1}, {0, -2}, {0, -3}, {0, -4}, {0, -5}, {0, -6}, {0, -7}}};
    return data;
}

const std::vector<std::vector<std::pair<int, int>>>& knight_operations() {
    static const std::vector<std::vector<std::pair<int, int>>> data = {{{1, -2}}, {{1, 2}},   {{2, -1}}, {{2, 1}},
                                                                       {{-1, 2}}, {{-1, -2}}, {{-2, 1}}, {{-2, -1}}};
    return data;
}

const std::vector<std::vector<std::pair<int, int>>>& bishop_operations() {
    static const std::vector<std::vector<std::pair<int, int>>> data = {
        {{1, 1}, {2, 2}, {3, 3}, {4, 4}, {5, 5}, {6, 6}, {7, 7}},
        {{1, -1}, {2, -2}, {3, -3}, {4, -4}, {5, -5}, {6, -6}, {7, -7}},
        {{-1, -1}, {-2, -2}, {-3, -3}, {-4, -4}, {-5, -5}, {-6, -6}, {-7, -7}},
        {{-1, 1}, {-2, 2}, {-3, 3}, {-4, 4}, {-5, 5}, {-6, 6}, {-7, 7}}};
    return data;
}

const std::vector<std::vector<std::pair<int, int>>>& queen_operations() {
    static const std::vector<std::vector<std::pair<int, int>>> data = {
        {{1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}},
        {{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}},
        {{-1, 0}, {-2, 0}, {-3, 0}, {-4, 0}, {-5, 0}, {-6, 0}, {-7, 0}},
        {{0, -1}, {0, -2}, {0, -3}, {0, -4}, {0, -5}, {0, -6}, {0, -7}},
        {{1, 1}, {2, 2}, {3, 3}, {4, 4}, {5, 5}, {6, 6}, {7, 7}},
        {{1, -1}, {2, -2}, {3, -3}, {4, -4}, {5, -5}, {6, -6}, {7, -7}},
        {{-1, -1}, {-2, -2}, {-3, -3}, {-4, -4}, {-5, -5}, {-6, -6}, {-7, -7}},
        {{-1, 1}, {-2, 2}, {-3, 3}, {-4, 4}, {-5, 5}, {-6, 6}, {-7, 7}}};
    return data;
}

const std::vector<std::vector<std::pair<int, int>>>& king_operations() {
    static const std::vector<std::vector<std::pair<int, int>>> data = {{{0, 1}},  {{1, -1}},  {{1, 0}},  {{1, 1}},
                                                                       {{0, -1}}, {{-1, -1}}, {{-1, 0}}, {{-1, 1}}};
    return data;
}

const std::vector<std::vector<std::pair<int, int>>>& black_pawn_operations() {
    static const std::vector<std::vector<std::pair<int, int>>> data = {{{-1, -1}}, {{-1, 1}}};
    return data;
}

const std::vector<std::vector<std::pair<int, int>>>& white_pawn_operations() {
    static const std::vector<std::vector<std::pair<int, int>>> data = {{{1, -1}}, {{1, 1}}};
    return data;
}