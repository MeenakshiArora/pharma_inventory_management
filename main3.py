from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog 
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk 
import random
import smtplib
import time

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System | Welcome")
        
        self.root.geometry("1800x1000+0+0")
        self.frame=Frame(self.root)
        self.frame.configure(bg="#d7f1c9")
        self.frame.pack()

        self.username = StringVar()
        self.password = StringVar()

        #________________________________________________________________________________
        
        self.lbltitle=Label(self.frame, text="Welcome!", font="stencil 15",fg="#21421e", bg="#d7f1c9")
        self.lbltitle.grid(row=0,column=1,columnspan=4,pady=20)
        self.lbltitle=Label(self.frame, text="Login to Pharmacy Management System", font="stencil 30",fg="#21421e", bg="#d7f1c9")
        self.lbltitle.grid(row=1,column=1,columnspan=4,pady=20)
        
        
        #_________________________________Frame Generation__________________________________
        
        self.loginframe1=Frame(self.frame, width=1010, height=500,bd=15,relief='ridge')
        self.loginframe1.grid(row=2,column=0,columnspan=5, pady=30)
        
        self.loginframe2=Frame(self.frame, width=1000, height=100,bd=15,relief='ridge')
        self.loginframe2.grid(row=3,column=0, columnspan=5, pady=30)
        #_________________________________________________________________________________
        self.lbl_username = Label(self.loginframe1, text="Username", font=('Arial', 14,'bold'), width=20,bg="#d7f1c9")
        self.lbl_username.grid(row=2, column=1,pady=5)
        self.entry_username= Entry(self.loginframe1, text="Username", textvariable=self.username,font=('Arial', 15,'bold') ,bd=5)
        self.entry_username.grid(row=2, column=2)

        self.lbl_password = Label(self.loginframe1, text="Password", font=('Arial', 14, 'bold'), width=20, bg="#d7f1c9")
        self.lbl_password.grid(row=4, column=1,pady=5)
        self.entry_password = Entry(self.loginframe1,text="Password",textvariable=self.password, font=('Arial', 15,'bold'), bd=5,show="*")
        self.entry_password.grid(row=4, column=2)
        #________________________________________________________________________________________
        self.btnlogin=Button(self.loginframe2, text="LOGIN", font="futura-bold 14", width=17, fg="White", bg="#87a96d", padx=4, pady=4, command=self.login)
        self.btnlogin.grid(row=0,column=0)
        self.btnreset=Button(self.loginframe2, text="RESET", font="futura-bold 14", width=17, fg="White", bg="#87a96d", padx=4, pady=4, command=self.reset)
        self.btnreset.grid(row=0,column=1)
        self.btnexit=Button(self.loginframe2, text="EXIT", font="futura-bold 14", fg="White",width=17, bg="#87a96d", padx=4, pady=4, command=self.exit_app)
        self.btnexit.grid(row=0,column=2)
        
        self.otp=None
        self.email=None
    
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
            self.username.set=("")
            self.password.set=("")
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    '''def login(self):
        self.email = "navmeen@gmail.com"  
        # Simulate a successful login
        if self.username.get() == "admin" and self.password.get() == "123":
            self.otp = self.send_otp(self.email)
            self.show_otp_popup()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def send_otp(self, email):
        # Generate a random 6-digit OTP
        otp = random.randint(100000, 999999)
        #smtp_server="smtp.gmail.com"
        #smtp_port=587
        #sender_email = "navmeen@gmail.com"
        #sender_password=""
        # Simulate sending the OTP via email (Here we'll print it)
        print(f"OTP sent to {email}: {otp}")
        # In a real application, you'd send the OTP via email using smtplib
        return otp

    def show_otp_popup(self):
        # Popup to ask for OTP
        self.otp_window = Toplevel(self.root)
        self.otp_window.title("Enter OTP")
        self.otp_window.geometry("300x200")
        self.otp_window.configure(bg="#d7f1c9")

        otp_label = Label(self.otp_window, text="Enter OTP sent to your email", font=('Arial', 12), bg="#d7f1c9")
        otp_label.pack(pady=10)

        self.otp_entry = Entry(self.otp_window, font=('Arial', 12))
        self.otp_entry.pack(pady=10)

        otp_button = Button(self.otp_window, text="Verify OTP", font=('Arial', 12), command=self.verify_otp)
        otp_button.pack(pady=10)

    def verify_otp(self):
        # Verify the OTP entered by the user
        entered_otp = self.otp_entry.get()
        if entered_otp == str(self.otp):
            messagebox.showinfo("OTP Verified", "OTP verified successfully. Welcome!")
            self.otp_window.destroy()  # Close OTP window
            self.root.destroy()  # Close login window
            # Open the main application window
            root_main = tk.Tk()
            PharmacyManagementSystem(root_main)
            root_main.mainloop()
        else:
            messagebox.showerror("Invalid OTP", "Incorrect OTP entered. Please try again.")
    '''
    def exit_app(self):
        """Exit the application when Exit button is clicked."""
        self.exit= messagebox.askyesno("Pharmacy Management System","Confirm if you want to exit")
        if self.exit:
            self.root.quit()
    
    def reset(self):
        self.username.set("")
        self.password.set("")

class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry('1400x850')
        self.root.config(bg="lightgrey")
        
        self.entries = []
        self.entries1 = []
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

        self.mainframe=Frame(self.root)
        self.mainframe.pack(fill="both", expand=True)
        #self.mainFrame.place(x=0, y=0, width=1200, height=700)
        #_______________________________Image Placement _________________________________
        #self.img = Image.open(r"D:\ph_logo.jpeg")  # Use raw string to handle backslashes
        #self.img = self.img.resize((10,10))  # Resize image to fit in the window
        #self.logo = ImageTk.PhotoImage(self.img)
        self.logo_label = Label(self.mainframe, text="LOGO", font=("arial",14),bg="lightblue")#image=self.logo#,bd=10,relief=RIDGE)
        self.logo_label.grid(row=0, column=0,padx=10,sticky='w') # Position the logo
        self.lbltitle = Label(self.mainframe, text="PHARMACY MANAGEMENT SYSTEM", bd=10, relief=RIDGE, bg='white', fg='darkgreen', font=('Times New Roman', 30, "bold"))
        self.lbltitle.grid(row=0, column=1,  padx=10)#pack(side=TOP, fill=X, padx=2, pady=2)
        
        self.DataFrame2 = LabelFrame(self.mainframe,text="Modules Available", fg="darkred", height=150, relief=RIDGE, padx=5, bd=10)
        self.DataFrame2.grid(row=1,column=0, columnspan=5,pady=5)
        self.DataFrame2.grid_rowconfigure(0, weight=1)
        self.DataFrame2.grid_rowconfigure(1, weight=1)
        self.DataFrame2.grid_columnconfigure(0, weight=1)
        self.DataFrame2.grid_columnconfigure(1, weight=1)
        self.DataFrame2.grid_columnconfigure(2, weight=1)
        self.DataFrame2.grid_columnconfigure(3, weight=1)
        self.DataFrame2.grid_columnconfigure(4, weight=1)
        self.DataFrame3 = LabelFrame(self.mainframe, text="Medicine Information", fg="darkred", width=1300, height=450,relief=RIDGE, padx=5, bd=10)
        self.DataFrame3.grid(row=2,column=0, columnspan=5, pady=5) 
        self.add_buttons()
    
    def clear_dataframe3(self):
        for widget in self.DataFrame3.winfo_children():
            widget.destroy()

    def add_buttons(self):
        
        Label(self.DataFrame2, text="Stock Management", bg="lightcoral", fg="#21421e",  font=("Arial", 13, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        Label(self.DataFrame2, text="Access Database", bg="lightcoral", fg="#21421e",  font=("Arial", 13, "bold")).grid(row=1, column=0, padx=5, pady=10, sticky="ew")

    # Add buttons in the first row
        button1 = Button(self.DataFrame2, text="ADD ITEM", bg="#d7f1c9", fg="green",  font=("Times-Bold 11"), command=self.additem)
        button1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        button2 = Button(self.DataFrame2, text="DELETE ITEM", bg="#d7f1c9", fg="green",  font=("Times-Bold 11"), command=self.deleteitem)
        button2.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        button3 = Button(self.DataFrame2, text="DISPLAY STOCK", bg="#d7f1c9", fg="green",  font=("Times-Bold 11"), command=self.displayall)
        button3.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Add buttons in the second row
        button4 = Button(self.DataFrame2, text="UPDATE ITEM", bg="#d7f1c9", fg="green",  font=("Times-Bold 11"), command=self.updateitem)
        button4.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        button5 = Button(self.DataFrame2, text="SEARCH ITEM", bg="#d7f1c9", fg="green",  font=("Times-Bold 11"), command=self.searchitem)
        button5.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        button6 = Button(self.DataFrame2, text="RESTOCKED ITEM", bg="#d7f1c9", fg="green",  font=("Times-Bold 11"), command=self.restockitem)
        button6.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # Sorted Data button
        button7 = Button(self.DataFrame2, text="SORTED DATA", bg="#d7f1c9", fg="green",  font=("Times-Bold 11"), command=self.restockitem)
        button7.grid(row=1, column=4, padx=5, pady=5, sticky="ew")

        # Log Out button
        button9 = Button(self.DataFrame2, text="LOG OUT", bg="#d7f1c9", fg="green",  font=("Times-Bold 11"), command=self.exit_app)
        button9.grid(row=1, column=5, padx=5, pady=5, sticky="ew")

        # Make the column expandable to fit the frame width
        '''self.DataFrame2.grid_columnconfigure(0, weight=1, minsize=200)
        self.DataFrame2.grid_columnconfigure(1, weight=1, minsize=200)
        self.DataFrame2.grid_columnconfigure(2, weight=1, minsize=200)
        self.DataFrame2.grid_columnconfigure(3, weight=1, minsize=200)
        self.DataFrame2.grid_columnconfigure(4, weight=1, minsize=200)
        self.DataFrame2.grid_columnconfigure(5, weight=1, minsize=200)'''
    def exit_app(self):
        """Exit the application when Exit button is clicked."""
        self.root.quit()
    
    def add_medicine_info_fields(self):
        #self.clear_DataFrame3()
        self.entries = []
        Label(self.DataFrame3, text= " STOCK ENTRY ", bg="lightcoral",fg="#21421e",width=20,font=("Arial",13,"bold")). grid(row=0,columnspan=7,padx=5,pady=5,sticky="ew")
        labels = ["MEDICINE CODE", "MEDICINE NAME", "QUANTITY", "MEDICINE MRP ", "MFG DATE(yyyy-mm-dd)", "EXPIRY DATE(yyyy-mm-dd)","PURPOSE"]
        for i, label_text in enumerate(labels,start=2):
            label = Label(self.DataFrame3, text=label_text, bg="darkgreen", fg="white", font=("Times", 12), width=25, relief="ridge")
            label.grid(row=i, column=0, sticky=W, padx=5, pady=10)
            entry = Entry(self.DataFrame3, font=("Times", 12), width=30)
            entry.grid(row=i, column=1, padx=5, pady=10)
            self.entries.append(entry)
        btn_submit = Button(self.DataFrame3, text="SUBMIT", bg="lightgreen", fg="darkgreen", font=("Times", 12, "bold"), command=self.additem)
        btn_submit.place(x=700, y=300)

    def additem(self):
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
        med_code = int(med_code)
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
        messagebox.showerror("Database Error", f"Error: {err}")


    def updateitem(self):
        med_code = simpledialog.askinteger("Update Item", "Enter the Med_Code of the medicine you want to update:")
        if med_code is None:  # User cancelled the input
            return
        self.cursor.execute("SELECT * FROM Medicines_info WHERE Med_Code = %s", (med_code,))
        item = self.cursor.fetchone()

        if item:
            # Ask the user for the field to update
            update_options = ["Med_Name", "Qty", "MRP", "MFG", "EXP", "Purpose"]
            self.selected_field = ttk.Combobox(self.DataFrame3, values=update_options, state="readonly")
            self.selected_field.set("Select field to update")  # Default value
            self.selected_field.grid(row=0, column=0, padx=5, pady=5)

            # Ask user to select which field to update
            def on_field_select(event):
                selected_field = self.selected_field.get()
                new_value = None

                if selected_field == "Med_Name":
                    new_value = simpledialog.askstring("Update Item", "Enter new medicine name:", initialvalue=item[1])
                elif selected_field == "Qty":
                    new_value = simpledialog.askinteger("Update Item", "Enter new quantity:", initialvalue=item[2])
                elif selected_field == "MRP":
                    new_value = simpledialog.askfloat("Update Item", "Enter new MRP:", initialvalue=item[3])
                elif selected_field == "MFG":
                    new_value = simpledialog.askstring("Update Item", "Enter new MFG date:", initialvalue=item[4])
                elif selected_field == "EXP":
                    new_value = simpledialog.askstring("Update Item", "Enter new EXP date:", initialvalue=item[5])
                elif selected_field == "Purpose":
                    new_value = simpledialog.askstring("Update Item", "Enter new purpose:", initialvalue=item[6])

                # Proceed with the update if the user has entered a valid value
                if new_value is not None:
                    confirm = messagebox.askyesno("Confirm Update", f"Are you sure you want to update {selected_field} to '{new_value}'?")
                    if confirm:
                        # Create a dictionary to map field names to their corresponding database column indices
                        field_map = {"Med_Name": 1, "Qty": 2, "MRP": 3, "MFG": 4, "EXP": 5, "Purpose": 6}
                        # Get the column index from the field_map
                        column_index = field_map[selected_field]
                        # Prepare the update statement based on the selected field
                        update_query = f'''
                            UPDATE Medicines_info
                            SET {selected_field} = %s
                            WHERE Med_Code = %s
                        '''
                        # Execute the update query
                        self.cursor.execute(update_query, (new_value, med_code))
                        # Commit the transaction
                        self.db_connection.commit()
                        messagebox.showinfo("Success", f"{selected_field} has been updated to '{new_value}' for Med_Code {med_code}.")
                    else:
                        messagebox.showinfo("Cancelled", f"Update for {selected_field} cancelled.")
                else:
                    messagebox.showinfo("No Change", "No change made to the field.")
            # Bind the event when the user selects a field from the dropdown
            self.selected_field.bind("<<ComboboxSelected>>", on_field_select)

        else:
            messagebox.showwarning("Not Found", f"No item found with Med_Code {med_code}.")


    def searchitem(self):
        self.clear_dataframe3()
        label1 = Label(self.DataFrame3, text="Enter the Med_Code or Med_Name to search:", 
                    bg="darkgreen", relief="ridge", fg="white", font=("Times", 12, "bold"), width=45)
        label1.place(x=100, y=100)

        search_entry = Entry(self.DataFrame3, font=("Times", 12))
        search_entry.place(x=100, y=200, width=450)

        def on_search_click():
            search_value = search_entry.get()

            if not search_value:
                messagebox.showerror("Input Error", "Please enter a Med_Code or Med_Name to search.")
                return
            self.cursor.execute("SELECT * FROM Medicines_info WHERE Med_Code = %s", (search_value,))
            item = self.cursor.fetchone()

            if not item:  # If no Med_Code found, search by Med_Name
                self.cursor.execute("SELECT * FROM Medicines_info WHERE Med_Name LIKE %s", ('%' + search_value + '%',))
                item = self.cursor.fetchone()

            if item:
                # Display search results
                result_text = f"Med_Code: {item[0]}\nMed_Name: {item[1]}\nQty: {item[2]}\nMRP: {item[3]}\nMFG: {item[4]}\nEXP: {item[5]}\nPurpose: {item[6]}"
                messagebox.showinfo("Search Result", result_text)
            else:
                messagebox.showwarning("Not Found", f"No item found with Med_Code or Med_Name containing '{search_value}'.")
        # Button to trigger search
        btn_search = Button(self.DataFrame3, text="Search", bg="lightgreen", fg="darkgreen", 
                            font=("Times", 12, "bold"), command=on_search_click)
        btn_search.place(x=100, y=300)


    def displayall(self):
        self.clear_dataframe3()
        self.cursor.execute("Select * from Medicines_info")
        items = self.cursor.fetchall()
        display_label = Label(self.DataFrame3, text=" AVAILABLE STOCK", font=("Times", 16, "bold"), bg="lightcoral", relief="ridge")
        display_label.grid(row=0, columnspan=7, padx=5, pady=5, sticky="ew")
        headers = ("Med_Code", "Med_Name", "Qty", "MRP", "MFG", "EXP", "Purpose")
        for col, header in enumerate(headers):
            label = Label(self.DataFrame3, text=header, font=("Times", 12, "bold"), bg="lightgreen", relief="ridge")
            label.grid(row=1, column=col, padx=5, pady=5)
        for row_id, item in enumerate(items, start=2):
            for col_id, value in enumerate(item):
                label = Label(self.DataFrame3, text=value, font=("Times", 12), bg="white", relief="ridge")
                label.grid(row=row_id, column=col_id, padx=5, pady=5)
        #pdf_button = Button(self.DataFrame3, text="Convert it into PDF", command=self.convert_to_pdf, font=("Arial", 15, "Bold"), width=30, bg="darkgreen", fg="white")
        #pdf_button.grid(row=row_id + 2, columnspan=7, padx=5, pady=10)
        #button9 = Button(self.DataFrame3,text="CONVERT TO PDF",bg="lightgrey",fg="green",width=20,font=("Times",12, "Bold"), command=self.convert_to_pdf)
        #button9.grid(row=row_id+1,column=5,padx=30) 
        button9 = Button(self.DataFrame3,text="CONVERT TO PDF",bg="lightgrey",fg="green",width=20,font=("Times-Bold 11"), command=self.convert_to_pdf).grid(row=7,column=5,padx=30)

    def convert_to_pdf(self):
        # Create the PDF file
        pdf_filename = "medicines_info.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter

        # Set up header for PDF
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 50, "Medicines Information")

        # Define table headers
        headers = ("Med_Code", "Med_Name", "Qty", "MRP", "MFG", "EXP", "Purpose")
        x_position = 100
        y_position = height - 70

        for header in headers:
            c.drawString(x_position, y_position, header)
            x_position += 90  # Space between columns

        y_position -= 20  # Move down for data rows

        # Extract the data from the labels (this is a basic approach)
        # Assuming the data is already available in `items`
        self.cursor.execute("SELECT * FROM Medicines_info")
        items = self.cursor.fetchall()

        for item in items:
            x_position = 100
            for value in item:
                c.drawString(x_position, y_position, str(value))
                x_position += 90
            y_position -= 20  # Move down for next row

        # Save the PDF
        c.save()

        # Show message
        print(f"PDF saved as {pdf_filename}")


    def restockitem(self):
        self.clear_dataframe3()
        self.cursor.execute("SELECT * FROM Medicines_info WHERE Qty < 10")
        items = self.cursor.fetchall()
        restock_label = Label(self.DataFrame3, text=" ITEMS TO RESTOCK", font=("Times", 16, "bold"), bg="lightcoral", relief="ridge")
        restock_label.grid(row=0, columnspan=7, padx=5, pady=5, sticky="ew")  # Span across all columns
        
        # Headers for the columns
        headers = ("Med_Code", "Med_Name", "Qty", "MRP", "MFG", "EXP", "Purpose")
        for col, header in enumerate(headers):
            header_label = Label(self.DataFrame3, text=header, font=("Times", 12, "bold"), bg="lightgreen", relief="ridge")
            header_label.grid(row=1, column=col, padx=5, pady=5)

        if not items:
            no_data_label = Label(self.DataFrame3, text="No items need restocking.", font=("Times", 12), bg="white", relief="ridge")
            no_data_label.grid(row=2, columnspan=7, padx=5, pady=5, sticky="ew")
            return

        for row_id, item in enumerate(items, start=2):  # Start from row 2 because row 0 is for "Required Restock" and row 1 is for headers
            for col_id, value in enumerate(item):
                value_label = Label(self.DataFrame3, text=value, font=("Times", 12), bg="white", relief="ridge")
                value_label.grid(row=row_id, column=col_id, padx=5, pady=5)
    
    def add_transaction_info(self):
        # Clear any previous entries if necessary
        self.entries1 = []
        Label(self.DataFrame3, text=" ADD TRANSACTION INFORMATION ", bg="lightcoral", fg="#21421e", width=20, font=("Arial", 13, "bold")).grid(row=0, columnspan=7, padx=5, pady=5, sticky="ew")
        labels = ["TRANSACTION_ID", "CLIENT NAME", "MED_NAME", "QUANTITY", "BILL"]
        for i, label_text in enumerate(labels, start=2):
            label = Label(self.DataFrame3, text=label_text, bg="darkgreen", fg="white", font=("Times", 12), width=25, relief="ridge")
            label.grid(row=i, column=0, sticky=W, padx=5, pady=10)
            entry = Entry(self.DataFrame3, font=("Times", 12), width=30)
            entry.grid(row=i, column=1, padx=5, pady=10)
            self.entries1.append(entry)
        btn_submit = Button(self.DataFrame3, text="SUBMIT", bg="lightgreen", fg="darkgreen", font=("Times", 12, "bold"), command=self.add_transaction)
        btn_submit.place(x=700, y=300)

    def add_transaction(self):
        self.add_transaction_info()
        # Fetch input data from the entries
        item_details = [entry.get() for entry in self.entries1]
        try:
            transaction_id = int(item_details[0])  # Ensures it's an integer
            Client_name = item_details[1].strip()
            Med_Name = item_details[2].strip()
            Qty = int(item_details[3])  # Ensure it's an integer
            Bill = float(item_details[4])  # Ensure it's a float
            formatted_details = (transaction_id, Client_name, Med_Name, Qty, Bill)
            
            # Execute the insert query
            self.cursor.execute('''INSERT INTO trans_info(transaction_id, Client_name, Med_Name, Qty, Bill)
                                    VALUES (%s, %s, %s, %s, %s)''', formatted_details)
            self.db_connection.commit()
            messagebox.showinfo("Success", "Transaction detail added to database.")
            # Clear the entry fields after successful submission
            for entry in self.entries1:
                entry.delete(0, END)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error while inserting into database: {err}")


if __name__ == "__main__":
    root_login = Tk()
    LoginWindow(root_login)
    root_login.mainloop()

def __del__(self):
        # Close the database connection when the program ends
        if self.db_connection.is_connected():
            self.cursor.close()
            self.db_connection.close()