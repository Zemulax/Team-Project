import time
import board #define the gpio pin in use
import adafruit_dht #sensor library 
import fcntl #file locking library
import os #operating system library
from datetime import datetime #date and time library
import threading #threading library
import subprocess #subprocess library
import sys

#constants
FILE_NAME = "/home/pi/TemperatureFolder/Temperature_Humidity.log"
PIN_NUMBER = board.D4
HEADER_LINE = "||||Today's Weather Report||||\n\n"
INFO = "" #add an empty line

#variables
line_number = 2 #line number to start reading from
dhtSensor = adafruit_dht.DHT11(PIN_NUMBER) #Initialize the sensor, with data pin connected to: PIN_NUMBER

#this function simply exits the program
#upon specified error occurrence
def quit():
  sys.exit(0)
  
#function to call the hygrometergui.py file
#this function is called in a thread
#so that the program can continue to read the temperature
#while the display is reading from the file
def call_display():
    subprocess.call(["python3", "/home/pi/Desktop/TestFolder/nearfinal/hygrometergui.py"]) #call the subprocess
    #subprocess.call(["python3", os.path.join(sys._MEIPASS, "hygrometergui.py")]) #when creating an executable use this line

#function to write errors to a file
def error_reporting(error):
    with open("/home/pi/TemperatureFolder/Temperature_Humidity.log", 'w') as file:
      file.truncate()
      file.write(error)
      file.flush()
      
#function to read temperature from the sensor
#and write it to a file
#the file is locked to prevent data corruption
#the file is flushed to clear the buffer and make sure it is written to
def read_temperature():
    #create or open a file with read and right permissions
    with open(FILE_NAME, 'w+') as file:

      lines = file.readlines() #read the filelines into a list called lines

      if not lines: #if the file is empty ->
        file.write(INFO) #add a header line as starting point
        lines.append(HEADER_LINE) #add a header to the list

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
              
              #catch errors
              except RuntimeError as error: 
                     error_reporting("Awaiting Sensor...") #print error messages to the display but continue executing the program
                     time.sleep(30)
                     continue
                    
              except TypeError:
                     file.write("Unable to Read from Sensor")
                     time.sleep(10)
                     continue
                      
              except OverflowError:
                     error_reporting("Halted.Connect Sensor and Restart Program")
                     time.sleep(20)
                     quit()
       
              except KeyboardInterrupt:
                     dhtSensor.exit()
                     quit()

      dhtSensor.exit() #close the sensor        

def main():
  thread = threading.Thread(target=call_display) #create a thread
  thread.start() #start the thread
  read_temperature() #call the read_temperature function

#call the main function
#when the program is executed
#this is the entry point of the program
if __name__ == "__main__":
  main() #call the main function
