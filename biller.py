#All necessary Packages
from asyncio.windows_events import NULL
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
        f.write(dumps(counter))
counter = read_counter()
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
def main():
#Top frame Designs
###############################################################################
    #top frame code
    global top_frame
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
    global mid_frame
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
    unit_rate_tb=Entry(mid_frame,font=arial,state="disable")
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

#######################################################################################
#List Box
#List Box Frame
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
        print(product_name)
        product_name_tb.delete(0,END)
        product_name_tb.insert(0,product_name)
        
        for key, value in selected_items.items():
            if key=='values':
                product_price=value[2]
        unit_rate_tb.config(state="normal")
        unit_rate_tb.delete(0,END)
        unit_rate_tb.insert(0,product_price)
        unit_rate_tb.config(state="disable")
        
    
    tree_view_list.bind('<ButtonRelease>',selectItem)


    products={"rice":[2,400],"wheat":[5,90],"guitar":[10,5000],"dasawala":[69,420]}
    def Scankey(event):
        #val stores the selected value
        unit_rate_tb.config(state="normal")
        unit_rate_tb.delete(0,END)
        unit_rate_tb.config(state="disable")
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
    def Update(data):
        for item in tree_view_list.get_children():
            tree_view_list.delete(item)
        for key, value in data.items():
           print( key, value)
           tree_view_list.insert("",'end',text="L1",values=(key, value[0], value[1]))

    quantity={}
    for key,value in products.items():
        quantity[key]=value
    Update(quantity)
    product_name_tb.bind('<Key>', Scankey)


    

    '''#to print the selected item from listbox to product name textbox
    def getElement(event):
        selection = event.widget.curselection()
        index = selection[0]
        value = event.widget.get(index)
        print(value)
        product_name_tb.delete(0, END)
        product_name_tb.insert(0, value)

    #lists products and adds to listbox
    def Scankey(event):
        #val stores the selected value
        val = event.widget.get()
        if val==NULL:
            name_data = products
        else:
            name_data = []
            for key,value in products.items():
                if val.lower() in key.lower():
                    name_data.append(key)
                    Update(name_data)
                    print(name_data)
    #updates into listbox
    def Update(data):
        listbox.delete(0, 'end')
        for item in data:
            listbox.insert('end', item)
    
    def Scankey_quantity(event):
        #val stores the selected value
        val = event.widget.get()
        if val==NULL:
            num_data = products
        else:
            num_data = []
            for key,value in products.items():
                if val.lower() in key.lower():
                    num_data.append(value)
                    Update_quantity(num_data)
                    print(num_data)
    
    def Update_quantity(data):
        listbox2.delete(0, 'end')
        for item in data:
            listbox2.insert('end', item)
            
    #binds the product name textbox to the scankey function
    
    
    #ListBox left
    listbox = Listbox(list_box_frame,width=150)
    listbox.grid(row=0,column=0)
    listbox.bind('<<ListboxSelect>>', getElement)
    name=[]
    for key,value in products.items():
        name.append(key)
    print(name)
    Update(name)

    #list box right
    listbox2 = Listbox(list_box_frame,width=50)
    listbox2.grid(row=0,column=1)
    product_name_tb.bind('<Key>', Scankey_quantity)
    product_name_tb.bind('<Key>', Scankey)
    quantity=[]
    for key,value in products.items():
        quantity.append(value)
    print(quantity)
    Update_quantity(quantity)'''



#######################################################################################
#TreeView Section/ Output Section
    global tv_frame
    tv_frame = LabelFrame(root, bg="white",fg="white")
    tv_frame.grid(row=3, column=0,sticky="w")
    
    #treeview element
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
    def display():
        try:
            con=sqlite3.connect('Customer_Data.sql')
            cur=con.cursor()
            customer_number=customer_number_tb.get()

            #print all the inserted data into the tree view
            cur.execute("SELECT * from '{}'".format(customer_number))
            rec=cur.fetchall()
            for i in rec:
                tree_view.insert("", 'end', text ="L1",values =(i[3],i[0],i[5],i[6],i[7]))
            
            #print the total
            cur.execute("SELECT SUM(price) FROM '{}'".format(customer_number))
            rows=cur.fetchall()
            for i in rows:
                total_tb.delete(0, END)
                total_tb.insert(0,i[0])
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print("Error- ",err)
    
    #to clear the Tree view
    def clear_all():
        for item in tree_view.get_children():
            tree_view.delete(item)

###############################################################################################################
#Bottom Frame
    global frame_4
    frame_4 = LabelFrame(root, bg="white",fg="white")
    frame_4.grid(row=4, column=0,sticky="w")
    
    #Deletes Button
    delete_btn=Button(frame_4,text="Delete",command=lambda:[delete_item()])
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
            con=sqlite3.connect('Customer_Data.sql')
            cur=con.cursor()
            customer_number=customer_number_tb.get()
            cur.execute("DELETE FROM '{}' where sl_no={}".format(customer_number,k))
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print("Error- ",err)
        tree_view.delete(curItem)

    #Total
    total_lbl=Label(frame_4,text="Total",font=book_antiqua)
    total_lbl.grid(row=0,column=1)
    total_tb=Entry(frame_4)
    total_tb.grid(row=0,column=2)

#--------------------------------------------------------------------------------------------------------------------------------------------#
#Inventory Window Object
def add_to_inventory():
    #Top Frame Of second window !!!testing!!!
    global top_frame_inventory
    top_frame_inventory=LabelFrame(root)
    top_frame_inventory.grid(row=0,column=0)
    
    #product name
    product_name_lbl=Label(top_frame_inventory,text="Product Name",font=book_antiqua)
    product_name_lbl.grid(row=0,column=0)
    product_name_tb=Entry(top_frame_inventory,font=arial)
    product_name_tb.grid(row=1,column=0)

    #product Quantity
    product_quantity_lbl=Label(top_frame_inventory,text="Unit Rate",font=book_antiqua)
    product_quantity_lbl.grid(row=0,column=1)
    product_quantity_tb=Entry(top_frame_inventory,font=arial)
    product_quantity_tb.grid(row=1,column=1)

    def save_to_inventory():
        try:
            con=sqlite3.connect('Store_Inventory.sql')
            cur=con.cursor()
            product_name=product_name_tb.get()
            product_quantity=product_quantity_tb.get()
            cur.execute("CREATE table if not exists inventory(productname varchar, quantity int)")
            cur.execute("INSERT into inventory(productname,quantity)VALUES('{}',{})".format(product_name,product_quantity))
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print("Error- ",err)
    
    #submit
    submit_button=Button(top_frame_inventory,text="Submit",command=save_to_inventory)
    submit_button.grid(row=1,column=2)



#shows all the widget Bill window and Inventory window
def make_bill():
    top_frame.grid(row=0,column=0,sticky="w")
    mid_frame.grid(row=1,column=0,sticky="w")
    list_box_frame.grid(row=2,column=0,sticky="w")
    tv_frame.grid(row=3,column=0,sticky="w")
    frame_4.grid(row=4,column=0,sticky="w")
def make_inventory():
    top_frame_inventory.grid(row=0,column=0)

#hides all the widget Bill window and Inventory window
def clear_inventory_window():
    top_frame_inventory.grid_forget()
def clear_billing_window():
    top_frame.grid_forget()
    mid_frame.grid_forget()
    list_box_frame.grid_forget()
    tv_frame.grid_forget()
    frame_4.grid_forget()

##############################################################################################################
#menu Bar
menubar = Menu(root)

#menus in menubar
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menu", menu=file)
file.add_command(label="Add to Inventory",command=lambda:[clear_billing_window(),add_to_inventory()])
file.add_command(label="Make Bill",command=lambda:[clear_inventory_window(),make_bill()])
menubar.add_cascade(label="Exit", menu=exit)

exit=Menu(menubar,tearoff=0)
exit.add_command(label="exit")

#places menu to the window
root.config(menu=menubar)

#calling the main function
main()
#add_to_inventory()

#To run the tkinter window infinitely
root.mainloop()