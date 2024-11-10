import mysql.connector

# Establish a connection (replace with your actual MySQL credentials)
connection = mysql.connector.connect(
    host="localhost",  # Change if your MySQL server is remote
    user="root",  # Your MySQL username
    password="admin11",  # Your MySQL password
    database="pharmacy_management"  # Optional, or you can leave this out if not using a specific DB
)

# Check if the connection is successful
if connection.is_connected():
    print("Successfully connected to MySQL")

# Close the connection
connection.close()
