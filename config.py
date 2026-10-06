import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "divya123",
    "database": "hospital_db"
}


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

    except mysql.connector.Error as e:
        print("Database connection error:", e)

    return None