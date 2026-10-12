#pragma once

#include <string>
#include <utility>

#include "piece.hpp"

int x_to_int(char x);

int y_to_int(char y);

char x_to_char(int x);

char y_to_char(int y);

std::pair<std::pair<int, int>, std::pair<int, int>> ParseMove(std::string move);

std::string GetMove(std::pair<int, int> start, std::pair<int, int> end);

Piece::Color ColorTransition(Piece::Color color);
