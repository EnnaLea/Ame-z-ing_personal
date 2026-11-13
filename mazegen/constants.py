from __future__ import annotations


# Direction Bit decimal version
# bit value would be:
# N = 0001
# E = 0010
# S = 0100
# W = 1000
# using the power of 2 as to not overlap bits
N, E, S, W = 1, 2, 4, 8
# all walls closed, total of 15 bit(1+2+4+8)
# because OR operator combine the for bit into one
ALL_WALLS = N | E | S | W
# right and left movements
# row movement
DIRX: dict[int, int] = {E: 1, W: -1, N: 0, S: 0}
# column movement
DIRY: dict[int, int] = {E: 0, W: 0, N: -1, S: 1}
# opposite direction
OPPOSITE: dict[int, int] = {E: W, W: E, N: S, S: N}
# bitmap patter "42"
PATTERN42: list[list[int]] = [
    [1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
]
