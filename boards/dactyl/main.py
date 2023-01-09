#from dactyl_kb2040 import KMKKeyboard
from dactyl_rp2040 import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.modules.split import Split, SplitType

keyboard = KMKKeyboard()
keyboard.debug_enabled = False

keyboard.modules.append(Layers())
keyboard.modules.append(ModTap())
keyboard.extensions.append(MediaKeys())

# Using drive names (DACTYLL, DACTYLR) to recognize sides; use split_side arg if you're not doing it
split = Split(split_type=SplitType.UART, use_pio=True)
keyboard.modules.append(split)

# Uncomment below if you're having RGB
rgb_ext = RGB(
    pixel_pin=keyboard.rgb_pixel_pin,
    num_pixels=1,
    hue_default=0,
    animation_mode=AnimationModes.OFF,
)
keyboard.extensions.append(rgb_ext)

# Edit your layout below
ESC_LCTL = KC.MT(KC.ESC, KC.LCTL)
QUOTE_RCTL = KC.MT(KC.QUOTE, KC.RCTL)
ENT_LALT = KC.MT(KC.ENT, KC.LALT)
MINUS_RCTL = KC.MT(KC.MINUS, KC.RCTL)
keyboard.keymap = [
    [
        KC.ESC,     KC.N1,      KC.N2,      KC.N3,      KC.N4,      KC.N5,              KC.N6,      KC.N7,      KC.N8,      KC.N9,      KC.N0,      KC.BSPC,
        KC.TAB,     KC.Q,       KC.W,       KC.E,       KC.R,       KC.T,               KC.Y,       KC.U,       KC.I,       KC.O,       KC.P,       KC.ENT,
        KC.LSFT,    KC.A,       KC.S,       KC.D,       KC.F,       KC.G,               KC.H,       KC.J,       KC.K,       KC.L,       KC.SCLN,    KC.QUOTE,
        KC.LCTL,    KC.Z,       KC.X,       KC.C,       KC.V,       KC.B,               KC.N,       KC.M,       KC.COMM,    KC.DOT,     KC.SLSH,    KC.RSFT,
        KC.N1,      KC.LALT,    KC.SPC,     KC.LGUI,    KC.MO(2),   KC.MO(3),           KC.ENT,     KC.SPC,     KC.RALT,    KC.MO(2),   KC.RGUI,    KC.N1,
    ],
    [
        KC.ESC,     KC.N1,      KC.N2,      KC.N3,      KC.N4,      KC.N5,              KC.N6,      KC.N7,      KC.N8,      KC.N9,      KC.N0,      KC.BSPC,
        KC.TAB,     KC.Q,       KC.W,       KC.E,       KC.R,       KC.T,               KC.Y,       KC.U,       KC.I,       KC.O,       KC.P,       KC.ENT,
        KC.LSFT,    KC.A,       KC.S,       KC.D,       KC.F,       KC.G,               KC.H,       KC.J,       KC.K,       KC.L,       KC.SCLN,    KC.QUOTE,
        KC.LCTL,    KC.Z,       KC.X,       KC.C,       KC.V,       KC.B,               KC.N,       KC.M,       KC.COMM,    KC.DOT,     KC.SLSH,    KC.RSFT,
        KC.NO,      KC.NO,      KC.LALT,    KC.SPC,     KC.M,       KC.NO,              KC.NO,      KC.MO(4),   KC.RALT,    KC.RGUI,    KC.NO,      KC.NO,
    ],
    [
        KC.TRNS,    KC.EXCLAIM, KC.AT,      KC.HASH,    KC.DOLLAR,  KC.PERCENT,         KC.CIRC,    KC.AMPR,    KC.ASTR,    KC.LPRN,    KC.RPRN,    KC.EQUAL,
        KC.TAB,     KC.NO,      KC.UP,      KC.NO,      KC.NO,      KC.NO,              KC.GRAVE,   KC.EQUAL,   KC.LPRN,    KC.RPRN,    KC.PIPE,    KC.NO,
        KC.LSFT,    KC.LEFT,    KC.DOWN,    KC.RIGHT,   KC.NO,      KC.NO,              KC.MINUS,   KC.LCBR,    KC.LBRC,    KC.RBRC,    KC.RCBR,    KC.GRAVE,
        KC.LCTL,    KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,              KC.UNDS,    KC.PLUS,    KC.LABK,    KC.RABK,    KC.BSLS,    KC.TILD,
        KC.NO,      KC.NO,      KC.TRNS,    KC.NO,      KC.MO(4),   KC.NO,              KC.NO,      KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.NO,      KC.NO,
    ],
    [
        KC.TRNS,    KC.F1,      KC.F2,      KC.F3,      KC.F4,      KC.F5,              KC.F6,      KC.F7,      KC.F8,      KC.F9,      KC.F10,     KC.NO,
        KC.CAPS,    KC.NO,      KC.UP,      KC.NO,      KC.VOLU,    KC.NO,              KC.PGUP,    KC.PGDN,    KC.DEL,     KC.INS,     KC.F11,     KC.F12,
        KC.TRNS,    KC.LEFT,    KC.DOWN,    KC.RIGHT,   KC.VOLD,    KC.NO,              KC.LEFT,    KC.DOWN,    KC.UP,      KC.RIGHT,   KC.HOME,    KC.END,
        KC.TRNS,    KC.NO,      KC.NO,      KC.NO,      KC.MUTE,    KC.NO,              KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,
        KC.NO,      KC.NO,      KC.TRNS,    KC.MO(4),   KC.NO,      KC.NO,              KC.NO,      KC.TRNS,    KC.TRNS,    KC.TRNS,    KC.NO,      KC.NO,
    ],
    [
        KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,              KC.LGUI(KC.HOME), KC.LGUI(KC.END), KC.NO, KC.NO, KC.NO,     KC.NO,
        KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,              KC.DF(0),   KC.DF(1),   KC.NO,      KC.NO,      KC.NO,      KC.NO,
        KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,              KC.RGB_TOG, KC.RGB_SAI, KC.RGB_HUI, KC.RGB_VAI, KC.RGB_M_P, KC.NO,
        KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,              KC.TRNS,    KC.RGB_SAD, KC.RGB_HUD, KC.RGB_VAD, KC.RGB_M_P, KC.NO,
        KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,              KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,      KC.NO,
    ],
]

if __name__ == '__main__':
    keyboard.go()
