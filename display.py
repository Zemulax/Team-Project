# Description: This program displays the contents of the log file in a GUI window
#the log files comes from the dht.py program
                               
import tkinter as tk
import asyncio
import os

#create a new window for displaying the file contents from the log
window = tk.Tk()
window.title("Sensor Log")
window.geometry("280x600")
window.configure(bg="purple")
window.configure(borderwidth=10, relief="groove")
window.resizable(width=False, height=False)

#display the file content here
text_widget = tk.Text(window)
text_widget.pack(fill="both", expand=True)

#read cotents from the log
async def read_file(filename):
     while True:
          with open(filename, "r") as file:
              for line in file:
                     #insert the file content into the widget
                     text_widget.insert("end", line)
                     text_widget.update() #update the widget with new information
              await asyncio.sleep(3) #wait 3 seconds before reading the file again

async def main():
    filename = "/home/pi/Desktop/Temperature_Humidity.log"
    if os.path.exists(filename): #returns true if file exists
         await read_file(filename)
    else: text_widget.insert("end","""Sensor log was not found!!\nIs the sensor running?\n"""
                             """Restart this program when the sensor is operational.""")

if __name__ == '__main__':
     asyncio.run(main())
     window.mainloop() #display the window

