from pyLiquidCrystal.I2C import PCFLCD
from smbus import SMBus

bus = SMBus(1)
lcd = PCFLCD(bus,0x3f,16,2)

lcd.setCursor(5,0)
lcd.writeString("Hello")
lcd.setCursor(5,1)
lcd.writeString("World!")
