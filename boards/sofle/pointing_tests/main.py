import board
import busio
import storage
import time

from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitType
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.easypoint import Easypoint
from kmk.modules.mouse_keys import MouseKeys

from kmk.extensions.display import Display, SSD1306, TextEntry, ImageEntry
from kmk.quickpin.pro_micro.kb2040 import pinout as pins

#from kmk.modules.pimoroni_trackball import PointingHandler, Trackball, TrackballMode, PointingHandler, KeyHandler, ScrollHandler, ScrollDirection
#from kmk.modules.glidepoint import GlidePoint
from cirque import GlidePoint

def scan_i2c(i2c):
    while not i2c.try_lock():
        pass
    try:
        while True:
            print("I2C address found:", [hex(device_address) for device_address in i2c.scan()],)
            time.sleep(2)
    finally:
        i2c.unlock()

def test_cirque(i2c):
    while not i2c.try_lock():
        pass
    try:
        print("I2C address found:", [hex(device_address) for device_address in i2c.scan()],)
        buffer = bytearray(8)
        buffer[0] = 0x00 | 0xa0 # firmware id | read
        i2c.writeto_then_readfrom(0x2a, buffer, buffer, out_end=1, in_end=2)
        print("buffer:", buffer)
    finally:
        i2c.unlock()



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

keyboard.modules = [layers, split]

i2c_bus = busio.I2C(pins[5], pins[4])
easypoint = Easypoint(i2c_bus, address=0x40, x_offset=14, y_offset=-11, invert_x=True, invert_y=True)
keyboard.modules.append(easypoint)
keyboard.modules.append(MouseKeys())
#scan_i2c(i2c_bus)
#test_cirque(i2c_bus)

name = str(storage.getmount('/').label)
if name.endswith('L'):
    driver = SSD1306(i2c=i2c_bus, device_address=0x3C,)
    display = Display(
        # Mandatory:
        display=driver,
        # Optional:
        width=128, # screen size
        height=32, # screen size
        flip = False, # flips your display content
        flip_left = False, # flips your display content on left side split
        flip_right = False, # flips your display content on right side split
        brightness=0.8, # initial screen brightness level
        brightness_step=0.1, # used for brightness increase/decrease keycodes
        dim_time=20, # time in seconds to reduce screen brightness
        dim_target=0.1, # set level for brightness decrease
        off_time=60, # time in seconds to turn off screen
        powersave_dim_time=10, # time in seconds to reduce screen brightness
        powersave_dim_target=0.1, # set level for brightness decrease
        powersave_off_time=30, # time in seconds to turn off screen
    )
    display.entries = [
        TextEntry(text="Longer text that", x=0, y=0, layer=0),
        TextEntry(text="has been divided", x=0, y=12, layer=0, side="L"),
        TextEntry(text="for an example", x=0, y=12, layer=0, side="R"),
    ]
    keyboard.extensions.append(display)
elif name.endswith('R'):
    print("nothing here")
    glidepoint = GlidePoint(i2c_bus)
    keyboard.modules.append(glidepoint)
    #glidepoint.during_bootup(None)

keyboard.extensions.append(MediaKeys())


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
MOUSE = KC.MO(7)

LOWERT = KC.HT(KC.TAB, KC.MO(4), prefer_hold=True, tap_interrupted=False, tap_time=200)
RAISET = KC.HT(KC.ESC, KC.MO(5), prefer_hold=True, tap_interrupted=False, tap_time=200)

MOUSET = KC.HT(KC.QUOT, KC.MO(7), prefer_hold=False, tap_interrupted=False, tap_time=100)

keyboard.keymap = [
    [  # COLEMAK
        # HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----#ENCODER--#ENCODER--# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----
        KC.ESC,   KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                                            KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,    KC.BSPC,
        KC.TAB,   KC.Q,     KC.W,     KC.F,     KC.P,     KC.B,                                             KC.J,     KC.L,     KC.U,     KC.Y,     KC.SCLN,  KC.DEL,
        KC.LSFT,  KC.A,     KC.R,     KC.S,     KC.T,     KC.G,                                             KC.M,     KC.N,     KC.E,     KC.I,     KC.O,     MOUSET,
        KC.LCTL,  KC.Z,     KC.X,     KC.C,     KC.D,     KC.V,                                             KC.K,     KC.H,     KC.COMM,  KC.DOT,   KC.SLSH,  KC.RSFT,
                            KC.LCTL,  KC.LALT,  KC.LGUI,  LOWERT,   RAISET,   KC.MUTE,  KC.MPLY,  KC.ENT,   KC.SPC,   KC.RGUI,  KC.RALT,  KC.RCTL,
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
                            KC.LCTL,  KC.LALT,  KC.LGUI,  LOWER,    RAISE,    KC.MUTE,  KC.MPLY,  KC.ENT,   KC.SPC,   KC.RGUI,  KC.RALT,  KC.RCTL,
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
    ],
    [  #MOUSE
        # HERE----# HERE----# HERE----# HERE----# HERE----# HERE----# HERE----#ENCODER--#ENCODER--# HERE----# HERE----# HERE----  # HERE---- # HERE----  # HERE----# HERE----
        KC.TRNS,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,                                          XXXXXXX,  XXXXXXX,    KC.MW_UP,  XXXXXXX,    XXXXXXX,  XXXXXXX,
        KC.TRNS,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,                                          XXXXXXX,  KC.MB_BTN4, KC.MW_DN,  KC.MB_BTN5, XXXXXXX,  XXXXXXX,
        KC.TRNS,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,                                          XXXXXXX,  KC.MB_LMB,  KC.MB_MMB, KC.MB_RMB,  XXXXXXX,  XXXXXXX,
        KC.TRNS,  UNDO,     CUT,      COPY,     PASTE,    XXXXXXX,                                          XXXXXXX,  XXXXXXX,    XXXXXXX,   XXXXXXX,    XXXXXXX,  XXXXXXX,
                            KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,    KC.TRNS,   KC.TRNS,
    ]

]

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
encoder_handler.pins = ((keyboard.encoder_pin_1, keyboard.encoder_pin_0, None, True),)
encoder_handler.map = (
    ((KC.VOLD, KC.VOLU),),  # base layer
    ((KC.VOLD, KC.VOLU),),  # Raise
    ((KC.VOLD, KC.VOLU),),  # Lower
    ((KC.VOLD, KC.VOLU),),  # base layer
    ((KC.VOLD, KC.VOLU),),  # base layer
    ((KC.VOLD, KC.VOLU),),  # base layer
)


if __name__ == '__main__':
    keyboard.go()
