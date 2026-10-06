from hospital.config import get_connection

from hospital.validators import (
    validate_name,
    validate_gender,
    validate_phone,
    validate_date,
    validate_required
)


def add_patient():

    print("\n========== REGISTER PATIENT ==========")

    name = input("Enter patient name: ")

    if not validate_name(name):
        print("Invalid name. Use letters and spaces only.")
        return

    gender = input("Enter gender (Male/Female/Other): ")

    if not validate_gender(gender):
        print("Invalid gender. Enter Male, Female, or Other.")
        return

    dob = input("Enter date of birth (YYYY-MM-DD): ")

    if not validate_date(dob):
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    phone = input("Enter phone number: ")

    if not validate_phone(phone):
        print("Invalid phone number. Enter exactly 10 digits.")
        return

    address = input("Enter address: ")

    if not validate_required(address):
        print("Address cannot be empty.")
        return

    blood_group = input("Enter blood group: ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        query = """
            INSERT INTO patients
            (patient_name, gender, dob, phone, address, blood_group)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                name,
                gender,
                dob,
                phone,
                address,
                blood_group
            )
        )

        conn.commit()

        print("Patient registered successfully!")
        print("Patient ID:", cursor.lastrowid)

    except Exception as e:
        conn.rollback()
        print("Error registering patient:", e)

    finally:
        cursor.close()
        conn.close()


def view_patients():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT patient_id,
                   patient_name,
                   gender,
                   dob,
                   phone,
                   address,
                   blood_group,
                   status
            FROM patients
        """)

        patients = cursor.fetchall()

        if not patients:
            print("No patients found.")
            return

        print("\n========== ALL PATIENTS ==========")

        for patient in patients:

            print("Patient ID:", patient[0])
            print("Name:", patient[1])
            print("Gender:", patient[2])
            print("DOB:", patient[3])
            print("Phone:", patient[4])
            print("Address:", patient[5])
            print("Blood Group:", patient[6])
            print("Status:", patient[7])
            print("--------------------------------")

    except Exception as e:
        print("Error viewing patients:", e)

    finally:
        cursor.close()
        conn.close()


def search_patient():

    search = input("Enter patient ID, name or phone: ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        query = """
            SELECT patient_id,
                   patient_name,
                   gender,
                   dob,
                   phone,
                   address,
                   blood_group,
                   status
            FROM patients
            WHERE patient_id = %s
               OR patient_name LIKE %s
               OR phone = %s
        """

        cursor.execute(
            query,
            (
                search,
                "%" + search + "%",
                search
            )
        )

        patients = cursor.fetchall()

        if not patients:
            print("Patient not found.")
            return

        for patient in patients:

            print("\nPatient ID:", patient[0])
            print("Name:", patient[1])
            print("Gender:", patient[2])
            print("DOB:", patient[3])
            print("Phone:", patient[4])
            print("Address:", patient[5])
            print("Blood Group:", patient[6])
            print("Status:", patient[7])

    except Exception as e:
        print("Error searching patient:", e)

    finally:
        cursor.close()
        conn.close()


def update_patient():

    patient_id = input("Enter patient ID: ")
    phone = input("Enter new phone: ")
    address = input("Enter new address: ")
    blood_group = input("Enter new blood group: ")

    if not validate_phone(phone):
        print("Invalid phone number.")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        query = """
            UPDATE patients
            SET phone = %s,
                address = %s,
                blood_group = %s
            WHERE patient_id = %s
        """

        cursor.execute(
            query,
            (
                phone,
                address,
                blood_group,
                patient_id
            )
        )

        conn.commit()

        if cursor.rowcount > 0:
            print("Patient updated successfully!")
        else:
            print("Patient not found.")

    except Exception as e:
        conn.rollback()
        print("Error updating patient:", e)

    finally:
        cursor.close()
        conn.close()


def deactivate_patient():

    patient_id = input("Enter patient ID: ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE patients
            SET status = 'INACTIVE'
            WHERE patient_id = %s
        """, (patient_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print("Patient deactivated successfully!")
        else:
            print("Patient not found.")

    except Exception as e:
        conn.rollback()
        print("Error deactivating patient:", e)

    finally:
        cursor.close()
        conn.close()