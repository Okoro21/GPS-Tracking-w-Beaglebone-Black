import serial
import Adafruit_BBIO.UART as UART
from time import sleep 
UART.setup("UART1")
#.setup() initalizes UART1 on the BBB 
ser = serial.Serial('/dev/ttyO1', 9600)
#Opens up the serial port on the BBB

class GPS:
    def __init__(self):
         UPDATE_10_sec = b'$PMTK220,10000*2F\r\n'
         #Update Every 10 Seconds
         UPDATE_5_sec = b'$PMTK220,5000*1B\r\n'  
         #Update Every 5 Seconds
         UPDATE_1_sec = b'$PMTK220,1000*1F\r\n'  
         #Update Every One Second
         UPDATE_200_msec = b'$PMTK220,200*2C\r\n' 
         #Update Every 200 Milliseconds
        
         #This set is used to set the rate the GPS takes measurements
         MEAS_10_sec = b'$PMTK300,10000,0,0,0,0*2C\r\n'
         #Measure every 10 seconds
         MEAS_5_sec = b'$PMTK300,5000,0,0,0,0*18\r\n'  
         #Measure every 5 seconds
         MEAS_1_sec = b'$PMTK300,1000,0,0,0,0*1C\r\n'  
         #Measure once a second
         MEAS_200_msec= b'$PMTK300,200,0,0,0,0*2F\r\n'
        # MEAS_200_msec.format(MEAS_200_msec)
        #MEAS_200_msec = bytes(MEAS_200_msec, 'ascii')
         #ser.write(MEAS_200_msec.encode())
         #Meaure 5 times a second
        
         #Set the Baud Rate of GPS
         BAUD_57600 = b'$PMTK251,57600*2C\r\n' #Set Baud Rate at 57600
         BAUD_9600 = b'$PMTK251,9600*17\r\n'    #Set 9600 Baud Rate
         #Commands for which NMEA Sentences are sent
         GPRMC_ONLY = b'$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n'
         #Send only the GPRMC Sentence
         GPRMC_GPGGA = b'$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n'
         #Send GPRMC AND GPGGA Sentences
         SEND_ALL = b'$PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n'
         #Send All Sentences
         SEND_NOTHING = b'$PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n'
         #Send Nothing

         ser.write(UPDATE_200_msec)
         sleep(1)
         ser.write(MEAS_200_msec)
         sleep(1)
         ser.write(GPRMC_GPGGA)
         sleep(1)
         print("GPS Initialized")

myGPS = GPS()
#Instantiating a GPS object 
while(1):
    ser.flushInput() #clears out the input buffer
    ser.flushInput()
    while ser.inWaiting() == 0:
        pass
    NMEA1 = ser.readline()
    NMEA2 = ser.readline()
    print(NMEA1)
    print(NMEA2)
    
