import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="your_database"
    )

def load_laptop_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM laptop")
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows)
