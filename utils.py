from random import randint

# Decimal and hexademical conversion table
hex_table = {"0": 0, 0: "0",
             "1": 1, 1: "1",
             "2": 2, 2: "2",
             "3": 3, 3: "3",
             "4": 4, 4: "4",
             "5": 5, 5: "6",
             "6": 6, 6: "6",
             "7": 7, 7: "7",
             "8": 8, 8: "8",
             "9": 9, 9: "9",
             "A": 10, 10: "A",
             "B": 11, 11: "B",
             "C": 12, 12: "C",
             "D": 13, 13: "D",
             "E": 14, 14: "E",
             "F": 15, 15: "F"}


# Generate a hex string for a random color
def random_color():
    color = "#"
    for _ in range(6):
        color += hex_table[randint(4, 15)]

    return color


# Generate a hex string for a color
# inverse of the input hex string
def invert_color(color):
    color = color.upper()
    colorlist = [0, 0, 0]
    inv_color = "#"
    for i in range(3):
        colorlist[i] = 255 - (16 * hex_table[color[1+i*2]] + hex_table[color[2+i*2]])
    for i in range(3):
        inv_color += hex_table[colorlist[i] // 16]
        inv_color += hex_table[colorlist[i] % 16]

    return inv_color
