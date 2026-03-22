def convert(x_step, y_step, mode):
    if mode == "white":
        alpha = chr(x_step + ord('a'))
        digit = 8 - y_step
    if mode == "black":
        alpha = chr(7 - x_step + ord('a'))
        digit = y_step + 1
    return alpha + str(digit)
