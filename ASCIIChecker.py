
def checkAscii(x):
    if x == 39:  # '
        x = 97 + 29
    elif x == 32:  # space
        x = 97 + 28
    elif x == 95:  # _
        x = 97 + 27
    elif x == 45:  # -
        x = 97 + 26
    elif x == 46:  # .
        x = 97 + 31
    elif x in range(65, 91):  # upper-case
        x = 97 + 30
    return x