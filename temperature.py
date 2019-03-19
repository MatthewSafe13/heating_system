import RPi.GPIO as GPIO
import os
import glob
import time
from RPLCD import CharLCD

GPIO.setwarnings(False)

class Pi:

    def __init__(self, board, warnings): 
        self.board = board
        self.warning = warnings

    def set_mode(self):
        if self.board == "BCM":
            GPI0.setmode(GPI0.BCM)
            print("board is set to BCM")
        elif self.board == "BOARD":
            GPI0.setmode(GPI0.BOARD)
            print("board set to BOARD")
        else:
            print("board not set")

    def set_warnings(self):
        if self.warnings == "False":
            GPIO.setwarnings(False)
            print("warnings set to False")
        elif self.warnings == "True":
            GPIO.setwarnings(True)
            print("Warnings set to true")       
        else:
            print("warnings not set")

pi = Pi("BCM", "False")


class LCD:
    # commands
    LCD_CLEARDISPLAY        = 0x01
    LCD_RETURNHOME          = 0x02
    LCD_ENTRYMODESET        = 0x04
    LCD_DISPLAYCONTROL      = 0x08
    LCD_CURSORSHIFT         = 0x10
    LCD_FUNCTIONSET         = 0x20
    LCD_SETCGRAMADDR        = 0x40
    LCD_SETDDRAMADDR        = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT      = 0x00
    LCD_ENTRYLEFT       = 0x02
    LCD_ENTRYSHIFTINCREMENT     = 0x01
    LCD_ENTRYSHIFTDECREMENT     = 0x00

    # flags for display on/off control
    LCD_DISPLAYON       = 0x04
    LCD_DISPLAYOFF      = 0x00
    LCD_CURSORON        = 0x02
    LCD_CURSOROFF       = 0x00
    LCD_BLINKON         = 0x01
    LCD_BLINKOFF        = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE      = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE      = 0x00
    LCD_MOVERIGHT       = 0x04
    LCD_MOVELEFT        = 0x00

    # flags for function set
    LCD_8BITMODE        = 0x10
    LCD_4BITMODE        = 0x00
    LCD_2LINE           = 0x08
    LCD_1LINE           = 0x00
    LCD_5x10DOTS        = 0x04
    LCD_5x8DOTS         = 0x00

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#CELSIUS CALCULATION
def read_temp_c():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = int(temp_string) / 1000.0 # TEMP_STRING IS THE SENSOR OUTPUT
        temp_c = str(round(temp_c, 1)) # ROUND THE RESULT TO 1 PLACE
        return temp_c

#FAHRENHEIT CALCULATION
def read_temp_f():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_f = (int(temp_string) / 1000.0) * 9.0 / 5.0 + 32.0 # TEMP_STRING IS THE SENSOR OUTPUT
        temp_f = str(round(temp_f, 1)) # ROUND THE RESULT TO 1 PLACE
        return temp_f

while True:

    lcd.cursor_pos = (0, 0)
    lcd.write_string("Twist for bright")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("-ness & contrast")

    time.sleep(3)
    lcd.clear()

    lcd.cursor_pos = (0, 0)
    lcd.write_string("Temp: " + read_temp_c() + unichr(223) + "C")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Temp: " + read_temp_f() + unichr(223) + "F")

    time.sleep(5)

