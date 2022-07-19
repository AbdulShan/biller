#All necessary Packages
from ast import Break
from asyncio.windows_events import NULL
import datetime
from tkinter import *
import sqlite3
from tkinter.ttk import Treeview
import atexit
from os import path
from turtle import left
import fpdf
from json import dumps, loads

#font
book_antiqua=("Book Antiqua",12,"bold")
arial=('Arial', 12)

#date and time, sorting date into dd/mm/yyyy
date=datetime.date.today()
datesorted=date.strftime("%d-%m-%Y")

#Bill Number Counter
def read_counter():
    #reads the Bill number from the counter.json file
    return loads(open("counter.json", "r").read()) + 1 if path.exists("counter.json") else 0
def write_counter():
    #writes/saves the Bill Number in counter.json file
    with open("counter.json", "w") as f:
        f.write(dumps(bill_number))
bill_number = read_counter()
atexit.register(write_counter)

#Tkinter window configs
if "__main__"==__name__:
    root=Tk()
    root.title("Billing App")
    #get your Windows width/height, set size to full window
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    #wont allow to resize window, and full screen when opening
    root.resizable(False,False)
    root.state('zoomed')

#Billing Window Object
#Top frame Designs
###############################################################################
    #top frame code
def frame_1():
    global top_frame
    top_frame = LabelFrame(root, bg="white",fg="white")
    top_frame.grid(row=0, column=0,sticky="w")

    #Mobile
    customer_number_lbl=Label(top_frame,text="Customer Number",font=book_antiqua)
    customer_number_lbl.grid(row=0,column=0,sticky="w")
    global customer_number_tb
    customer_number_tb=Entry(top_frame,font=arial)
    customer_number_tb.grid(row=1,column=0)
    customer_number_tb.focus_set()

    #Name
    customer_name_lbl=Label(top_frame,text="Customer Name",font=book_antiqua)
    customer_name_lbl.grid(row=0,column=1)
    global customer_name_tb
    customer_name_tb=Entry(top_frame,font=arial)
    customer_name_tb.grid(row=1,column=1)

    #Bill Number
    bill_number_lbl=Label(top_frame,text="Bill Number",font=book_antiqua)
    bill_number_lbl.grid(row=0,column=2)
    bill_number_tb=Entry(top_frame,font=arial)
    bill_number_tb.insert(0,bill_number)
    bill_number_tb.config(state='disabled')
    bill_number_tb.grid(row=1,column=2)

#Mid frame Designs
################################################################################
def frame_2():
    global mid_frame
    mid_frame = LabelFrame(root, bg="white",fg="white")
    mid_frame.grid(row=1, column=0,sticky="w")
    
    '''#product ID
    product_id_lbl=Label(mid_frame,text="Product Id",font=book_antiqua)
    product_id_lbl.grid(row=0,column=0)
    product_id_tb=Entry(mid_frame,font=arial)
    product_id_tb.grid(row=1,column=0)'''

    #product Name
    product_name_lbl=Label(mid_frame,text="Product Name",font=book_antiqua)
    product_name_lbl.grid(row=0,column=1)
    global product_name_tb
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
    global unit_rate_tb
    unit_rate_tb=Entry(mid_frame,font=arial)#,state="disable")
    unit_rate_tb.grid(row=1,column=3)

    #total amount
    total_amount_lbl=Label(mid_frame,text="Total Amount",font=book_antiqua)
    total_amount_lbl.grid(row=0,column=4)
    total_amount_tb=Entry(mid_frame,font=arial)
    total_amount_tb.grid(row=1,column=4)

    #Submit
    enter=Button(mid_frame,text="Enter",padx=10,pady=5,command=lambda:[fetch_data(),clear_all(),display()])
    enter.grid(row=1,column=5)

    def fetch_data():
    #Creation and Insertion of the Data into the records
        #Takes the input from the textbox
        global product_name,customer_name,customer_number,quantity_ins,unit_rate_ins,total_amount
        product_name=product_name_tb.get()
        customer_number=customer_number_tb.get()
        customer_name=customer_name_tb.get()
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
            con=sqlite3.connect("Store_Data.sql")
            cur=con.cursor()
            customer_number=customer_number_tb.get()
            cur.execute("create table if not exists customer_data(bill_num int ,date varchar(15),customer_number int,customer_name varchar(30),sl_no int,productname varchar,quantity int,unit_rate int,price int)")
            cur.execute("SELECT * from customer_data".format(customer_number))
            global count
            count=(len(cur.fetchall())+1)
            cur.execute("INSERT into customer_data(bill_num,date,customer_number,customer_name,sl_no,productname,quantity,unit_rate,price)VALUES({},'{}',{},'{}',{},'{}',{},{},{})".format(bill_number,datesorted,customer_number,customer_name,count,product_name,quantity_ins,unit_rate_ins,total_amount))
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)

#######################################################################################
#List Box
#List Box Frame
def frame_3():
    global list_box_frame
    list_box_frame=LabelFrame(root,bg="white",fg="white")
    list_box_frame.grid(row=2,column=0,sticky="w")

    tree_view_list= Treeview(list_box_frame,selectmode='browse')
    tree_view_list.grid(row=0,column=0)

    vertical_scrollbar=Scrollbar(list_box_frame,orient="vertical",command=tree_view_list.yview)
    vertical_scrollbar.grid(row=0,column=4)
    tree_view_list.configure(xscrollcommand=vertical_scrollbar.set)

    tree_view_list["columns"]=("1","2")
    tree_view_list["show"]='headings'

    tree_view_list.column("1",width=250)
    tree_view_list.column("2",width=100)

    tree_view_list.heading("1",text="Product Name")
    tree_view_list.heading("2",text="Quantity Left")

    def selectItem(event):
        curItem0 = tree_view_list.focus()
        tree_view_list.item(curItem0)
        selected_items =tree_view_list.item(curItem0)
        for key, value in selected_items.items():
            if key=='values':
                product_name=value[0]
        product_name_tb.delete(0,END)
        product_name_tb.insert(0,product_name)
        
        for key, value in selected_items.items():
            if key=='values':
                product_price=value[2]
        #unit_rate_tb.config(state="normal")
        unit_rate_tb.delete(0,END)
        unit_rate_tb.insert(0,product_price)
        #unit_rate_tb.config(state="disable")
        
    
    tree_view_list.bind('<ButtonRelease>',selectItem)

    global products
    products={}
    def Scankey(event):
        #val stores the selected value
        #unit_rate_tb.config(state="normal")
        unit_rate_tb.delete(0,END)
        #unit_rate_tb.config(state="disable")
        val = event.widget.get()
        if val==NULL:
            name_data = products
        else:
            name_data = {}
            for key,value in products.items():
                if val.lower() in key.lower():
                    name_data[key]=value
                    Update(name_data)
    
    #updates into listbox
    global Update
    def Update(data):
        for item in tree_view_list.get_children():
            tree_view_list.delete(item)
        for key, value in data.items():
           tree_view_list.insert("",'end',text="L1",values=(key, value[1]))

    product_name_tb.bind('<Key>', Scankey)


#######################################################################################
#TreeView Section/ Output Section
def frame_4():
    global tv_frame
    tv_frame = LabelFrame(root, bg="white",fg="white")
    tv_frame.grid(row=3, column=0,sticky="w")
    
    #treeview element
    global tree_view
    tree_view= Treeview(tv_frame,selectmode='browse')
    tree_view.grid(row=0,column=0)

    #verticle scrollbar
    vertical_scrollbar=Scrollbar(tv_frame,orient="vertical",command=tree_view.yview)
    vertical_scrollbar.grid(row=0,column=4)
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
    global display
    def display():
        try:
            con=sqlite3.connect('Store_Data.sql')
            cur=con.cursor()
            customer_number=customer_number_tb.get()
            cur.execute("CREATE TABLE IF NOT EXISTS final_bill(bill_num1 int,productname1 varchar,quantity1 int,unit_rate1 int,price1 int)")
            cur.execute("INSERT INTO final_bill(bill_num1,productname1,quantity1,unit_rate1,price1)VALUES({},'{}',{},{},{})".format(bill_number,product_name,quantity_ins,unit_rate_ins,total_amount))
            #print all the inserted data into the tree view
            cur.execute("SELECT rowid,productname1,quantity1,unit_rate1,price1 FROM final_bill where bill_num1={}".format(bill_number))
            rec=cur.fetchall()
            for i in rec:
                tree_view.insert("", 'end', text ="L1",values =(i[0],i[1],i[2],i[3],i[4]))
            #cur.execute("SELECT sl_no,productname,quantity,unit_rate,price FROM customer_data ORDER BY sl_no ASC")


            #print the total
            cur.execute("SELECT SUM(price1) FROM final_bill")
            rows=cur.fetchall()
            for i in rows:
                total_tb.delete(0, END)
                total_tb.insert(0,i[0])
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print("Error- ",err)
    
    #to clear the Tree view
    global clear_all
    def clear_all():
        for item in tree_view.get_children():
            tree_view.delete(item)

###############################################################################################################
#Bottom Frame
def frame_5():
    global del_total_frame
    del_total_frame = LabelFrame(root, bg="white",fg="white")
    del_total_frame.grid(row=4, column=0,sticky="w")
    
    #Deletes Button
    delete_btn=Button(del_total_frame,text="Delete",command=lambda:[delete_item()])
    delete_btn.grid(row=0,column=0)

    #delete the selected item from tree_view
    def delete_item():
        curItem = tree_view.focus()
        tree_view.item(curItem)
        selected_items =tree_view.item(curItem)
        for key, value in selected_items.items():
            if key == 'values':
                k=value[0]

        #deletes the selected item from database
        try:
            con=sqlite3.connect('Store_Data.sql')
            cur=con.cursor()
            customer_number=customer_number_tb.get()
            cur.execute("DELETE FROM customer_data where sl_no={}".format(k))
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print("Error- ",err)
        tree_view.delete(curItem)
    
    def drop_table():
        try:
            con=sqlite3.connect('Store_Data.sql')
            cur=con.cursor()
            cur.execute("DROP TABLE final_bill")
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print("Error- ",err)


    #Total
    total_lbl=Label(del_total_frame,text="Total",font=book_antiqua)
    total_lbl.grid(row=0,column=1)
    global total_tb
    total_tb=Entry(del_total_frame)
    total_tb.grid(row=0,column=2)

    #Print Bill
    printbill_btn=Button(del_total_frame,text="Print Bill",command=lambda:[pdf_output(),drop_table(),clear_all()])
    printbill_btn.grid(row=0,column=3)

#--------------------------------------------------------------------------------------------------------------------------------------------#
#Inventory Window Object
def window_2_frame_1():
##########################################################################################################################
    #Top Frame Of second window
    global top_frame_inventory
    top_frame_inventory=LabelFrame(root,text="Add Product to inventory",font=("book_antiqua",9,'bold'))
    
    #product name
    product_name_lbl=Label(top_frame_inventory,text="Product Name",font=book_antiqua)
    product_name_lbl.grid(row=0,column=0)
    product_name_tb=Entry(top_frame_inventory,font=arial)
    product_name_tb.grid(row=1,column=0)

    #product Quantity
    product_quantity_lbl=Label(top_frame_inventory,text="Quantity",font=book_antiqua)
    product_quantity_lbl.grid(row=0,column=1)
    global product_quantity_tb
    product_quantity_tb=Entry(top_frame_inventory,font=arial)
    product_quantity_tb.grid(row=1,column=1)

    #product Price
    product_price_lbl=Label(top_frame_inventory,text="Unit Rate",font=book_antiqua)
    product_price_lbl.grid(row=0,column=2)
    product_price_tb=Entry(top_frame_inventory,font=arial)
    product_price_tb.grid(row=1,column=2)

    def save_to_inventory():
        try:
            con=sqlite3.connect('Store_Data.sql')
            cur=con.cursor()
            global product_name_window2,product_quantity
            product_name_window2=product_name_tb.get()
            product_quantity=product_quantity_tb.get()
            product_price=product_price_tb.get()
            #Creates a table if not exists
            cur.execute("CREATE table if not exists inventory(productname varchar,quantity int,price int)")
            
            #returns a binary value 0 or 1 if the entered record is existing or not:"1 if existing, 0 if not exist"
            cur.execute("SELECT COUNT(*) FROM inventory WHERE productname='{}'".format(product_name_window2))
            boolean_if_in_database_inventory1=cur.fetchall()

            #inserts the data into inventory database
            cur.execute("INSERT into inventory(productname,quantity,price)VALUES('{}',{},{})".format(product_name_window2,product_quantity,product_price))
            
            #Deletes the data if already existing
            cur.execute("DELETE FROM inventory WHERE rowid NOT IN (SELECT min(rowid) FROM inventory GROUP BY productname)")

            #Updates the quantity if the data entered is existing
            cur.execute("SELECT quantity from inventory where productname='{}'".format(product_name_window2))
            existing_quantity=cur.fetchall()
            if boolean_if_in_database_inventory1[0][0]==1:
                cur.execute("UPDATE inventory SET quantity={} where productname='{}'".format(existing_quantity[0][0]+int(product_quantity),product_name_window2))
            
            con.commit()
        except sqlite3.Error as err:
            print("Error- ",err)
    
    #submit
    submit_button=Button(top_frame_inventory,text="Submit",command=lambda:[clear_all2(),save_to_inventory(),display2()])
    submit_button.grid(row=1,column=3)

############################################################################################
#TreeView frame to display the inventory Database
def window_2_frame_2():
    global tv_frame_inventory
    tv_frame_inventory = LabelFrame(root, bg="white",fg="white")

    global tree_view_inventory
    tree_view_inventory= Treeview(tv_frame_inventory,selectmode='browse')
    tree_view_inventory.grid(row=0,column=0)

    vertical_scrollbar=Scrollbar(tv_frame_inventory,orient="vertical",command=tree_view_inventory.yview)
    vertical_scrollbar.grid(row=0,column=4)
    tree_view_inventory.configure(xscrollcommand=vertical_scrollbar.set)

    tree_view_inventory["columns"]=("1","2")

    tree_view_inventory["show"]='headings'

    tree_view_inventory.column("1",width=250)
    tree_view_inventory.column("2",width=100)

    tree_view_inventory.heading("1",text="Product Name")
    tree_view_inventory.heading("2",text="Quantity Left")

####################################################################################
#Deletion frame
def window_2_frame_3():
    global edit_frame_inventory
    edit_frame_inventory = LabelFrame(root, bg="white",fg="white")

    delete_btn=Button(edit_frame_inventory,text="Delete",command=lambda:[delete_item1()])
    delete_btn.grid(row=0,column=0)

    def delete_item1():
        curItem = tree_view_inventory.focus()
        tree_view_inventory.item(curItem)
        selected_items =tree_view_inventory.item(curItem)
        for key, value in selected_items.items():
            if key == 'values':
                name=value[0]
        
        try:
            con=sqlite3.connect('Store_Data.sql')
            cur=con.cursor()
            cur.execute("DELETE FROM inventory where productname='{}'".format(name))
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print("Error- ",err)

        tree_view_inventory.delete(curItem)
#----------------------------------------------------------------------------------------------------- work in progress
def display2():
    try:
        con=sqlite3.connect('Store_Data.sql')
        cur=con.cursor()
        cur.execute("SELECT * from inventory")
        rec=cur.fetchall()
        for i in rec:
            products[i[0]]=[i[2],i[1]]
            tree_view_inventory.insert("", 'end', text ="L1",values =(i[0],i[1]))
        con.commit()
        con.close()
    except sqlite3.Error as err:
        print("Error- ",err)
    

    quantity={}
    for key,value in products.items():
        quantity[key]=value
        Update(quantity)


def clear_all2():
    for item in tree_view_inventory.get_children():
        tree_view_inventory.delete(item)

###########################################################################################
#shows all the widget Bill window and Inventory window
def make_bill():
    top_frame.grid(row=0,column=0,sticky="w")
    mid_frame.grid(row=1,column=0,sticky="w")
    list_box_frame.grid(row=2,column=0,sticky="w")
    tv_frame.grid(row=3,column=0,sticky="w")
    del_total_frame.grid(row=4,column=0,sticky="w")
def make_inventory():
    top_frame_inventory.grid(row=0,column=0,sticky="w")
    tv_frame_inventory.grid(row=1, column=0,sticky="w")
    edit_frame_inventory.grid(row=2, column=0,sticky="w")

#hides all the widget Bill window and Inventory window
def clear_window1():
    top_frame.grid_forget()
    mid_frame.grid_forget()
    list_box_frame.grid_forget()
    tv_frame.grid_forget()
    del_total_frame.grid_forget()

def clear_window2():
    top_frame_inventory.grid_forget()
    tv_frame_inventory.grid_forget()
    edit_frame_inventory.grid_forget()

##############################################################################################################
def window1():
    frame_1()
    frame_2()
    frame_3()
    frame_4()
    frame_5()

def window2():
    window_2_frame_1()
    window_2_frame_2()
    window_2_frame_3()

##############################################################################################################
#menu Bar
#Bug Fixer
def disable_menu_condition():
    flag=True
    if flag==True:
        file.entryconfig(1,state='disable')
        file.entryconfig(0,state='normal')
        flag=False

def enable_menu_condition():
    flag=True
    if flag==True:
        file.entryconfig(1,state='normal')
        file.entryconfig(0,state='disable')
        flag=False
#Bug Fixer^^^^^ for menubar

menubar = Menu(root)

#menus in menubar
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menu", menu=file)
file.add_command(label="Add to Inventory",command=lambda:[clear_window1(),clear_all2(),display2(),make_inventory(),enable_menu_condition()])
file.add_command(label="Make Bill",command=lambda:[clear_window2(),frame_3(),display2(),make_bill(),disable_menu_condition()])
menubar.add_cascade(label="Exit", menu=exit)

exit=Menu(menubar,tearoff=0)
exit.add_command(label="exit")

#places menu to the window
root.config(menu=menubar)

###################################################################################
#PDF
#pdf output generator
def pdf_output():
    pdf= fpdf.FPDF()
    pdf.add_page()

    def pdf_arial():
        pdf.set_font("Arial", size = 12)

    def pdf_arial_bold():
        pdf.set_font("Arial",style="B", size = 12)

    #invoice
    pdf.set_font("Times",style="BU", size = 55)
    pdf.cell(93, 28, txt = "INVOICE",ln = 2, align = 'L', border=0)
    


    #celspacer
    def cellspacer():
        pdf.cell(30, 7,ln = 0, align = 'L', border=0)

    def cellspacer_bottom():
        pdf.cell(30, 5,ln = 1, align = 'L', border=0)


    #row1
    pdf.set_font("Arial",style="B", size = 12)
    pdf.cell(30, 5, txt = "Bill Number",ln = 0, align = 'L', border=0)
    cellspacer()
    pdf.cell(30, 5, txt = "Date of Issue",ln = 1, align = 'L', border=0)

    #row2
    pdf_arial()
    pdf.cell(30, 7, txt = "{}".format(bill_number),ln = 0, align = 'L', border=0)
    cellspacer()
    pdf.cell(30, 7, txt = "{}".format(datesorted),ln = 1, align = 'L', border=0)

    #row3
    cellspacer_bottom()

    #row4
    pdf_arial_bold()
    pdf.cell(30, 5, txt = "Billed To",ln = 0, align = 'L', border=0)
    cellspacer()
    pdf.cell(30, 5, txt = "The-Mart",ln = 1, align = 'L', border=0)

    #row5
    pdf_arial()
    pdf.cell(30, 7, txt = "{}".format(customer_name),ln = 0, align = 'L', border=0)
    cellspacer()
    pdf.cell(30, 7, txt = "{}".format("5th Street"),ln = 1, align = 'L', border=0)
    cellspacer()
    cellspacer()
    pdf.cell(30, 7, txt = "{}".format("#company mail"),ln = 1, align = 'L', border=0)
    cellspacer()
    cellspacer()
    pdf.cell(30, 7, txt = "{}".format("#contact number"),ln = 1, align = 'L', border=0)
    cellspacer_bottom()
    cellspacer_bottom()
    pdf_arial_bold()
    pdf.cell(10, 7, txt = "{}".format("no."),ln = 0, align = 'L', border=0)
    pdf.cell(30, 7, txt = "{}".format("Description"),ln = 0, align = 'L', border=0)
    cellspacer()
    cellspacer()
    pdf.cell(30, 7, txt = "{}".format("Units/Kg"),ln = 0, align = 'L', border=0)
    pdf.cell(30, 7, txt = "{}".format("Unit Cost"),ln = 0, align = 'L', border=0)
    pdf.cell(30, 7, txt = "{}".format("Amount"),ln = 1, align = 'L', border=0)
    pdf.line(11, 99, 187, 99)

    cellspacer_bottom()
    try:
            con=sqlite3.connect('Store_Data.sql')
            cur=con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS final_bill(bill_num1 int,productname1 varchar,quantity1 int,unit_rate1 int,price1 int)")
            cur.execute("SELECT rowid,productname1,quantity1,unit_rate1,price1 FROM final_bill where bill_num1={}".format(bill_number))
            rec=cur.fetchall()
            for i in rec:
                number_of_items=len(rec)
                pdf_arial()
                pdf.cell(10, 7, txt = "{}".format(i[0]),ln = 0, align = 'L', border=0)
                pdf.cell(30, 7, txt = "{}".format(i[1]),ln = 0, align = 'L', border=0)
                cellspacer()
                cellspacer()
                pdf.cell(30, 7, txt = "{}".format(i[2]),ln = 0, align = 'L', border=0)
                pdf.cell(30, 7, txt = "{}".format(i[3]),ln = 0, align = 'L', border=0)
                pdf.cell(30, 7, txt = "{}".format(i[4]),ln = 1, align = 'L', border=0)
            cur.execute("SELECT SUM(price1) FROM final_bill")
            total_pdf=cur.fetchall()
            total_pdf1=total_pdf[0]
            
    except sqlite3.Error as err:
        print("Error: ",err)


    
    pdf.cell(30, 7, txt = "{}".format("-----------------------------------------------------------------------------------------------------------------------------"),ln = 1, align = 'L', border=0)
    pdf.cell(10, 7,ln = 0, align = 'L', border=0)
    cellspacer()
    cellspacer()
    cellspacer()
    cellspacer()
    pdf_arial_bold()
    pdf.cell(30, 7, txt = "{}".format("Total"),ln = 0, align = 'L', border=0)
    pdf_arial()
    pdf.cell(30, 7, txt = "{}".format(total_pdf1[0]),ln = 1, align = 'L', border=0)
    pdf.output("testings.pdf")


#calling the main function

window1()
window2()
display2()
disable_menu_condition()
#pdf_output()
#To run the tkinter window
root.mainloop()