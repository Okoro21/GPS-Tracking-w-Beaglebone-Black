import serial
from serial import Serial
import Adafruit_BBIO.UART as UART

UART.setup("UART1") 
#Initializes UART1 Tx and Rx pins on BBB
GPS = serial.Serial('/dev/ttyO1', 9600)
#Opens up a serial port on the BBB
#.Serial() requires path of serial comm port, and baud rate as an arguments

while(1):
    while GPS.inWaiting() == 0:
        pass
    NMEA = GPS.readline()
    print(NMEA)


