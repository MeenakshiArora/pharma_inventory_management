from tkinter import *
from tkinter import messagebox, simpledialog 
import mysql.connector

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System | Welcome")
        #self.root.geometry("500x500+500+200")
        self.root.geometry("700x450")
        self.root.configure(bg="#d7f1c9")
        Label(self.root, text="Login to Pharmacy System", font="stencil 30", fg="#21421e", bg="#d7f1c9").place(x=50, y=10)

        self.username = StringVar()
        self.password = StringVar()

        lbl_username = Label(self.root, text="Username", font=('Arial', 12), bg="#d7f1c9").place(x=100,y=100)
        entry_username = Entry(self.root, textvariable=self.username, font=('Arial', 12)).place(x=100,y=150)
        lbl_password = Label(self.root, text="Password", font=('Arial', 12),bg="#d7f1c9").place(x=100,y=200)
        entry_password = Entry(self.root, textvariable=self.password, font=('Arial', 12), show="*").place(x=100,y=250)
        Button(self.root, text="Login", font="futura-bold 14", fg="White", bg="#87a96d", padx=4, pady=4, command=self.login).place(x=260, y=350)
    
    def login(self):
        # Sample credentials check
        if self.username.get() == "admin" and self.password.get() == "123":
            messagebox.showinfo("Login Success", "Welcome to the Pharmacy Management System")
            self.root.destroy()  # Close the login window
            # Open the main application window
            root_main = Tk()
            PharmacyManagementSystem(root_main)
            root_main.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")


class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry('1500x800+0+0')
        self.root.config(bg="lightgrey")
        self.entries = []
        self.db_connection = None

        self.connect_to_database()
        self.setup_main_window()

    def connect_to_database(self):
        # Database connection
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin11",  # Replace with your MySQL password
                database="pharmacy_management"
            )
            self.cursor = self.db_connection.cursor()
            print("Connected to the database")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to the database: {err}")

    def setup_main_window(self):
        lbltitle = Label(self.root, text="PHARMACY MANAGEMENT SYSTEM", bd=15, relief=RIDGE, bg='white', fg='darkgreen', font=('Times New Roman', 30, "bold"))
        lbltitle.pack(side=TOP, fill=X, padx=2, pady=2)

        DataFrame = Frame(self.root, bd=15, relief=RIDGE, padx=5)
        DataFrame.place(x=0, y=100, width=1400, height=850)

        self.DataFrame2 = LabelFrame(self.root, bd=10, relief=RIDGE, padx=5, text="Available Modules", fg="red", font=('Times New Roman', 15, "bold"))
        self.DataFrame2.place(x=5, y=100, width=1400, height=150)
        
        self.DataFrame3 = LabelFrame(self.root, bd=10, relief=RIDGE, padx=5, text="Medicine Information", fg="red", font=('Times New Roman', 15, "bold"))
        self.DataFrame3.place(x=5, y=260, width=1400, height=500)

        self.add_buttons()
        #self.add_medicine_info_fields()
        #btn_submit = Button(self.DataFrameRight, text="Submit", bg="lightgreen", fg="darkgreen", font=("Times", 12, "bold"), command=self.additem)
        #btn_submit.place(x=300, y=400)
    def clear_dataframe3(self):
        # Loop through all widgets in DataFrame3 and destroy them
        for widget in self.DataFrame3.winfo_children():
            widget.destroy()

    def add_buttons(self):
        button1=Button(self.DataFrame2,text="ADD ITEM",bg="lightgrey",fg="green",width=20,font=("Times-Bold 12"),command=self.additem)
        button1.place(x=30, y=50)
        button2 = Button(self.DataFrame2,text="DELETE ITEM",bg="lightgrey",fg="green",width=20,font=("Times-Bold 12"),command=self.deleteitem) 
        button2.place(x=250, y=50)
        button3 = Button(self.DataFrame2,text="UPDATE ITEM",bg="lightgrey",fg="green",width=20,font=("Times-Bold 12"), command=self.updateitem)  
        button3.place(x=450, y=50)
        button4 = Button(self.DataFrame2,text="SEARCH ITEM",bg="lightgrey",fg="green",width=20,font=("Times-Bold 12"), command=self.searchitem)  
        button4.place(x=650, y=50)
        button5 = Button(self.DataFrame2,text="DISPLAY STOCK",bg="lightgrey",fg="green",width=20,font=("Times-Bold 12"), command=self.nextitem)  
        button5.place(x=850, y=50)
        button6 = Button(self.DataFrame2,text="RESTOCKED ITEM",bg="lightgrey",fg="green",width=20,font=("Times-Bold 12"), command=self.previousitem)  
        button6.place(x=1050, y=50)

    def add_medicine_info_fields(self):
        labels = ["MEDICINE CODE", "MEDICINE NAME", "QUANTITY", "MEDICINE MRP ", "MFG DATE(yyyy-mm-dd)", "EXPIRY DATE(yyyy-mm-dd)","PURPOSE"]
        for i, label_text in enumerate(labels):
            label = Label(self.DataFrame3, text=label_text, bg="darkgreen", fg="white", font=("Times", 12), width=25, relief="ridge")
            label.grid(row=i, column=0, sticky=W, padx=5, pady=10)
            entry = Entry(self.DataFrame3, font=("Times", 12), width=30)
            entry.grid(row=i, column=1, padx=5, pady=10)
            self.entries.append(entry)
        btn_submit = Button(self.DataFrame3, text="Submit", bg="lightgreen", fg="darkgreen", font=("Times", 12, "bold"), command=self.additem)
        btn_submit.place(x=700, y=300)

    def additem(self):
        #self.clear_DataFrame3()
        self.add_medicine_info_fields()
        # Get item details from entries
        item_details = [entry.get() for entry in self.entries]
        
        try:
            Med_Code = int(item_details[0])
            Qty = int(item_details[2])
            MRP= float(item_details[3])
            MFG= item_details[4]
            EXP= item_details[5]
            Med_Name = item_details[1]
            Purpose = item_details[6]
            formatted_details = (Med_Code, Med_Name, Qty, MRP,MFG,EXP,Purpose)

            # Insert into database
            self.cursor.execute('''
                INSERT INTO Medicines_info(Med_Code, Med_Name, Qty,MRP,MFG,EXP,Purpose)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', formatted_details)
            
            # Commit transaction
            self.db_connection.commit()
            messagebox.showinfo("Success", "Item added to database.")
            
            # Clear entry fields
            for entry in self.entries:
                entry.delete(0, END)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def deleteitem(self):
        self.clear_dataframe3()
        label1 = Label(self.DataFrame3, text="Enter the Med_Code of the medicine you want to delete:", 
                    bg="darkgreen", relief="ridge", fg="white", font=("Times", 13, "bold"), width=45)
        label1.place(x=100, y=100)
        med_value = Entry(self.DataFrame3, font=("Times", 12))
        med_value.place(x=100, y=200, width=450)
        btn_submit = Button(self.DataFrame3, text="DELETE", bg="lightgrey", fg="darkgreen", 
                            font=("Times", 12, "bold"), command=lambda: self.on_delete_button_click(med_value))
        btn_submit.place(x=100, y=300)  # Adjust x and y based on your layout

    def on_delete_button_click(self, med_value):
        med_code = med_value.get()

        if not med_code:
            messagebox.showerror("Input Error", "Please enter a valid Med_Code.")
            return

        try:
            med_code = int(med_code)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric Med_Code.")
            return

        try:
            self.cursor.execute("SELECT * FROM Medicines_info WHERE Med_Code = %s", (med_code,))
            item = self.cursor.fetchone()

            if item:
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete item with Med_Code {med_code}?")
                if confirm:
                    self.cursor.execute("DELETE FROM Medicines_info WHERE Med_Code = %s", (med_code,))
                    self.db_connection.commit()
                    messagebox.showinfo("Success", f"Item with Med_Code {med_code} has been deleted.")
                else:
                    messagebox.showinfo("Cancelled", "Deletion cancelled.")
            else:
                messagebox.showwarning("Not Found", f"No item found with Med_Code {med_code}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


            
    
    def updateitem(self):
        try:
            # Ask the user for the Med_Code of the item to update
            med_code = simpledialog.askinteger("Update Item", "Enter the Med_Code of the medicine you want to update:")

            if med_code is None:  # User cancelled the input
                return

            # Check if the item exists in the database
            self.cursor.execute("SELECT * FROM Medicines_info WHERE Med_Code = %s", (med_code,))
            item = self.cursor.fetchone()

            if item:
                # Ask the user for new values for each field
                new_med_name = simpledialog.askstring("Update Item", "Enter new medicine name:", initialvalue=item[1])
                new_qty = simpledialog.askinteger("Update Item", "Enter new quantity:", initialvalue=item[2])
                new_mrp = simpledialog.askfloat("Update Item", "Enter new MRP:", initialvalue=item[3])
                new_mfg = simpledialog.askstring("Update Item", "Enter new MFG date:", initialvalue=item[4])
                new_exp = simpledialog.askstring("Update Item", "Enter new EXP date:", initialvalue=item[5])
                new_purpose = simpledialog.askstring("Update Item", "Enter new purpose:", initialvalue=item[6])

                # Confirm update
                confirm = messagebox.askyesno("Confirm Update", f"Are you sure you want to update item with Med_Code {med_code}?")
                if confirm:
                    # Execute update statement
                    self.cursor.execute('''
                        UPDATE Medicines_info
                        SET Med_Name = %s, Qty = %s, MRP = %s, MFG = %s, EXP = %s, Purpose = %s
                        WHERE Med_Code = %s
                    ''', (new_med_name, new_qty, new_mrp, new_mfg, new_exp, new_purpose, med_code))
                    
                    # Commit the transaction
                    self.db_connection.commit()
                    messagebox.showinfo("Success", f"Item with Med_Code {med_code} has been updated.")
                else:
                    messagebox.showinfo("Cancelled", "Update cancelled.")
            else:
                messagebox.showwarning("Not Found", f"No item found with Med_Code {med_code}.")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid values.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def searchitem(self):
        pass

    
if __name__ == "__main__":
    root_login = Tk()
    LoginWindow(root_login)
    root_login.mainloop()

def __del__(self):
        # Close the database connection when the program ends
        if self.db_connection.is_connected():
            self.cursor.close()
            self.db_connection.close()