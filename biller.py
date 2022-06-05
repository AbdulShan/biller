from tkinter import *
import sqlite3

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
    
    

    

def top_frame():  
    
    ###############################################################################
    top_frame = LabelFrame(root, bg="white",fg="white", padx=215, pady=15)
    top_frame.grid(row=0, column=0)
    
    #Mobile
    customer_number_lbl=Label(top_frame,text="Customer Number",font=book_antiqua)
    customer_number_lbl.grid(row=0,column=0)
    
    customer_number_tb=Entry(top_frame,font=arial)
    customer_number_tb.grid(row=1,column=0)

    #Name
    customer_name_lbl=Label(top_frame,text="Customer Name",font=book_antiqua)
    customer_name_lbl.grid(row=0,column=1)

    customer_name_tb=Entry(top_frame,font=arial)
    customer_name_tb.grid(row=1,column=1)

    #Bill Number
    bill_number_lbl=Label(top_frame,text="Bill Number",font=book_antiqua)
    bill_number_lbl.grid(row=0,column=2)
    
    bill_number_tb=Entry(top_frame,font=arial)
    bill_number_tb.grid(row=1,column=2)

    #Button Save
    save_btn=Button(top_frame,text="Enter",padx=10,pady=5,command=lambda:[create_data()])
    save_btn.grid(row=2,column=1)

    def create_data():
        try:    
            con=sqlite3.connect('Customer Data')
            cur=con.cursor()
            customer_number=customer_number_tb.get()
            cur.execute("create table if not exists '{}'(customer_number number(20) PRIMARY KEY NOT NULL,customer_name varchar(30),bill_number int(50))".format(customer_number))
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)

    ################################################################################
    mid_frame = LabelFrame(root, bg="white",fg="white", padx=30, pady=15)
    mid_frame.grid(row=1, column=0)
    

    '''for i in range(10):
        spacer = Label(root, text="            ")
        spacer.grid(row=1, column=i)'''

    #product ID
    product_id_lbl=Label(mid_frame,text="Product Id",font=book_antiqua)
    product_id_lbl.grid(row=0,column=0)

    product_id_tb=Entry(mid_frame,font=arial)
    product_id_tb.grid(row=1,column=0,padx=1)

    #product Name
    product_name_lbl=Label(mid_frame,text="Product Name",font=book_antiqua)
    product_name_lbl.grid(row=0,column=1)

    product_name_tb=Entry(mid_frame,font=arial)
    product_name_tb.grid(row=1,column=1)

    #Quantity
    quantity_lbl=Label(mid_frame,text="Quantity",font=book_antiqua)
    quantity_lbl.grid(row=0,column=2)

    quantity_tb=Entry(mid_frame,font=arial)
    quantity_tb.grid(row=1,column=2)

    #unit Rate
    unit_rate_lbl=Label(mid_frame,text="Unit Rate",font=book_antiqua)
    unit_rate_lbl.grid(row=0,column=3)

    unit_rate_tb=Entry(mid_frame,font=arial)
    unit_rate_tb.grid(row=1,column=3)


    #total amount
    total_amount_lbl=Label(mid_frame,text="Total Amount",font=book_antiqua)
    total_amount_lbl.grid(row=0,column=4)

    total_amount_tb=Entry(mid_frame,font=arial)
    total_amount_tb.grid(row=1,column=4)

    #Submit
    enter=Button(mid_frame,text="Enter",padx=10,pady=5)
    enter.grid(row=3,column=2)

    ##############################################################################
                
top_frame()
root.mainloop()