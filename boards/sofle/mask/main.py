import board
import busio

from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitType
from kmk.extensions.media_keys import MediaKeys

from kmk.quickpin.pro_micro.kb2040 import pinout as pins

keyboard = KMKKeyboard()

layers = Layers()

split = Split(
    split_flip=True,  # If both halves are the same, but flipped, set this True
    split_type=SplitType.UART,  # Defaults to UART
    uart_interval=20,  # Sets the uarts delay. Lower numbers draw more power
    data_pin=board.RX,  # The primary data pin to talk to the secondary device with
    data_pin2=board.TX,  # Second uart pin to allow 2 way communication
    use_pio=True,  # allows for UART to be used with PIO
)

keyboard.extensions.append(MediaKeys())
keyboard.modules = [layers, split]

# Cleaner key names
XXXXXXX = KC.NO
UNDO = KC.LCTL(KC.Z)
CUT = KC.LCTL(KC.X)
COPY = KC.LCTL(KC.C)
PASTE = KC.LCTL(KC.V)
LSTRT = KC.LCTL(KC.HOME)
LEND = KC.LCTL(KC.END)
BACK = KC.LALT(KC.LEFT)
NEXT = KC.LALT(KC.RGHT)
LBSPC = KC.LCTL(KC.BSPC)

SGRV = KC.LSFT(KC.GRV)
GHOME = KC.LGUI(KC.HOME)
GEND = KC.LGUI(KC.END)

CMAK = KC.DF(0)
QWERT = KC.DF(1)
GAME = KC.DF(2)
TESTL = KC.DF(3)
LOWER = KC.MO(4)
RAISE = KC.MO(5)
ADJUST = KC.MO(6)

LOWERT = KC.HT(KC.TAB, KC.MO(4), prefer_hold=True, tap_interrupted=False, tap_time=200)
RAISET = KC.HT(KC.ESC, KC.MO(5), prefer_hold=True, tap_interrupted=False, tap_time=200)

keyboard.keymap = [
    [  # COLEMAK
        # HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----#ENCODER--#ENCODER--# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----
        KC.ESC,   KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                                            KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,    KC.BSPC,
        KC.TAB,   KC.Q,     KC.W,     KC.F,     KC.P,     KC.B,                                             KC.J,     KC.L,     KC.U,     KC.Y,     KC.SCLN,  KC.DEL,
        KC.LSFT,  KC.A,     KC.R,     KC.S,     KC.T,     KC.G,                                             KC.M,     KC.N,     KC.E,     KC.I,     KC.O,     KC.QUOT,
        KC.LCTL,  KC.Z,     KC.X,     KC.C,     KC.D,     KC.V,                                             KC.K,     KC.H,     KC.COMM,  KC.DOT,   KC.SLSH,  KC.RSFT,
                            KC.LCTL,  KC.LALT,  KC.LGUI,  LOWER,    RAISE,    KC.MUTE,  KC.MPLY,  KC.ENT,   KC.SPC,   KC.RGUI,  KC.RALT,  KC.RCTL,
    ],
    [  # QWERTY
        # HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----#ENCODER--#ENCODER--# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----
        KC.ESC,   KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                                            KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,    KC.BSPC,
        KC.TAB,   KC.Q,     KC.W,     KC.E,     KC.R,     KC.T,                                             KC.Y,     KC.U,     KC.I,     KC.O,     KC.P,     KC.DEL,
        KC.LSFT,  KC.A,     KC.S,     KC.D,     KC.F,     KC.G,                                             KC.H,     KC.J,     KC.K,     KC.L,     KC.SCLN,  KC.QUOT,
        KC.LCTL,  KC.Z,     KC.X,     KC.C,     KC.V,     KC.B,                                             KC.N,     KC.M,     KC.COMM,  KC.DOT,   KC.SLSH,  KC.RSFT,
                            KC.LCTL,  KC.LALT,  KC.LGUI,  LOWER,    RAISE,    KC.MUTE,  KC.MPLY,  KC.ENT,   KC.SPC,   KC.RGUI,  KC.RALT,  KC.RCTL,
    ],
    [  # GAME
        # HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----#ENCODER--#ENCODER--# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----
        KC.ESC,   KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                                            KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,    KC.BSPC,
        KC.TAB,   KC.Q,     KC.W,     KC.E,     KC.R,     KC.T,                                             KC.Y,     KC.U,     KC.I,     KC.O,     KC.P,     KC.DEL,
        KC.LSFT,  KC.A,     KC.S,     KC.D,     KC.F,     KC.G,                                             KC.H,     KC.J,     KC.K,     KC.L,     KC.SCLN,  KC.QUOT,
        KC.LCTL,  KC.Z,     KC.X,     KC.C,     KC.V,     KC.B,                                             KC.N,     KC.M,     KC.COMM,  KC.DOT,   KC.SLSH,  KC.RSFT,
                            KC.CIRC,  KC.M,     KC.LALT,  KC.SPC,   KC.ENT,   KC.MUTE,  KC.MPLY,  RAISE,    LOWER,    KC.RGUI,  KC.RALT,  KC.RCTL,
    ],
    [  # TESTL
        # HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----#ENCODER--#ENCODER--# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----
        KC.ESC,   KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                                            KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,    KC.BSPC,
        KC.TAB,   KC.Q,     KC.W,     KC.F,     KC.P,     KC.B,                                             KC.J,     KC.L,     KC.U,     KC.Y,     KC.SCLN,  KC.DEL,
        KC.LSFT,  KC.A,     KC.R,     KC.S,     KC.T,     KC.G,                                             KC.M,     KC.N,     KC.E,     KC.I,     KC.O,     KC.QUOT,
        KC.LCTL,  KC.Z,     KC.X,     KC.C,     KC.D,     KC.V,                                             KC.K,     KC.H,     KC.COMM,  KC.DOT,   KC.SLSH,  KC.RSFT,
                            KC.LCTL,  KC.LALT,  KC.LGUI,  LOWERT,   RAISET,   KC.MUTE,  KC.MPLY,  KC.ENT,   KC.SPC,   KC.RGUI,  KC.RALT,  KC.RCTL,
    ],
    [  #LOWER
        # HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----#ENCODER--#ENCODER--# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----
        KC.TRNS,  KC.F1,    KC.F2,    KC.F3,    KC.F4,    KC.F5,                                            KC.F6,    KC.F7,    KC.F8,    KC.F9,    KC.F10,   KC.F11,
        KC.TILD,  KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                                            KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,    KC.F12,
        SGRV,     KC.EXLM,  KC.AT,    KC.HASH,  KC.DLR,   KC.PERC,                                          KC.CIRC,  KC.AMPR,  KC.ASTR,  KC.LPRN,  KC.RPRN,  KC.UNDS,
        KC.TRNS,  KC.EQL,   KC.MINS,  KC.PLUS,  KC.LCBR,  KC.RCBR,                                          KC.LBRC,  KC.RBRC,  KC.PIPE,  KC.COLN,  KC.BSLS,  KC.TRNS,
                            KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  ADJUST,   KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,
    ],
    [  #RAISE
        # HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----#ENCODER--#ENCODER--# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----
        KC.TRNS,  KC.F1,    KC.F2,    KC.F3,    KC.F4,    KC.F5,                                            KC.F6,    KC.F7,    KC.F8,    KC.F9,    KC.F10,   KC.F11,
        KC.TRNS,  KC.INS,   KC.UP,    KC.APP,   XXXXXXX,  XXXXXXX,                                          KC.PGUP,  BACK,     KC.UP,    NEXT,     LBSPC,    KC.F12,
        KC.TRNS,  KC.LEFT,  KC.DOWN,  KC.RIGHT, XXXXXXX,  KC.CAPS,                                          KC.PGDN,  KC.LEFT,  KC.DOWN,  KC.RGHT,  KC.DEL,   KC.BSPC,
        KC.TRNS,  UNDO,     CUT,      COPY,     PASTE,    KC.TRNS,                                          XXXXXXX,  LSTRT,    XXXXXXX,  LEND,     XXXXXXX,  KC.TRNS,
                            KC.TRNS,  KC.TRNS,  KC.TRNS,  ADJUST,   KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,
    ],
    [  #ADJUST
        # HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----#ENCODER--#ENCODER--# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----
        KC.TRNS,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,                                          GHOME,    GEND,     XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,
        KC.TRNS,  KC.INS,   KC.UP,    KC.APP,   XXXXXXX,  XXXXXXX,                                          CMAK,     QWERT,    GAME,     TESTL,    LBSPC,    KC.BSPC,
        KC.TRNS,  KC.LEFT,  KC.DOWN,  KC.RIGHT, XXXXXXX,  KC.CAPS,                                          KC.PGDN,  KC.LEFT,  KC.DOWN,  KC.RGHT,  KC.DEL,   KC.BSPC,
        KC.TRNS,  UNDO,     CUT,      COPY,     PASTE,    XXXXXXX,                                          XXXXXXX,  LSTRT,    XXXXXXX,  LEND,     XXXXXXX,  KC.TRNS,
                            KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,
    ]
]

if __name__ == '__main__':
    keyboard.go()
