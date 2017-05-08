import time
from .base import Lcd4Bit


class PCFLCD(Lcd4Bit):
    backlightflag = 1

    def __init__(self, bus, addr, cols, rows, font='5x8'):
        self.__bus = bus
        self.__addr = addr
        super(self.__class__, self).__init__(cols, rows, font)

    def write4bits(self, value):
        value &= 0b00001111
        reg = self.__bus.read_byte(self.__addr)
        reg &= 0b00001111
        reg |= value << 4
        reg |= self.backlightflag << 3
        self.__bus.write_byte(self.__addr, reg)
        self.pulse_enable()

    def rs_pin(self, value):
        if value != 0 and value != 1:
            raise ValueError
        reg = self.__bus.read_byte(self.__addr)
        reg &= 0b11111110
        reg |= value
        reg |= self.backlightflag << 3
        self.__bus.write_byte(self.__addr, reg)

    def rw_pin(self, value):
        if value != 0 and value != 1:
            raise ValueError
        reg = self.__bus.read_byte(self.__addr)
        reg &= 0b11111101
        reg |= value << 1
        reg |= self.backlightflag << 3
        self.__bus.write_byte(self.__addr, reg)

    def enable_pin(self, value):
        if value != 0 and value != 1:
            raise ValueError
        reg = self.__bus.read_byte(self.__addr)
        reg &= 0b11111011
        reg |= value << 2
        reg |= self.backlightflag << 3
        self.__bus.write_byte(self.__addr, reg)

    def pulse_enable(self):
        self.enable_pin(0)
        time.sleep(0.000001)
        self.enable_pin(1)
        time.sleep(0.000001)
        self.enable_pin(0)
        time.sleep(0.000100)

    def backlight(self):
        self.backlightflag = 1
        register = self.__bus.read_byte(self.__addr)
        self.__bus.write_byte(self.__addr, register | 0b00001000)

    def no_backlight(self):
        self.backlightflag = 0
        register = self.__bus.read_byte(self.__addr)
        self.__bus.write_byte(self.__addr, register & 0b11110111)