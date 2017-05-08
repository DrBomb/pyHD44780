import time


class HD44780(object):
    displaycontrol = 0x00
    displaymode = 0x00
    displayfunction = 0x00

    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    def __init__(self, cols, rows, font='5x8'):
        self.cols = cols
        self.rows = rows
        if rows > 1:
            self.displayfunction |= self.LCD_2LINE
        if font != '5x8' and rows == 1:
            self.displayfunction |= self.LCD_5x10DOTS
        self.command(self.LCD_FUNCTIONSET | self.displayfunction)
        self.clear()
        self.no_cursor()
        self.no_blink()
        self.display()

    def clear(self):
        self.command(self.LCD_CLEARDISPLAY)
        time.sleep(0.002)

    def home(self):
        self.command(self.LCD_RETURNHOME)
        time.sleep(0.002)

    def set_cursor(self, col, row):
        if row < 0:
            row = 0
        if row > 1:
            row = 1
        if col > 0x39:
            col = 0x39
        if col < 0:
            col = 0
        self.command(self.LCD_SETDDRAMADDR | col + (0x40*row))

    def no_display(self):
        self.displaycontrol &= ~self.LCD_DISPLAYON
        self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def display(self):
        self.displaycontrol |= self.LCD_DISPLAYON
        self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def no_cursor(self):
        self.displaycontrol &= ~self.LCD_CURSORON
        self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor(self):
        self.displaycontrol |= self.LCD_CURSORON
        self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def no_blink(self):
        self.displaycontrol &= ~self.LCD_BLINKON
        self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def blink(self):
        self.displaycontrol |= self.LCD_BLINKON
        self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def scroll_display_left(self):
        self.command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)

    def scroll_display_right(self):
        self.command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT)

    def left_to_right(self):
        self.displaymode |= self.LCD_ENTRYLEFT
        self.command(self.LCD_ENTRYMODESET | self.displaymode)

    def right_to_left(self):
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.command(self.LCD_ENTRYMODESET | self.displaymode)

    def autoscroll(self):
        self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        self.command(self.LCD_ENTRYMODESET | self.displaymode)

    def no_autoscroll(self):
        self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.command(self.LCD_ENTRYMODESET | self.displaymode)

    def write_string(self, string):
        for x in string:
            self.write_raw(ord(x))


class Lcd4Bit(HD44780):
    def __init__(self, cols, rows, font='5x8'):
        self.rs_pin(0)
        self.rw_pin(0)
        self.enable_pin(0)
        self.write4bits(0x03)
        time.sleep(0.0041)
        self.write4bits(0x03)
        time.sleep(0.0041)
        self.write4bits(0x03)
        time.sleep(0.000150)
        self.write4bits(0x02)
        self.displayfunction |= self.LCD_4BITMODE
        super(Lcd4Bit, self).__init__(cols, rows, font)

    def command(self, command):
        self.rs_pin(0)
        self.rw_pin(0)
        self.write4bits((command >> 4) & 0x0f)
        self.write4bits(command & 0x0f)

    def write_raw(self, char):
        self.rs_pin(1)
        self.rw_pin(0)
        self.write4bits((char >> 4) & 0x0f)
        self.write4bits(char & 0x0f)

