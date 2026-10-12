#include <string>
#include <utility>

#include "piece.hpp"

int x_to_int(char x) { return static_cast<int>(x) - static_cast<int>('a') + 1; }

int y_to_int(char y) { return static_cast<int>(y) - static_cast<int>('0'); }

char x_to_char(int x) { return static_cast<char>(x - 1 + static_cast<int>('a')); }

char y_to_char(int y) { return static_cast<char>(y + static_cast<int>('0')); }

std::pair<std::pair<int, int>, std::pair<int, int>> ParseMove(std::string move) {
    std::pair<int, int> start, end;
    start = {y_to_int(move[1]), x_to_int(move[0])};
    end = {y_to_int(move[3]), x_to_int(move[2])};
    return {start, end};
}

std::string GetMove(std::pair<int, int> start, std::pair<int, int> end) {
    std::string move;
    move += x_to_char(start.second);
    move += y_to_char(start.first);
    move += x_to_char(end.second);
    move += y_to_char(end.first);
    return move;
}

Piece::Color ColorTransition(Piece::Color color) {
    return static_cast<Piece::Color>((static_cast<int>(color) + 1) % 2);
}