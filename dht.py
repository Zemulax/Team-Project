import time
import board #define the gpio pin in use
import adafruit_dht #sensor library 
import fcntl #file locking library
import os #operating system library
from datetime import datetime #date and time library
import threading #threading library
import subprocess #subprocess library

#constants
FILE_NAME = "/home/pi/TemperatureFolder/Temperature_Humidity.log"
ERROR_LOG   = "/home/pi/Desktop/Error.log"
PIN_NUMBER = board.D4
HEADER_LINE = "||||Today's Weather Report||||\n\n"
ERROR_MESSAGE = "Reading Temperature Failed. is the Sensor connected?"

#variables
now = datetime.now() #get the current date and time
error_time = now.strftime("%H:%M:%S")
line_number = 2 #line number to start reading from
dhtSensor = adafruit_dht.DHT11(PIN_NUMBER) #Initialize the sensor, with data pin connected to: PIN_NUMBER

#function to call the display.py file
#this function is called in a thread
#so that the program can continue to read the temperature
#while the display is reading from the file
def call_display():
    subprocess.call(["python3", "display.py"]) #call the subprocess
    #for compilation purposes use this line instead: subprocess.call(["python3", os.path.join(sys._MEIPASS, "displayTest.py")]) #

#function to write errors to a file
def error_reporting(error):
    with open(ERROR_LOG, 'w') as error_file:
      error_file.write(error_time + ": ")
      error_file.write(error)
      error_file.flush()
      error_file.close() #clear
      
#function to read temperature from the sensor
#and write it to a file
#the file is locked to prevent data corruption
#the file is flushed to clear the buffer
def read_temperature():
    #create or open a file with read and right permissions
    with open(FILE_NAME, 'w+') as file:

      lines = file.readlines() #read the filelines into a list called lines

      if not lines: #if the file is empty ->
        file.write(ERROR_MESSAGE) #add a header to the file
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
                      error_reporting(ERROR_MESSAGE) #print error messages to the console but continue executing the program
                      continue
                    
              except TypeError:
                      error_reporting(ERROR_MESSAGE)
                      
              except OverflowError:
                     error_reporting("Sensor seems to be disconnected")
                     dhtSensor.exit()
                     quit()
                     
              except KeyboardInterrupt:
                     error_reporting("Program was closed")
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
