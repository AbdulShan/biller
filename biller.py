#All necessary Packages
import datetime
from tkinter import *
import sqlite3
from tkinter.ttk import Treeview
import atexit
from os import path
from json import dumps, loads

#font
book_antiqua=("Book Antiqua",12,"bold")
arial=('Arial', 12)

#date and time
date=datetime.date.today()
datesorted=date.strftime("%d-%m-%Y")

#Bill Number Counter
def read_counter():
    return loads(open("counter.json", "r").read()) + 1 if path.exists("counter.json") else 0
def write_counter():
    with open("counter.json", "w") as f:
        f.write(dumps(counter))
counter = read_counter()
atexit.register(write_counter)

#Tkinter window configs
if "__main__"==__name__:
    root=Tk()
    root.title("Billing App")
    width = root.winfo_screenwidth() #get your Windows width size 
    height = root.winfo_screenheight() #get your Windows height size 
    root.geometry("%dx%d" % (width, height))
    root.resizable(False,False)
    root.state('zoomed')


def main():
#Top frame Designs
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
    bill_number_tb.insert(0,counter)
    bill_number_tb.config(state='disabled')
    bill_number_tb.grid(row=1,column=2)

#Mid frame Designs
################################################################################
    mid_frame = LabelFrame(root, bg="white",fg="white")
    mid_frame.grid(row=1, column=0,sticky="w")
    
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
    enter=Button(mid_frame,text="Enter",padx=10,pady=5,command=lambda:[clear_all(),fetch_data(),display()])
    enter.grid(row=1,column=5)

    def fetch_data():
    #Creation and Insertion of the Data into the records
        #Takes the input from the textbox
        product_name=product_name_tb.get()
        customer_number=customer_number_tb.get()
        customer_name=customer_name_tb.get()
        bill_number=counter
        quantity_ins=quantity_tb.get()
        unit_rate_ins=unit_rate_tb.get()
        
        #Displays the total amount when clicked the #submit BUTTON
        total_amount_tb.delete(0,END)
        total_amount=float(quantity_ins)*float(unit_rate_ins)
        total_amount_tb.insert(0,total_amount)

        #To clear the textbox after clicking the button
        '''product_id_tb.delete('0', END)
        product_name_tb.delete('0', END)
        quantity_tb.delete('0', END)
        unit_rate_tb.delete('0', END)
        total_amount_tb.delete('0', END)'''

        #Creation & Insertion of the Database
        try:
            con=sqlite3.connect("Customer_Data.sql")
            cur=con.cursor()
            customer_number=customer_number_tb.get()
            cur.execute("create table if not exists '{}'(productname varchar PRIMARY KEY NOT NULL,date varchar(15),customer_name varchar(30),sl_no int,bill_num varchar(100),quantity int,unit_rate int,price int)".format(customer_number))
            cur.execute("SELECT * from '{}'".format(customer_number))
            count=(len(cur.fetchall())+1)
            cur.execute("INSERT into '{}'(productname,date,customer_name,sl_no,bill_num,quantity,unit_rate,price)VALUES('{}','{}','{}',{},{},{},{},{})".format(customer_number,product_name,datesorted,customer_name,count,bill_number,quantity_ins,unit_rate_ins,total_amount))
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)

    #TreeView Section/ Output Section
    ##############################################################################
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
    tree_view.heading("1",text="Sl.No")
    tree_view.heading("2",text="Product Name")
    tree_view.heading("3",text="Quantity")
    tree_view.heading("4",text="Unit Rate")
    tree_view.heading("5",text="Price")
    
    #To display the records in tree view and to add the records to the database
    def display():
        try:
            con=sqlite3.connect('Customer_Data.sql')
            cur=con.cursor()
            customer_number=customer_number_tb.get()
            cur.execute("SELECT * from '{}'".format(customer_number))
            rec=cur.fetchall()
            for i in rec:
                print("   ",i[3],"  |",i[0],"   |",i[5],"   ",i[6],"  |",i[7],"   |")
                tree_view.insert("", 'end', text ="L1",values =(i[3],i[0],i[5],i[6],i[7]))
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print("Error- ",err)
    
    #to clear the Tree view
    def clear_all():
        for item in tree_view.get_children():
            tree_view.delete(item)

main()
root.mainloop()