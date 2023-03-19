import time
import board #define the gpio pin in use
import adafruit_dht #sensor library 
import fcntl #file locking library
import os #operating system library

#constants
FILE_NAME = "/home/pi/Desktop/Temperature_Humidity.log"
ERROR_LOG   = "/home/pi/Desktop/Error.log"
PIN_NUMBER = board.D4
HEADER_LINE = "||||Temperature & Humidity Gauge||||\n\n"
ERROR_MESSAGE = "Reading Temperature Failed. is the Sensor connected?"


line_number = 2 #line number to start reading from

#Initialize the sensor, with data pin connected to:
dhtSensor = adafruit_dht.DHT11(PIN_NUMBER) #depends on where the signal cable is plugged

def read_temperature(): #function to read temperature from the sensor

    #create or open a file with read and right permissions
    with open(FILE_NAME, 'w+') as file:

      lines = file.readlines() #read the file

      if not lines: #if the file is empty ->
        file.write(ERROR_MESSAGE) #add a header to the file
        lines.append(HEADER_LINE)

        #loop forever
        while True:
              try:
                      fcntl.flock(file,fcntl.LOCK_SH) #lock the file
                      
                      # assign temp reading to variables
                      temperature_c = dhtSensor.temperature 
                      temperature_f = temperature_c * (9/5) + 32
                      humidity = dhtSensor.humidity 

                      #assign temp reading to the lines, replacing their current text
                      if len(lines) >= line_number:
                           lines [line_number-1] = f"Temperature\n{temperature_f:.1f} F | {temperature_c:.1f}°C\n\nHumidity\n{humidity:.1f}%"
                      else:
                          lines.append(f"Temperature\n{temperature_f:.1f} F | {temperature_c:.1f}°C\n\nHumidity\n{humidity:.1f}%")
                      
                      file.seek(0) #go to the beginning of the file
                      file.writelines(lines) # write line to the file
                      fcntl.flock(file, fcntl.LOCK_UN) #unlock the file
                      file.truncate() #delete the rest of the file
                      file.flush() #flush the buffer
                      time.sleep(5.0) #get measurements every 2 secon

              except RuntimeError as error: #catch errors
                      error_reporting(ERROR_MESSAGE) #print error messages to the console but continue executing the program
                      continue
                    
              except TypeError:
                      error_reporting(ERROR_MESSAGE)
                      
              except OverflowError:
                     error_reporting("Sensor seems to be disconnected")
                     dhtsensor.exit()
                     quit()
                     
              except KeyboardInterrupt:
                     error_reporting("Program was closed")
                     dhtsensor.exit()
                     quit()

      dhtSensor.exit() #close the sensor        

print("Temperature reading completed") #the program is done
