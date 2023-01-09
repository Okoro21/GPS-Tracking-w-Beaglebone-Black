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

         ser.write(UPDATE_1_sec)
         sleep(1)
         ser.write(MEAS_1_sec)
         sleep(1)
         ser.write(GPRMC_GPGGA) #Asking only for GPGGA and GPRMC sentances
         sleep(1)
         print("GPS Initialized")
         ser.flushInput() #clears input buffer
         ser.flushInput()

    def read(self):
        ser.flushInput()
        ser.flushInput()
        while ser.inWaiting() == 0:
            pass
        self.NMEA1 = ser.readline()
        while ser.inWaiting == 0:
            pass
        self.NMEA2 = ser.readline()
        NMEA1_array = self.NMEA1.split(b',') 
        NMEA2_array = self.NMEA2.split(b',')
        
        if NMEA1_array[0] == b'$GPRMC':
                self.utc_hours = NMEA1_array[1][:-8]
                self.utc_mins = NMEA1_array[1][-8:-6]
                self.utc_sec = NMEA1_array[1][-6:-3]
                self.latDeg = NMEA1_array[3][:-7]
                self.latMin = NMEA1_array[3][-7:]
                self.latHemi = NMEA1_array[4]
                self.lonDeg = NMEA1_array[5][:-7]
                self.lonMin = NMEA1_array[5][-7:] #Longitude minutes as a decimal number
                self.lonHemi = NMEA1_array[6] #Longitude Hemisphere
                self.knots = NMEA1_array[7] #Speed in Knots
        if NMEA1_array[0] == b'$GPGGA':
                self.fix = NMEA1_array[6] 
                print("My fix is:", self.fix)
                self.altitude = NMEA1_array[9] #Altitude above sea level in meters
                self.sats = NMEA1_array[7] #Number of satilities that are being tracked 
        
        if NMEA2_array[0] == b'$GPRMC':
                self.utc_hours = NMEA2_array[1][:-8]
                self.utc_mins = NMEA2_array[1][-8:-6]
                self.utc_sec = NMEA2_array[1][-6:-3]
                self.latDeg = NMEA2_array[3][:-7]
                self.latMin = NMEA2_array[3][-7:]
                self.latHemi = NMEA2_array[4]
                self.lonDeg = NMEA2_array[5][:-7]
                self.lonMin = NMEA2_array[5][-7:] #Longitude minutes as a decimal number
                self.lonHemi = NMEA2_array[6] #Longitude Hemisphere
                self.knots = NMEA2_array[7] #Speed in Knots
        if NMEA2_array[0] == b'$GPGGA':
                self.fix = NMEA2_array[6] 
                print("My fix is:", self.fix)
                self.altitude = NMEA2_array[9] #Altitude above sea level in meters
                self.sats = NMEA2_array[7] #Number of satilities that are being tracked 


myGPS = GPS() #Instantiating a GPS object 
while(1):
    myGPS.read()
    print(myGPS.NMEA1)
    print(myGPS.NMEA2)
    if (myGPS.fix) != 0:
        print(b"Universal Time: ", myGPS.utc_hours + b':' + myGPS.utc_mins + myGPS.utc_sec)
        print(b"Currently tracking:", myGPS.sats, b"satellites")
        print(b"Current Latitutde", myGPS.latDeg, b"Degrees", myGPS.latMin, b"Minutes", myGPS.latHemi, b"Hemisphere")
        print(b"Current Longitude:", myGPS.lonDeg, b"Degrees", myGPS.lonMin, b"Minutes", myGPS.lonHemi, b"Hemisphere")
        print(b"Speed (knots):", myGPS.knots)
        print(b"Current Altitude:", myGPS.altitude)

            
    



