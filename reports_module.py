from hospital.config import get_connection


def todays_appointments():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT a.appointment_id,
                   p.patient_name,
                   d.doctor_name,
                   a.time_slot,
                   a.status
            FROM appointments a
            JOIN patients p
                ON a.patient_id = p.patient_id
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            WHERE a.appointment_date = CURDATE()
            ORDER BY a.time_slot
        """)

        results = cursor.fetchall()

        if not results:
            print("No appointments today.")
            return

        print("\n========== TODAY'S APPOINTMENTS ==========")

        for r in results:
            print(r)

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


def appointments_by_date_range():

    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT a.appointment_id,
                   p.patient_name,
                   d.doctor_name,
                   a.appointment_date,
                   a.time_slot,
                   a.status
            FROM appointments a
            JOIN patients p
                ON a.patient_id = p.patient_id
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            WHERE a.appointment_date
            BETWEEN %s AND %s
        """, (start_date, end_date))

        results = cursor.fetchall()

        for r in results:
            print(r)

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


def doctor_appointment_count():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT d.doctor_name,
                   COUNT(a.appointment_id)
            FROM doctors d
            LEFT JOIN appointments a
                ON d.doctor_id = a.doctor_id
            GROUP BY d.doctor_id, d.doctor_name
        """)

        results = cursor.fetchall()

        print("\n========== DOCTOR-WISE COUNT ==========")

        for r in results:
            print("Doctor:", r[0])
            print("Appointments:", r[1])
            print("--------------------------------")

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


def patient_visit_history():

    patient_id = input("Enter patient ID: ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT a.appointment_id,
                   d.doctor_name,
                   a.appointment_date,
                   a.time_slot,
                   a.status
            FROM appointments a
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            WHERE a.patient_id = %s
            ORDER BY a.appointment_date DESC
        """, (patient_id,))

        results = cursor.fetchall()

        for r in results:
            print(r)

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


def revenue_summary():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT COUNT(bill_id),
                   COALESCE(SUM(amount), 0),
                   COALESCE(
                       SUM(
                           CASE
                               WHEN payment_status = 'PAID'
                               THEN amount
                               ELSE 0
                           END
                       ),
                       0
                   )
            FROM bills
        """)

        result = cursor.fetchone()

        print("\n========== REVENUE SUMMARY ==========")
        print("Total Bills:", result[0])
        print("Total Amount:", result[1])
        print("Paid Amount:", result[2])

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


def cancelled_no_show_statistics():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT status, COUNT(*)
            FROM appointments
            WHERE status IN ('CANCELLED', 'NO_SHOW')
            GROUP BY status
        """)

        results = cursor.fetchall()

        if not results:
            print("No cancelled or no-show appointments.")
            return

        for r in results:
            print(r[0], ":", r[1])

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()