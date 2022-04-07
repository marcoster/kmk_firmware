import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.DA1,
        board.A0,
        board.D15,
        board.D14,
        board.D16,
        board.D10,
    )
    row_pins = (
        board.D5,
        board.D6,
        board.D7,
        board.D8,
        board.D9)
    diode_orientation = DiodeOrientation.COLUMNS
    uart_pin = board.D1
    rgb_pixel_pin = board.P0_06
    data_pin = board.P0_08
    i2c = board.I2C
    powersave_pin = board.P0_13

    # flake8: noqa
    coord_mapping = [
     0,  1,  2,  3,  4,  5,  36, 35, 34, 33, 32, 31,
     6,  7,  8,  9, 10, 11,  42, 41, 40, 39, 38, 37,
    12, 13, 14, 15, 16, 17,  48, 47, 46, 45, 44, 43,
    18, 19, 20, 21, 22, 23,  54, 53, 52, 51, 50, 49,
        26, 27, 28, 29, 30,  60, 59, 58, 57, 56,
    ]
