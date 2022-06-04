from tkinter import *
from tkinter.ttk import Separator

book_antiqua=("Book Antiqua",12,"bold")
arial=('Arial', 12)

if "__main__"==__name__:
    root=Tk()
    root.title("Billing App")
    width = root.winfo_screenwidth() #get your Windows width size 
    height = root.winfo_screenheight() #get your Windows height size 
    root.geometry("%dx%d" % (width, height))
    root.resizable(False,False)
    root.state('zoomed')
    
    

    

def topbar():  
    
    ###############################################################################
    topbar = LabelFrame(root, bg="white",fg="white", padx=15, pady=15)
    topbar.grid(row=0, column=0)
    #Name
    customer_name_lbl=Label(topbar,text="Customer Name: ",font=book_antiqua)
    customer_name_lbl.grid(row=0,column=0)

    customer_name_tb=Entry(topbar,font=arial)
    customer_name_tb.grid(row=0,column=1)
    

    #Mobile
    customer_number_lbl=Label(topbar,text="Customer Number: ",font=book_antiqua)
    customer_number_lbl.grid(row=0,column=3)
    
    customer_number_tb=Entry(topbar,font=arial)
    customer_number_tb.grid(row=0,column=4)

    #Bill Number
    bill_number_lbl=Label(topbar,text="Bill Number: ",font=book_antiqua)
    bill_number_lbl.grid(row=0,column=6)
    
    bill_number_tb=Entry(topbar,font=arial)
    bill_number_tb.grid(row=0,column=7)

    ################################################################################
    midbar = LabelFrame(root, bg="white",fg="white", padx=30, pady=15)
    midbar.grid(row=1, column=0)
    

    for i in range(10):
        spacer = Label(root, text="            ")
        spacer.grid(row=1, column=i)

    #product ID
    product_id_lbl=Label(midbar,text="Product Id",font=book_antiqua)
    product_id_lbl.grid(row=0,column=0)

    product_id_tb=Entry(midbar,font=arial)
    product_id_tb.grid(row=1,column=0,padx=1)

    #product Name
    product_name_lbl=Label(midbar,text="Product Name",font=book_antiqua)
    product_name_lbl.grid(row=0,column=1)

    product_name_tb=Entry(midbar,font=arial)
    product_name_tb.grid(row=1,column=1)

    #Quantity
    quantity_lbl=Label(midbar,text="Quantity",font=book_antiqua)
    quantity_lbl.grid(row=0,column=2)

    quantity_tb=Entry(midbar,font=arial)
    quantity_tb.grid(row=1,column=2)

    #unit Rate
    unit_rate_lbl=Label(midbar,text="Unit Rate",font=book_antiqua)
    unit_rate_lbl.grid(row=0,column=3)

    unit_rate_tb=Entry(midbar,font=arial)
    unit_rate_tb.grid(row=1,column=3)


    #total amount
    total_amount_lbl=Label(midbar,text="Total Amount",font=book_antiqua)
    total_amount_lbl.grid(row=0,column=4)

    total_amount_tb=Entry(midbar,font=arial)
    total_amount_tb.grid(row=1,column=4)

    ##############################################################################

    


    
    


                
topbar()
root.mainloop()