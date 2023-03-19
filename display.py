# Description: This program displays the contents of the log file in a GUI window
                               
import tkinter as tk #tkinter library
import os #operating system library
import fcntl #file locking library
import time #time library
import threading #threading library
from queue import Queue #queue library

class DispClass(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        frame = tk.Frame(self.master)
        frame.pack(fill="both", expand=True)

        # display the file content here
        self.text_widget = tk.Text(frame, bg="midnightblue", fg= "white",font=("Arial", 16))
        self.text_widget.pack(fill="both", expand=True)
        self.label = tk.Label(frame, text="Reading Temperature...", fg="white")
        self.label.pack()

    def read_file(self, q, filename):
        while True:
            try:
                with open(filename, "r") as file:
                    fcntl.flock(file, fcntl.LOCK_SH)

                    for line in file:
                        # insert the file content into the queue
                        q.put(line)
                         
                    fcntl.flock(file, fcntl.LOCK_UN)

                time.sleep(10)
                self.text_widget.delete("1.0", "end")
            except tk.TclError as error:  # program will know that its been closed on purpose
                print("Program was closed", error)
                return


def main():
    filename = "/home/pi/Desktop/Temperature_Humidity.log"
    if os.path.exists(filename):  # returns true if file exists
        # create a new window for displaying the file contents from the log
        window = tk.Tk()
        window.title("DHT11")
        window.geometry("380x250")
        window.configure(bg="white")
        window.configure(borderwidth=10, relief="sunken")
        window.resizable(width=False, height=False)

        disp = DispClass(master=window)
        disp.pack(fill="both", expand=True)

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
        # create a new window for displaying the error message
        window = tk.Tk()
        window.title("DHT11")
        window.geometry("400x250")
        window.configure(borderwidth=5, relief="sunken")
        window.resizable(width=False, height=False)

        disp = DispClass(master=window)
        disp.pack(fill="both", expand=True)

        disp.text_widget.insert("end", """Sensor log was not found!!\nIs the sensor running?\n"""
                                       """Restart this program when the sensor is operational""")
        disp.text_widget.configure(state="disabled")  # disabled editing

        window.mainloop()

if __name__ == '__main__':
    main()