def convert(x, y):
    alpha = chr(x - 1 + ord("a"))
    digit = y
    return alpha + str(digit)


def parse_move(move):
    start = [int(move[1]), ord(move[0]) - ord("a") + 1]
    end = [int(move[3]), ord(move[2]) - ord("a") + 1]
    return [start, end]
