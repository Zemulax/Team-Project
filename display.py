# Description: This program displays the contents of the log file in a GUI window
                               
import tkinter as tk #tkinter library
import os #operating system library
import fcntl #file locking library
import time #time library

#create a new window for displaying the file contents from the log
window = tk.Tk()
window.title("Sensor Log")
window.geometry("350x100")
window.configure(bg="purple")
window.configure(borderwidth=10, relief="groove")
window.resizable(width=False, height=False)

#display the file content here
text_widget = tk.Text(window)
text_widget.pack(fill="both", expand=True)
#read cotents from the log
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


