#include <iostream>
#include <random>
#include <sstream>
#include <string>

#include "position.hpp"

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
