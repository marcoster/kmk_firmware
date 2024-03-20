'''
Extension handles usage of AS5013 by AMS
'''

from supervisor import ticks_ms

from kmk.keys import AX
from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)

I2C_ADDRESS = 0x40
I2X_ALT_ADDRESS = 0x41

X = 0x10
Y_RES_INT = 0x11

XP = 0x12
XN = 0x13
YP = 0x14
YN = 0x15

M_CTRL = 0x2B
T_CTRL = 0x2D

Y_OFFSET = 17
X_OFFSET = 7

DEAD_X = 5
DEAD_Y = 5


class Easypoint(Module):
    '''Module handles usage of AS5013 by AMS'''

    def __init__(
        self,
        i2c,
        address=I2C_ADDRESS,
        y_offset=Y_OFFSET,
        x_offset=X_OFFSET,
        dead_x=DEAD_X,
        dead_y=DEAD_Y,
        invert_x=False,
        invert_y=False,
    ):
        self._i2c_address = address
        self._i2c_bus = i2c

        # HID parameters
        self.polling_interval = 20
        self.last_tick = ticks_ms()

        # Offsets for poor soldering
        self.y_offset = y_offset
        self.x_offset = x_offset

        # Deadzone
        self.dead_x = dead_x
        self.dead_y = dead_y

        # Invert
        self.invert_x = invert_x
        self.invert_y = invert_y


    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        now = ticks_ms()
        if now - self.last_tick < self.polling_interval:
            return
        self.last_tick = now

        x, y = self._read_raw_state()

        s_x = self.get_signed8(x) - self.x_offset
        s_y = self.get_signed8(y) - self.y_offset

        if self.invert_x:
            s_x = s_x * -1
        if self.invert_y:
            s_y = s_y * -1

        if s_x < -self.dead_x or s_x > self.dead_x or s_y < -self.dead_y or s_y > self.dead_y:
            AX.X.move(keyboard, s_x)
            AX.Y.move(keyboard, s_y)

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def _read_raw_state(self):
        '''Read data from AS5013'''
        x, y = self._i2c_rdwr([X], length=2)
        return x, y

    def get_signed8(self, number):
        number = number & 0xFF
        if number & 0x80:
            return number - 0xFF
        return number 

    def _i2c_rdwr(self, data, length=1):
        '''Write and optionally read I2C data.'''
        while not self._i2c_bus.try_lock():
            pass

        try:
            if length > 0:
                result = bytearray(length)
                self._i2c_bus.writeto_then_readfrom(
                    self._i2c_address, bytes(data), result
                )
                return result
            else:
                self._i2c_bus.writeto(self._i2c_address, bytes(data))
            return []
        finally:
            self._i2c_bus.unlock()
