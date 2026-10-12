#pragma once

#include <random>
#include <string>
#include <utility>
#include <vector>

#include "piece.hpp"

class Position {
   private:
    Piece::Color player;
    std::vector<Piece> white_pieces, black_pieces;
    std::vector<std::string> moves;
    std::vector<std::pair<std::vector<Piece>, std::vector<Piece>>> positions;
    bool white_kingside_flag, white_queenside_flag, black_kingside_flag, black_queenside_flag;

    void Move(std::pair<int, int> start, std::pair<int, int> end);
    std::vector<Piece>& Pieces(Piece::Color player);
    bool Check(Piece::Color player);
    bool Checkmate(Piece::Color player);
    bool IsControlled(std::pair<int, int> square, Piece::Color player);
    bool IsOccupied(std::pair<int, int> square, Piece::Color player);
    std::vector<std::pair<int, int>> ControlledSquares(Piece& piece);
    int FindPiece(std::pair<int, int> square, Piece::Color player);
    bool Castling(Piece& king, std::string side);
    std::vector<std::pair<int, int>> EnPassant(Piece::Color player);
    std::vector<std::pair<int, int>> AvailableSquares(Piece& piece);
    int PositionEvaluation();

   public:
    void StartPosition(std::string fen);
    void Move(std::string move);
    std::pair<long long, std::pair<int, std::string>> Go(std::mt19937& gen, int depth);
};