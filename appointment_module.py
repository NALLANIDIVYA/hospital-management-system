from hospital.config import get_connection

from hospital.validators import (
    validate_date,
    validate_required,
    validate_time_slot
)


def book_appointment():

    print("\n========== BOOK APPOINTMENT ==========")

    patient_id = input("Enter patient ID: ")

    if not patient_id.isdigit():
        print("Invalid patient ID.")
        return

    doctor_id = input("Enter doctor ID: ")

    if not doctor_id.isdigit():
        print("Invalid doctor ID.")
        return

    appointment_date = input(
        "Enter appointment date (YYYY-MM-DD): "
    )

    if not validate_date(appointment_date):
        print("Invalid date. Use YYYY-MM-DD.")
        return

    time_slot = input(
        "Enter time slot (10:00-10:30): "
    )

    if not validate_time_slot(time_slot):
        print("Invalid time slot. Use HH:MM-HH:MM.")
        return

    notes = input("Enter notes: ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT patient_id
            FROM patients
            WHERE patient_id = %s
            AND status = 'ACTIVE'
        """, (patient_id,))

        if cursor.fetchone() is None:
            print("Patient not found or inactive.")
            return

        cursor.execute("""
            SELECT doctor_id
            FROM doctors
            WHERE doctor_id = %s
            AND status = 'ACTIVE'
        """, (doctor_id,))

        if cursor.fetchone() is None:
            print("Doctor not found or inactive.")
            return

        cursor.execute("""
            SELECT appointment_id
            FROM appointments
            WHERE doctor_id = %s
            AND appointment_date = %s
            AND time_slot = %s
            AND status NOT IN ('CANCELLED', 'NO_SHOW')
        """, (
            doctor_id,
            appointment_date,
            time_slot
        ))

        if cursor.fetchone():
            print(
                "This doctor already has an appointment "
                "in this time slot."
            )
            return

        query = """
            INSERT INTO appointments
            (
                patient_id,
                doctor_id,
                appointment_date,
                time_slot,
                notes
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                patient_id,
                doctor_id,
                appointment_date,
                time_slot,
                notes
            )
        )

        conn.commit()

        print("Appointment booked successfully!")
        print("Appointment ID:", cursor.lastrowid)

    except Exception as e:

        conn.rollback()
        print("Error booking appointment:", e)

    finally:

        cursor.close()
        conn.close()


def view_appointments():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                a.appointment_id,
                p.patient_name,
                d.doctor_name,
                a.appointment_date,
                a.time_slot,
                a.status,
                a.notes
            FROM appointments a
            JOIN patients p
                ON a.patient_id = p.patient_id
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date
        """)

        appointments = cursor.fetchall()

        if not appointments:
            print("No appointments found.")
            return

        print("\n========== ALL APPOINTMENTS ==========")

        for appointment in appointments:

            print("Appointment ID:", appointment[0])
            print("Patient:", appointment[1])
            print("Doctor:", appointment[2])
            print("Date:", appointment[3])
            print("Time:", appointment[4])
            print("Status:", appointment[5])
            print("Notes:", appointment[6])
            print("--------------------------------")

    except Exception as e:

        print("Error viewing appointments:", e)

    finally:

        cursor.close()
        conn.close()


def view_appointments_by_date():

    print("\n========== APPOINTMENTS BY DATE ==========")

    appointment_date = input(
        "Enter date (YYYY-MM-DD): "
    )

    if not validate_date(appointment_date):
        print("Invalid date. Use YYYY-MM-DD.")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        query = """
            SELECT
                a.appointment_id,
                p.patient_name,
                d.doctor_name,
                a.time_slot,
                a.status,
                a.notes
            FROM appointments a
            JOIN patients p
                ON a.patient_id = p.patient_id
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            WHERE a.appointment_date = %s
            ORDER BY a.time_slot
        """

        cursor.execute(
            query,
            (appointment_date,)
        )

        appointments = cursor.fetchall()

        if not appointments:
            print("No appointments found for this date.")
            return

        for appointment in appointments:

            print("Appointment ID:", appointment[0])
            print("Patient:", appointment[1])
            print("Doctor:", appointment[2])
            print("Time:", appointment[3])
            print("Status:", appointment[4])
            print("Notes:", appointment[5])
            print("--------------------------------")

    except Exception as e:

        print("Error viewing appointments:", e)

    finally:

        cursor.close()
        conn.close()


def cancel_appointment():

    appointment_id = input(
        "Enter appointment ID: "
    )

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE appointments
            SET status = 'CANCELLED'
            WHERE appointment_id = %s
        """, (appointment_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print("Appointment cancelled successfully!")
        else:
            print("Appointment not found.")

    except Exception as e:

        conn.rollback()
        print("Error cancelling appointment:", e)

    finally:

        cursor.close()
        conn.close()


def reschedule_appointment():

    appointment_id = input(
        "Enter appointment ID: "
    )

    new_date = input(
        "Enter new date (YYYY-MM-DD): "
    )

    if not validate_date(new_date):
        print("Invalid date. Use YYYY-MM-DD.")
        return

    new_slot = input(
        "Enter new time slot (10:00-10:30): "
    )

    if not validate_time_slot(new_slot):
        print("Invalid time slot. Use HH:MM-HH:MM.")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE appointments
            SET appointment_date = %s,
                time_slot = %s
            WHERE appointment_id = %s
        """, (
            new_date,
            new_slot,
            appointment_id
        ))

        conn.commit()

        if cursor.rowcount > 0:
            print("Appointment rescheduled successfully!")
        else:
            print("Appointment not found.")

    except Exception as e:

        conn.rollback()
        print("Error rescheduling appointment:", e)

    finally:

        cursor.close()
        conn.close()


def mark_completed():

    appointment_id = input(
        "Enter appointment ID: "
    )

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE appointments
            SET status = 'COMPLETED'
            WHERE appointment_id = %s
        """, (appointment_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print("Appointment marked as COMPLETED!")
        else:
            print("Appointment not found.")

    except Exception as e:

        conn.rollback()
        print("Error:", e)

    finally:

        cursor.close()
        conn.close()