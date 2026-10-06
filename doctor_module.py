from hospital.config import get_connection

from hospital.validators import (
    validate_name,
    validate_phone,
    validate_positive_number,
    validate_required
)


def add_doctor():

    print("\n========== ADD DOCTOR ==========")

    doctor_name = input("Enter doctor name: ")

    if not validate_name(doctor_name):
        print("Invalid doctor name. Use letters and spaces only.")
        return

    department_id = input("Enter department ID: ")

    if not department_id.isdigit():
        print("Invalid department ID.")
        return

    phone = input("Enter phone number: ")

    if not validate_phone(phone):
        print("Invalid phone number.")
        return

    fee = input("Enter consultation fee: ")

    if not validate_positive_number(fee):
        print("Invalid consultation fee.")
        return

    available_slots = input("Enter available slots: ")

    if not validate_required(available_slots):
        print("Available slots cannot be empty.")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        query = """
            INSERT INTO doctors
            (doctor_name, dept_id, phone,
             consultation_fee, available_slots)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                doctor_name,
                department_id,
                phone,
                fee,
                available_slots
            )
        )

        conn.commit()

        print("Doctor added successfully!")
        print("Doctor ID:", cursor.lastrowid)

    except Exception as e:
        conn.rollback()
        print("Error adding doctor:", e)

    finally:
        cursor.close()
        conn.close()


def view_doctors():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        query = """
            SELECT d.doctor_id,
                   d.doctor_name,
                   dept.dept_name,
                   d.phone,
                   d.consultation_fee,
                   d.available_slots,
                   d.status
            FROM doctors d
            JOIN departments dept
                ON d.dept_id = dept.dept_id
            ORDER BY d.doctor_id
        """

        cursor.execute(query)

        doctors = cursor.fetchall()

        if not doctors:
            print("No doctors found.")
            return

        print("\n========== ALL DOCTORS ==========")

        for doctor in doctors:

            print("Doctor ID:", doctor[0])
            print("Name:", doctor[1])
            print("Department:", doctor[2])
            print("Phone:", doctor[3])
            print("Consultation Fee:", doctor[4])
            print("Available Slots:", doctor[5])
            print("Status:", doctor[6])
            print("--------------------------------")

    except Exception as e:
        print("Error viewing doctors:", e)

    finally:
        cursor.close()
        conn.close()


def view_doctors_by_department():

    department_id = input("Enter department ID: ")

    if not department_id.isdigit():
        print("Invalid department ID.")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT doctor_id,
                   doctor_name,
                   phone,
                   consultation_fee,
                   available_slots,
                   status
            FROM doctors
            WHERE dept_id = %s
              AND status = 'ACTIVE'
        """, (department_id,))

        doctors = cursor.fetchall()

        if not doctors:
            print("No doctors found.")
            return

        for doctor in doctors:

            print("Doctor ID:", doctor[0])
            print("Name:", doctor[1])
            print("Phone:", doctor[2])
            print("Fee:", doctor[3])
            print("Slots:", doctor[4])
            print("Status:", doctor[5])
            print("--------------------------------")

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


def update_doctor():

    doctor_id = input("Enter doctor ID: ")
    phone = input("Enter new phone number: ")
    fee = input("Enter new consultation fee: ")
    slots = input("Enter new available slots: ")

    if not doctor_id.isdigit():
        print("Invalid doctor ID.")
        return

    if not validate_phone(phone):
        print("Invalid phone number.")
        return

    if not validate_positive_number(fee):
        print("Invalid consultation fee.")
        return

    if not validate_required(slots):
        print("Slots cannot be empty.")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE doctors
            SET phone = %s,
                consultation_fee = %s,
                available_slots = %s
            WHERE doctor_id = %s
        """, (phone, fee, slots, doctor_id))

        conn.commit()

        if cursor.rowcount > 0:
            print("Doctor updated successfully!")
        else:
            print("Doctor not found.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


def deactivate_doctor():

    doctor_id = input("Enter doctor ID: ")

    if not doctor_id.isdigit():
        print("Invalid doctor ID.")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE doctors
            SET status = 'INACTIVE'
            WHERE doctor_id = %s
        """, (doctor_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print("Doctor deactivated successfully!")
        else:
            print("Doctor not found.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()