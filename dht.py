import time
import board
import adafruit_dht

#limit the time the sensor can be read
period = 30 #seconds

#Initialize the sensor, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4) #depends on where the signal cable is plugged

#open a file to write to
with open('Temperature_Humidity.log', 'w') as f:
    #start the timer
    start_time = time.monotonic()

    #loop until the time limit is reached
    while time.monotonic() - start_time < period:  #time wil not go backwards
       try:
         # get the readings from the sensor
         temperature_c = dhtDevice.temperature
         temperature_f = temperature_c * (9 / 5) + 32
         humidity = dhtDevice.humidity
         
            #write the readings to the file
         f.write("Temperature: {:.1f} F / {:.1f} C\n"
                 "Humidity: {:.1f}%\n\n"
               .format(temperature_f, temperature_c),humidity)
         
         #to make sure the file is written to
         f.flush()
       except RuntimeError as error:pass #skip error messages
    time.sleep(2.0) #get measurements every 2 seconds

print("Temperature reading completed") #the program is done
