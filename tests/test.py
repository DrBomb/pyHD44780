from pyHD44780 import PCF8574LCD

lcd = PCF8574LCD(1,0x3f,16,2)

lcd.writeString("Hello World!")
