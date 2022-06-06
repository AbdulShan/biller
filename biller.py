import datetime
from tkinter import *
import sqlite3
from tkinter.ttk import Treeview

book_antiqua=("Book Antiqua",12,"bold")
arial=('Arial', 12)

date=datetime.date.today()
datesorted=date.strftime("%d-%m-%Y")
print(datesorted)


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
    top_frame = LabelFrame(root, bg="white",fg="white")
    top_frame.grid(row=0, column=0,sticky="w")
    
    #Mobile
    customer_number_lbl=Label(top_frame,text="Customer Number",font=book_antiqua)
    customer_number_lbl.grid(row=0,column=0,sticky="w")
    
    customer_number_tb=Entry(top_frame,font=arial)
    customer_number_tb.grid(row=1,column=0)
    customer_number_tb.insert(0,"_")
    customer_number_tb.focus_set()

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
    save_btn.grid(row=1,column=3,padx=(0, 368))

    def create_data():
        try:    
            con=sqlite3.connect('Customer_Data.sql')
            cur=con.cursor()
            customer_number=customer_number_tb.get()
            cur.execute("create table if not exists '{}'(bill_number int PRIMARY KEY NOT NULL,date varchar(15),customer_name varchar(30),sl_no int,product_name varchar(100),quantity int,unit_rate int,price int)".format(customer_number))
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)

    ################################################################################
    mid_frame = LabelFrame(root, bg="white",fg="white")
    mid_frame.grid(row=1, column=0,sticky="w")
    

    '''for i in range(10):
        spacer = Label(root, text="            ")
        spacer.grid(row=1, column=i)'''

    #product ID
    product_id_lbl=Label(mid_frame,text="Product Id",font=book_antiqua)
    product_id_lbl.grid(row=0,column=0)

    product_id_tb=Entry(mid_frame,font=arial)
    product_id_tb.grid(row=1,column=0)

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
    enter.grid(row=1,column=5)

    ##############################################################################
    #TreeView Section/ Output Section
    tv_frame = LabelFrame(root, bg="white",fg="white")
    tv_frame.grid(row=2, column=0,sticky="w")
    
    #treeview element
    tree_view= Treeview(tv_frame,selectmode='browse')
    tree_view.pack(side="left")

    #verticle scrollbar
    vertical_scrollbar=Scrollbar(tv_frame,orient="vertical",command=tree_view.yview)
    vertical_scrollbar.pack(side="right",fill='x')
    tree_view.configure(xscrollcommand=vertical_scrollbar.set)

    #Definning number of columns
    tree_view["columns"]=("1","2","3","4","5")
    #defining heading
    tree_view["show"]='headings'
    #modifying the size of the columns
    tree_view.column("1",width=60)
    tree_view.column("2",width=250)
    tree_view.column("3",width=90)
    tree_view.column("4",width=90)
    tree_view.column("5",width=150)
    #assigning heading name
    tree_view.heading("1",text="SL no.")
    tree_view.heading("2",text="Product Name")
    tree_view.heading("3",text="Quantity")
    tree_view.heading("4",text="Unit Rate")
    tree_view.heading("5",text="Price")




                
top_frame()
root.mainloop()