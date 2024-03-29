try:
    from typing import Callable
except ImportError:
    pass

from micropython import const

from kmk.keys import AX, KC
from kmk.modules import Module
from kmk.utils import Debug

import time

debug = Debug(__name__)

_ADDRESS = const(0x2A)

_MASK_READ = const(0xA0)
_MASK_WRITE = const(0x80)

_REG_FW_ID = const(0x00)
_REG_FW_VER = const(0x01)
_REG_STATUS = const(0x02)
_REG_SYS_CFG = const(0x03)
_REG_FEED_CFG1 = const(0x04)
_REG_FEED_CFG2 = const(0x05)
_REG_FEED_CFG3 = const(0x06)
_REG_CAL_CFG = const(0x07)
_REG_AUX_CTL = const(0x08)
_REG_SAMPLE_RATE = const(0x09)
_REG_ZIDLE = const(0x0A)
_REG_Z_SCALER = const(0x0B)
_REG_SLEEP_INTERVAL = const(0x0C)
_REG_SLEEP_TIMER = const(0x0D)
_REG_DATA = const(0x12)

_EXT_REG_AXS_VALUE = const(0x1C)
_EXT_REG_AXS_ADDR_HIGH = const(0x1C)
_EXT_REG_AXS_ADDR_LOW = const(0x1D)
_EXT_REG_AXS_CTRL = const(0x1E)
_EXT_REG_ADCCONFIG = const(0x0187)

_EREG_AXS_READ = const(0x01)
_EREG_AXS_WRITE = const(0x02)
_EREG_AXS_INC_ADDR_READ = const(0x04)

_EREG_ADCCONFIG_ADC_ATTENUATE_MASK = const(0xC2)
_EREG_ADCCONFIG_ADC_ATTENUATE_1X = const(0x00)
_EREG_ADCCONFIG_ADC_ATTENUATE_2X = const(0x40)
_EREG_ADCCONFIG_ADC_ATTENUATE_3X = const(0x80)
_EREG_ADCCONFIG_ADC_ATTENUATE_4X = const(0xC0)

_CAL_CFG_CALIBRATE = const(0x01)

_FEED1_ENABLE = const(0x01)
_FEED1_ABSOLUTE = const(0x02)
_FEED1_NO_FILTER = const(0x04)
_FEED1_NO_X_DATA = const(0x08)
_FEED1_NO_Y_DATA = const(0x10)
_FEED1_INVERT_X = const(0x40)
_FEED1_INVERT_Y = const(0x80)

_FEED2_INTELLIMOUSE = const(0x01)
_FEED2_NO_TAPS = const(0x02)
_FEED2_NO_SEC_TAPS = const(0x04)
_FEED2_NO_SCROLL = const(0x08)
_FEED2_NO_GLIDEEXTEND = const(0x10)
_FEED2_SWAP_XY = const(0x80)

_FEED3_DISABLE_CROSS_RATE_SMOOTHING = const(0x02)


class AbsoluteHandler:
    cfg = (
        (_REG_FEED_CFG2, 0x00),
        (_REG_FEED_CFG1, _FEED1_ENABLE | _FEED1_NO_FILTER | _FEED1_ABSOLUTE | _FEED1_INVERT_X)
    )

    def handle(buffer: bytearray, keyboard) -> None:
        button = buffer[0]
        x_low = buffer[2]
        y_low = buffer[3]
        high = buffer[4]
        z_lvl = buffer[5]

        x_pos = ((high & 0x0F) << 8) | x_low
        y_pos = ((high & 0xF0) << 4) | y_low

        if debug.enabled:
            debug(
                'buttons:',
                bin(button),
                ' x_pos:',
                x_pos,
                ' y_pos:',
                y_pos,
                'z_lvl:',
                z_lvl,
            )


class RelativeHandler:
    cfg = (
        #(_REG_FEED_CFG2, _FEED2_NO_GLIDEEXTEND | _FEED2_INTELLIMOUSE ),
        (_REG_FEED_CFG2, _FEED2_NO_GLIDEEXTEND | _FEED2_INTELLIMOUSE | _FEED2_NO_SEC_TAPS | _FEED2_NO_SCROLL),
        (_REG_FEED_CFG1, 0x00)
    )
    def __init__(self):
        self._button_left_tapped = False

    def handle(self, buffer: bytearray, keyboard) -> None:
        button = buffer[0] & 0b00000111
        x_sign = buffer[0] & 0b00010000
        y_sign = buffer[0] & 0b00100000
        x_delta = buffer[1]
        y_delta = buffer[2]
        w_delta = buffer[3]

        if x_sign:
            x_delta -= 0xFF
        if y_sign:
            y_delta -= 0xFF

        if x_delta != 0:
            AX.X.move(keyboard, x_delta)
        if y_delta != 0:
            AX.Y.move(keyboard, -y_delta)

        if button & 0x01:
            if(self._button_left_tapped == False):
                self._button_left_tapped = True
                keyboard.tap_key(KC.MB_LMB)
        else:
            self._button_left_tapped = False

        if debug.enabled:
            debug(
                'buttons:',
                bin(button),
                ' x_delta:',
                x_delta,
                ' y_delta:',
                y_delta,
                ' w_delta',
                w_delta,
            )


class GlidePoint(Module):
    def __init__(self, i2c):
        self._i2c = i2c

        self.handler = RelativeHandler()
        #self.handler = AbsoluteHandler

    def _read(self, addr, n):
        rbuf = bytearray(n)
        wbuf = bytearray(1)
        wbuf[0] = addr | _MASK_READ

        while not self._i2c.try_lock():
            pass
        try:
            self._i2c.writeto_then_readfrom(_ADDRESS, wbuf, rbuf)
            return rbuf
        finally:
            self._i2c.unlock()

    def _read_extended(self, addr, n):
        rbuf = bytearray(n)
        self._enable_feed(False)
        self._write(_EXT_REG_AXS_ADDR_HIGH, addr >> 8)
        self._write(_EXT_REG_AXS_ADDR_LOW, addr & 0xFF)

        for i in range(0, n):
            self._write(_EXT_REG_AXS_CTRL, _EREG_AXS_INC_ADDR_READ | _EREG_AXS_READ)
            time.sleep(0.021)
            rbuf[i] = self._read(_EXT_REG_AXS_VALUE, 1)[0]
        self._clear_flags()
        return rbuf

    def _write(self, addr, data):
        wbuf = bytearray(2)
        wbuf[0] = addr | _MASK_WRITE
        wbuf[1] = data
        while not self._i2c.try_lock():
            pass
        try:
            self._i2c.writeto(_ADDRESS, wbuf)
        finally:
            self._i2c.unlock()

    def _write_extended(self, addr, data):
        self._enable_feed(False)
        self._write(_EXT_REG_AXS_VALUE, data)
        self._write(_EXT_REG_AXS_ADDR_HIGH, addr >> 8)
        self._write(_EXT_REG_AXS_ADDR_LOW, addr & 0xFF)
        self._write(_EXT_REG_AXS_CTRL, _EREG_AXS_WRITE)
        time.sleep(0.021)
        self._clear_flags()

    def _check_firmware(self) -> bool:
        fw = self._read(_REG_FW_ID, 2)
        return fw[:2] == b'\x07:'

    def _clear_flags(self) -> None:
        self._write(_REG_STATUS, 0x00)

    def _enable_feed(self, enable):
        en = self._read(_REG_FEED_CFG1, 1)
        if enable:
            self._write(_REG_FEED_CFG1, en[0] | _FEED1_ENABLE)
        else:
            self._write(_REG_FEED_CFG1, en[0] & ~_FEED1_ENABLE)

    def _set_adc_attenuation(self, gain):
        adcconfig = self._read_extended(_EXT_REG_ADCCONFIG, 1)
        adcconfig = adcconfig[0]
        gain &= _EREG_ADCCONFIG_ADC_ATTENUATE_MASK
        if gain == adcconfig & _EREG_ADCCONFIG_ADC_ATTENUATE_MASK:
            return False
        adcconfig &= ~_EREG_ADCCONFIG_ADC_ATTENUATE_MASK
        adcconfig |= gain
        self._write_extended(_EXT_REG_ADCCONFIG, adcconfig)
        return True

    def _calibrate(self):
        cal = self._read(_REG_CAL_CFG, 1)
        cal = cal[0]
        cal |= _CAL_CFG_CALIBRATE
        self._write(_REG_CAL_CFG, cal)
        time.sleep(0.2)
        self._clear_flags()

    def cursor_smoothing(self, enable):
        en = self._read(_REG_FEED_CFG3, 1)
        if enable:
            self._write(_REG_FEED_CFG3, en[0] & ~_FEED3_DISABLE_CROSS_RATE_SMOOTHING)
        else:
            self._write(_REG_FEED_CFG3, en[0] | _FEED3_DISABLE_CROSS_RATE_SMOOTHING)

    def _configure(self) -> None:
        for cfg in self.handler.cfg:
            self._write(cfg[0], cfg[1])

    def _data_ready(self) -> bool:
        data_ready = self._read(_REG_STATUS, 1)
        return data_ready[0] != 0x00

    def during_bootup(self, keyboard):
        if not self._check_firmware:
            raise OSError('Firmware ID mismatch')
        self._write(_REG_SYS_CFG, 0x01) # reset
        time.sleep(0.03)
        self._clear_flags()
        self._configure()
        self._set_adc_attenuation(_EREG_ADCCONFIG_ADC_ATTENUATE_4X)
        self._calibrate()
        self._enable_feed(True)

    def before_matrix_scan(self, keyboard):
        pass

    def after_matrix_scan(self, keyboard):
        if not self._data_ready():
            return

        data = self._read(_REG_DATA, 6)

        self.handler.handle(data, keyboard)

        self._clear_flags()

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        self._write(_REG_SYS_CFG, 0x04)

    def on_powersave_disable(self, keyboard):
        self._write(_REG_SYS_CFG, 0x00)
