from hospital.config import get_connection


def create_database_tables():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                dept_id INT AUTO_INCREMENT PRIMARY KEY,
                dept_name VARCHAR(100) UNIQUE NOT NULL,
                description VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INT AUTO_INCREMENT PRIMARY KEY,
                patient_name VARCHAR(100) NOT NULL,
                gender VARCHAR(20),
                dob DATE,
                phone VARCHAR(10),
                address VARCHAR(255),
                blood_group VARCHAR(10),
                status VARCHAR(20) DEFAULT 'ACTIVE'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                doctor_name VARCHAR(100) NOT NULL,
                dept_id INT,
                phone VARCHAR(10),
                consultation_fee DECIMAL(10,2),
                available_slots VARCHAR(255),
                status VARCHAR(20) DEFAULT 'ACTIVE',

                FOREIGN KEY (dept_id)
                REFERENCES departments(dept_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT NOT NULL,
                doctor_id INT NOT NULL,
                appointment_date DATE NOT NULL,
                time_slot VARCHAR(50) NOT NULL,
                status VARCHAR(20) DEFAULT 'BOOKED',
                notes VARCHAR(255),

                FOREIGN KEY (patient_id)
                REFERENCES patients(patient_id),

                FOREIGN KEY (doctor_id)
                REFERENCES doctors(doctor_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                bill_id INT AUTO_INCREMENT PRIMARY KEY,
                appointment_id INT UNIQUE NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                payment_status VARCHAR(20) DEFAULT 'PENDING',
                billed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (appointment_id)
                REFERENCES appointments(appointment_id)
            )
        """)

        conn.commit()

        print("All hospital tables created successfully!")

    except Exception as e:
        conn.rollback()
        print("Error creating tables:", e)

    finally:
        cursor.close()
        conn.close()