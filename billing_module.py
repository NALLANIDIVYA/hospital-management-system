from hospital.config import get_connection


def generate_bill():

    print("\n========== GENERATE BILL ==========")

    appointment_id = input("Enter completed appointment ID: ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT a.status,
                   d.consultation_fee,
                   p.patient_name,
                   d.doctor_name
            FROM appointments a
            JOIN patients p
                ON a.patient_id = p.patient_id
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            WHERE a.appointment_id = %s
        """, (appointment_id,))

        result = cursor.fetchone()

        if not result:
            print("Appointment not found.")
            return

        status = result[0]
        fee = result[1]
        patient = result[2]
        doctor = result[3]

        if status != "COMPLETED":
            print("Bill can be generated only for COMPLETED appointments.")
            return

        cursor.execute("""
            SELECT bill_id
            FROM bills
            WHERE appointment_id = %s
        """, (appointment_id,))

        if cursor.fetchone():
            print("Bill already exists for this appointment.")
            return

        cursor.execute("""
            INSERT INTO bills
            (appointment_id, amount)
            VALUES (%s, %s)
        """, (appointment_id, fee))

        conn.commit()

        print("Bill generated successfully!")
        print("Patient:", patient)
        print("Doctor:", doctor)
        print("Consultation Fee:", fee)
        print("Payment Status: PENDING")
        print("Bill ID:", cursor.lastrowid)

    except Exception as e:
        conn.rollback()
        print("Error generating bill:", e)

    finally:
        cursor.close()
        conn.close()


def view_bills():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT b.bill_id,
                   b.appointment_id,
                   p.patient_name,
                   d.doctor_name,
                   b.amount,
                   b.payment_status,
                   b.billed_at
            FROM bills b
            JOIN appointments a
                ON b.appointment_id = a.appointment_id
            JOIN patients p
                ON a.patient_id = p.patient_id
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
        """)

        bills = cursor.fetchall()

        if not bills:
            print("No bills found.")
            return

        for bill in bills:

            print("Bill ID:", bill[0])
            print("Appointment ID:", bill[1])
            print("Patient:", bill[2])
            print("Doctor:", bill[3])
            print("Amount:", bill[4])
            print("Payment Status:", bill[5])
            print("Billed At:", bill[6])
            print("--------------------------------")

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


def mark_bill_paid():

    bill_id = input("Enter bill ID: ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE bills
            SET payment_status = 'PAID'
            WHERE bill_id = %s
        """, (bill_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print("Bill marked as PAID!")
        else:
            print("Bill not found.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()