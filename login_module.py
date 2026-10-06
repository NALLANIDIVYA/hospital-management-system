from hospital.config import get_connection


def create_admin():
    print("\n========== CREATE ADMIN ==========")

    username = input("Enter username: ")
    password = input("Enter password: ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                admin_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)

        cursor.execute("""
            INSERT INTO admins (username, password)
            VALUES (%s, %s)
        """, (username, password))

        conn.commit()

        print("Admin created successfully!")

    except Exception as e:
        conn.rollback()
        print("Error creating admin:", e)

    finally:
        cursor.close()
        conn.close()


def login():

    print("\n========== ADMIN LOGIN ==========")

    username = input("Username: ")
    password = input("Password: ")

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT admin_id
            FROM admins
            WHERE username = %s
              AND password = %s
        """, (username, password))

        admin = cursor.fetchone()

        if admin:
            print("\nLogin successful!")
            return True

        print("\nInvalid username or password.")
        return False

    except Exception as e:

        print("Login error:", e)
        return False

    finally:
        cursor.close()
        conn.close()