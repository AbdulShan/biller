from tkinter import *


root=Tk()
#window=root.Tk()
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.geometry("{}x{}".format(width, height))

root.title("Billing App")
root.configure(bg="#18181b")

root.mainloop()