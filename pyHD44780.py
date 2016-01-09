import time
class HD44780(object):
  import smbus as __smbus
  bus = __smbus.SMBus()
  displaycontrol = 0x00
  displaymode = 0x00
  displayfunction = 0x00
  	
  commands = {
      "LCD_CLEARDISPLAY":0x01,
      "LCD_RETURNHOME":0x02,
      "LCD_ENTRYMODESET":0x04,
      "LCD_DISPLAYCONTROL":0x08,
      "LCD_CURSORSHIFT": 0x10,
      "LCD_FUNCTIONSET":0x20,
      "LCD_SETCGRAMADDR":0x40,
      "LCD_SETDDRAMADDR":0x80
      }
  entrymodeflags = {
      "LCD_ENTRYRIGHT":0x00,
      "LCD_ENTRYLEFT":0x02,
      "LCD_ENTRYSHIFTINCREMENT":0x01,
      "LCD_ENTRYSHIFTDECREMENT":0x00
      }
  displaycontrolflags = {
      "LCD_DISPLAYON":0x04,
      "LCD_DISPLAYOFF": 0x00,
      "LCD_CURSORON":0x02,
      "LCD_CURSOROFF":0x00,
      "LCD_BLINKON":0x01,
      "LCD_BLINKOFF":0x00
      }
  cursorshiftflags = {
      "LCD_DISPLAYMOVE":0x08,
      "LCD_CURSORMOVE":0x00,
      "LCD_MOVERIGHT":0x04,
      "LCD_MOVELEFT":0x00
      }
  functionsetflags = {
      "LCD_8BITMODE":0x10,
      "LCD_4BITMODE":0x00,
      "LCD_2LINE":0x08,
      "LCD_1LINE":0x00,
      "LCD_5x10DOTS":0x04,
      "LCD_5x8DOTS":0x00
      }
  def __init__(self,cols,rows,font='5x8'):
    self.cols = cols
    self.rows = rows
    if(rows > 1):
      self.displayfunction |= self.functionsetflags['LCD_2LINE']
    if(font != '5x8' and rows == 1):
      self.displayfunction |= self.functionsetflags['LCD_5x10DOTS']
    self.command(self.commands['LCD_FUNCTIONSET'] | self.displayfunction)
    self.clear()
    self.noCursor()
    self.noBlink()
    self.display()
  def clear(self):
    self.command(self.commands['LCD_CLEARDISPLAY'])
    time.sleep(0.002)
  def home(self):
    self.command(self.commands['LCD_RETURNHOME'])
    time.sleep(0.002)
  def setCursor(self,col,row):
    if(row<0):
      row = 0
    if(row>1):
      row = 1
    if(col > 0x39):
      col = 0x39
    if(col<0):
      col=0
    self.command(self.commands['LCD_SETDDRAMADDR'] | col + (0x40*(row)))
  def noDisplay(self):
    self.displaycontrol &= ~self.displaycontrolflags['LCD_DISPLAYON']
    self.command(self.commands['LCD_DISPLAYCONTROL'] | self.displaycontrol)
  def display(self):
    self.displaycontrol |= self.displaycontrolflags['LCD_DISPLAYON']
    self.command(self.commands['LCD_DISPLAYCONTROL'] | self.displaycontrol)
  def noCursor(self):
    self.displaycontrol &= ~self.displaycontrolflags['LCD_CURSORON']
    self.command(self.commands['LCD_DISPLAYCONTROL'] | self.displaycontrol)
  def cursor(self):
    self.displaycontrol |= self.displaycontrolflags['LCD_CURSORON']
    self.command(self.commands['LCD_DISPLAYCONTROL'] | self.displaycontrol)
  def noBlink(self):
    self.displaycontrol &= ~self.displaycontrolflags['LCD_BLINKON']
    self.command(self.commands['LCD_DISPLAYCONTROL'] | self.displaycontrol)
  def blink(self):
    self.displaycontrol |= self.displaycontrolflags['LCD_BLINKON']
    self.command(self.commands['LCD_DISPLAYCONTROL'] | self.displaycontrol)
  def scrollDisplayLeft(self):
    self.command(self.commands['LCD_CURSORSHIFT'] | self.cursorshiftflags['LCD_DISPLAYMOVE'] | self.cursorshiftflags['LCD_MOVELEFT'])
  def scrollDisplayRight(self):
    self.command(self.commands['LCD_CURSORSHIFT'] | self.cursorshiftflags['LCD_DISPLAYMOVE'] | self.cursorshiftflags['LCD_MOVERIGHT'])
  def leftToRight(self):
    self.displaymode |= self.entrymodeflags['LCD_ENTRYLEFT']
    self.command(self.commands['LCD_ENTRYMODESET'] | self.displaymode)
  def rightToLeft(self):
    self.displaymode &= ~self.entrymodeflags['LCD_ENTRYLEFT']
    self.command(self.commands['LCD_ENTRYMODESET'] | self.displaymode)
  def autoscroll(self):
    self.displaymode |= self.entrymodeflags['LCD_ENTRYSHIFTINCREMENT']
    self.command(self.commands['LCD_ENTRYMODESET'] | self.displaymode)
  def noAutoscroll(self):
    self.displaymode &= ~self.entrymodeflags['LCD_ENTRYSHIFTINCREMENT']
    self.command(self.commands['LCD_ENTRYMODESET'] | self.displaymode)
  def writeString(self,string):
    for x in string:
      self.writeRaw(ord(x))

class Lcd4Bit(HD44780):
  def __init__(self,cols,rows,font='5x8'):
    self.rsPin(0)
    self.rwPin(0)
    self.enablePin(0)
    self.write4bits(0x03)
    time.sleep(0.0041)
    self.write4bits(0x03)
    time.sleep(0.0041)
    self.write4bits(0x03)
    time.sleep(0.000150)
    self.write4bits(0x02)
    self.displayfunction |= self.functionsetflags['LCD_4BITMODE']
    super(Lcd4Bit,self).__init__(cols,rows,font)
  def command(self,command):
    self.rsPin(0)
    self.rwPin(0)
    self.write4bits((command>>4)&0x0f)
    self.write4bits(command&0x0f)
  def writeRaw(self,char):
    self.rsPin(1)
    self.rwPin(0)
    self.write4bits((char>>4)&0x0f)
    self.write4bits(char&0x0f)
    
class PCF8574LCD(Lcd4Bit):
  backlightflag = 1
  def __init__(self,bus,addr,cols,rows,font='5x8'): 
    self.bus.open(bus)
    self.__addr = addr
    self.displayfunction = self.functionsetflags['LCD_4BITMODE'] | self.functionsetflags['LCD_1LINE'] | self.functionsetflags['LCD_5x8DOTS']
    super(self.__class__,self).__init__(cols,rows,font)
  def write4bits(self,value):
    value &= 0b00001111
    reg = self.bus.read_byte(self.__addr)
    reg &= 0b00001111
    reg |= value<<4
    reg |= self.backlightflag<<3
    self.bus.write_byte(self.__addr,reg)
    self.pulseEnable()
  def rsPin(self,value):
    if(value!= 0 and value!=1):
      raise ValueError
    reg = self.bus.read_byte(self.__addr)
    reg &= 0b11111110
    reg |= value
    reg |= self.backlightflag<<3
    self.bus.write_byte(self.__addr,reg)
  def rwPin(self,value):
    if(value!= 0 and value!= 1):
      raise ValueError
    reg = self.bus.read_byte(self.__addr)
    reg &= 0b11111101
    reg |= value<<1
    reg |= self.backlightflag<<3
    self.bus.write_byte(self.__addr,reg)
  def enablePin(self,value):
    if(value!=0 and value!= 1):
      raise ValueError
    reg = self.bus.read_byte(self.__addr)
    reg &= 0b11111011
    reg |= value<<2
    reg |= self.backlightflag<<3
    self.bus.write_byte(self.__addr,reg)
  def pulseEnable(self):
    self.enablePin(0)
    time.sleep(0.000001)
    self.enablePin(1)
    time.sleep(0.000001)
    self.enablePin(0)
    time.sleep(0.000100)
  def backlight(self):
    self.backlightflag = 1
    register = self.bus.read_byte(self.__addr)
    self.bus.write_byte(self.__addr,register|0b00001000)
  def noBacklight(self):
    self.backlightflag = 0
    register = self.bus.read_byte(self.__addr)
    self.bus.write_byte(self.__addr,register&0b11110111)
