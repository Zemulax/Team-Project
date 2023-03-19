import time
import board #define the gpio pin in use
import adafruit_dht #sensor library 

#limit the time the sensor can be read
line_number = 2 #line number to start reading from

#Initialize the sensor, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4) #depends on where the signal cable is plugged

#open a file to write to
with open('Temperature_Humidity.log', 'r+') as f:
  
  lines = f.readlines() #read the file
  
  if not lines: #if the file is empty
    lines.append("Temperature\n") #add a header to the file
    
    #start the timer
    start_time = time.monotonic()
    #loop until the time limit is reached
    while  True:
          try:
                  # get the readings from the sensor
                  temperature_c = dhtDevice.temperature 
                  temperature_f = temperature_c * (9 / 5) + 32
                  humidity = dhtDevice.humidity#
                  
                  #write the readings to the file
                  lines [line_number-1] = f.write("Temperature: {:.1f} F / {:.1f} C\n"
                  "Humidity: {:.1f}%\n\n"
                  .format(temperature_f, temperature_c, humidity))
                  f.seek(0) #go to the beginning of the file
                  f.writelines(lines)
                  f.truncate() #delete the rest of the file
                  
                  #to make sure the file is written to
                  f.flush()
          except RuntimeError as error:pass #skip error messages
          time.sleep(2.0) #get measurements every 2 seconds
    
         

print("Temperature reading completed") #the program is done
