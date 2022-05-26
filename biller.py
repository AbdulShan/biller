#Tkinter Package 
from tkinter import *


#Tkinter Window Data
if __name__=="__main__":
    root=Tk()
    #To set Fixed window size
    width= root.winfo_screenwidth()
    height= root.winfo_screenheight()
    root.geometry("{}x{}".format(width, height))
    root.minsize(width, height)
    root.maxsize(width, height)
    #Title and bgcolor
    root.title("Billing App")
    root.configure(bg="#18181b")

#calling the package
root.mainloop()