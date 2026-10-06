from hospital.config import get_connection


def add_department():

    print("\n========== ADD DEPARTMENT ==========")

    name = input("Enter department name: ")
    description = input("Enter description: ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        query = """
            INSERT INTO departments
            (dept_name, description)
            VALUES (%s, %s)
        """

        cursor.execute(query, (name, description))

        conn.commit()

        print("Department added successfully!")
        print("Department ID:", cursor.lastrowid)

    except Exception as e:
        conn.rollback()
        print("Error adding department:", e)

    finally:
        cursor.close()
        conn.close()


def view_departments():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT dept_id, dept_name, description
            FROM departments
            ORDER BY dept_id
        """)

        departments = cursor.fetchall()

        print("\n========== DEPARTMENTS ==========")

        if not departments:
            print("No departments found.")
            return

        for dept in departments:

            print("Department ID:", dept[0])
            print("Name:", dept[1])
            print("Description:", dept[2])
            print("--------------------------------")

    except Exception as e:
        print("Error viewing departments:", e)

    finally:
        cursor.close()
        conn.close()


def update_department():

    dept_id = input("Enter department ID: ")
    name = input("Enter new department name: ")
    description = input("Enter new description: ")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        query = """
            UPDATE departments
            SET dept_name = %s,
                description = %s
            WHERE dept_id = %s
        """

        cursor.execute(
            query,
            (name, description, dept_id)
        )

        conn.commit()

        if cursor.rowcount > 0:
            print("Department updated successfully!")
        else:
            print("Department not found.")

    except Exception as e:
        conn.rollback()
        print("Error updating department:", e)

    finally:
        cursor.close()
        conn.close()