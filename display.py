# Description: This program displays the contents of the log file in a GUI window
                               
import tkinter as tk #tkinter library
import os #operating system library
import fcntl #file locking library
import time #time library
import threading #threading library
from queue import Queue #queue library
import sys

#this class creates a window for displaying the file contents
#it also creates a thread for reading the file
#and a function for updating the text widget
#the thread is started in the main function
#the update function is called in the mainloop
#the update function is called periodically
class DispClass(tk.Frame):
     #initialize the class
    def __init__(self, master=None):
        super().__init__(master)
        frame = tk.Frame(self.master)
        frame.pack(fill="both", expand=True)

        # create a text widget for displaying the file contents
        self.text_widget = tk.Text(frame, bg="midnightblue", fg= "white",font=("Arial", 16))
        self.text_widget.pack(fill="both", expand=True)
        
     #function for reading the file
     #the file is locked to prevent data corruption
     #the file is unlocked to allow other processes to access it
    def read_file(self, q, filename):
        while True:
            try:
                with open(filename, "r") as file:
                     # lock the file
                    fcntl.flock(file, fcntl.LOCK_SH)

                    for line in file:
                        # insert the file content into the queue
                        q.put(line)
                    #unlock the file
                    fcntl.flock(file, fcntl.LOCK_UN)

                time.sleep(10) #wait 10 seconds before reading the file again
                # clear the text widget
                self.text_widget.delete("1.0", "end")
            
            except tk.TclError as error:  # program will know that its been closed on purpose
                quit("Program was closed")
                

#main function
#creates a new window for displaying the file contents
#creates a new window for displaying the error message
#starts the thread
#calls the update function periodically
#calls the mainloop
#the mainloop is called in the main function
def main():
# create a new window for displaying the file contents from the log
    window = tk.Tk()
    window.title("Hygrometer")
    window.geometry("307x210")
    window.configure(bg="white")
    window.configure(borderwidth=10, relief="sunken")
    window.resizable(width=False, height=False)

    #icon = tk.PhotoImage(file="home/pi/Desktop/TestFolder/magni/icon.png")
    #window.iconphoto(True, icon)

    disp = DispClass(master=window)
    disp.pack(fill="both", expand=True)
    
    filename = "/home/pi/TemperatureFolder/Temperature_Humidity.log"
    if os.path.exists(filename):  # returns true if file exists
        

        q = Queue()
        t = threading.Thread(target=disp.read_file, args=(q, filename))
        t.start()

        def update_text_widget():
            while not q.empty():
                line = q.get_nowait()
                disp.text_widget.insert("end",line)
                disp.text_widget.see("end")
            window.after(500, update_text_widget)
            
        window.after(500, update_text_widget)
        window.mainloop()
        
    else:

        disp.text_widget.insert("end", """Sensor log was not found!!\nIs the sensor running?\n"""
                                       """Restart this program when the sensor is operational""")
        disp.text_widget.configure(state="disabled")  # disabled editing

    window.mainloop()

if __name__ == '__main__':
    main()
