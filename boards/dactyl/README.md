# Dactyl Manuform Keyboard

A split keyboard with a 4x6 columnar stagger and 5 thumb keys. Usually those keyboards are handwired.

Keyboard works with controllers having Pro Micro layout. Existing configurations:

| PCB version | Board                                                                | Config file               |
|:-----------:|----------------------------------------------------------------------|---------------------------|
|     1.*     | [Sparkfun Pro Micro RP2040](https://www.sparkfun.com/products/18288) | dactyl_rp2040             |
|     1.*     | [Adafruit KB2040](https://www.adafruit.com/product/5302)             | dactyl_kb2040             |
|     2.*     | [Sparkfun Pro Micro RP2040](https://www.sparkfun.com/products/18288) | _waiting for pinout docs_ |
|     2.*     | [Adafruit KB2040](https://www.adafruit.com/product/5302)             | _waiting for pinout docs_ |

## Compatibility issues

- **TRRS connection** - KMK has no protocol for one-pin communication between two splits. So, if you are using TRRS wire
  connection, only right side send matrix events to the left side. No issue when using BLE.

## `main.py` example config

The layout is my own layout that I'm used now from using mask and sofle keyboards.

It has the following modules/extensions enabled:

- [Split](https://github.com/KMKfw/kmk_firmware/tree/master/docs/split_keyboards.md) Connects halves using a wire
- [Layers](https://github.com/KMKfw/kmk_firmware/tree/master/docs/layers.md) Do you need more keys than switches? Use
  layers.
- [ModTap](https://github.com/KMKfw/kmk_firmware/blob/master/docs/modtap.md) Enable press/hold double binding of keys
- [MediaKeys](https://github.com/KMKfw/kmk_firmware/blob/master/docs/media_keys.md) Common media controls

## More steps required during install

In order to mitigate lack of one-wire protocol, KMK use its UART implementation but with special low-level PIO
subprogram available only on RP2040. It allows using other pins for UART than on-board RX and TX.

Because of the above, besides of normal installation steps, you have to also:

- install Circuit Python in 7.2+ version
- add `adafruit_pioasm.mpy` library to lib or root folder of a board
