import time
import board
import adafruit_dht

#Initialize the sensor, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4) #depends on where the signal cable is plugged
while True:
    try:
         # Print the values to the serial port
         temperature_c = dhtDevice.temperature
         temperature_f = temperature_c * (9 / 5) + 32
         print("Temperature: {:.1f} F / {:.1f} C"
               .format(temperature_f, temperature_c))
    except RuntimeError as error:pass #skip error messages
    time.sleep(2.0) #get measurements every 2 seconds
