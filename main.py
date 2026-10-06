from hospital.db_setup import create_database_tables

from hospital.department_module import (
    add_department,
    view_departments,
    update_department
)

from hospital.patient_module import (
    add_patient,
    view_patients,
    search_patient,
    update_patient,
    deactivate_patient
)

from hospital.doctor_module import (
    add_doctor,
    view_doctors,
    view_doctors_by_department,
    update_doctor,
    deactivate_doctor
)

from hospital.appointment_module import (
    book_appointment,
    view_appointments,
    view_appointments_by_date,
    cancel_appointment,
    reschedule_appointment,
    mark_completed
)

from hospital.billing_module import (
    generate_bill,
    view_bills,
    mark_bill_paid
)

from hospital.reports_module import (
    todays_appointments,
    appointments_by_date_range,
    doctor_appointment_count,
    patient_visit_history,
    revenue_summary,
    cancelled_no_show_statistics
)


create_database_tables()


def patient_menu():

    while True:

        print("\n========== PATIENT MENU ==========")
        print("1. Register Patient")
        print("2. View Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Deactivate Patient")
        print("6. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_patient()

        elif choice == "2":
            view_patients()

        elif choice == "3":
            search_patient()

        elif choice == "4":
            update_patient()

        elif choice == "5":
            deactivate_patient()

        elif choice == "6":
            break

        else:
            print("Invalid choice!")


def doctor_menu():

    while True:

        print("\n========== DOCTOR MENU ==========")
        print("1. Add Doctor")
        print("2. View Doctors")
        print("3. Doctors by Department")
        print("4. Update Doctor")
        print("5. Deactivate Doctor")
        print("6. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_doctor()

        elif choice == "2":
            view_doctors()

        elif choice == "3":
            view_doctors_by_department()

        elif choice == "4":
            update_doctor()

        elif choice == "5":
            deactivate_doctor()

        elif choice == "6":
            break

        else:
            print("Invalid choice!")


def department_menu():

    while True:

        print("\n========== DEPARTMENT MENU ==========")
        print("1. Add Department")
        print("2. View Departments")
        print("3. Update Department")
        print("4. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_department()

        elif choice == "2":
            view_departments()

        elif choice == "3":
            update_department()

        elif choice == "4":
            break

        else:
            print("Invalid choice!")


def appointment_menu():

    while True:

        print("\n========== APPOINTMENT MENU ==========")
        print("1. Book Appointment")
        print("2. View Appointments")
        print("3. Appointments by Date")
        print("4. Cancel Appointment")
        print("5. Reschedule Appointment")
        print("6. Mark Completed")
        print("7. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            book_appointment()

        elif choice == "2":
            view_appointments()

        elif choice == "3":
            view_appointments_by_date()

        elif choice == "4":
            cancel_appointment()

        elif choice == "5":
            reschedule_appointment()

        elif choice == "6":
            mark_completed()

        elif choice == "7":
            break

        else:
            print("Invalid choice!")


def billing_menu():

    while True:

        print("\n========== BILLING MENU ==========")
        print("1. Generate Bill")
        print("2. View Bills")
        print("3. Mark Bill Paid")
        print("4. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            generate_bill()

        elif choice == "2":
            view_bills()

        elif choice == "3":
            mark_bill_paid()

        elif choice == "4":
            break

        else:
            print("Invalid choice!")


def reports_menu():

    while True:

        print("\n========== REPORTS MENU ==========")
        print("1. Today's Appointments")
        print("2. Date Range Appointments")
        print("3. Doctor-wise Count")
        print("4. Patient Visit History")
        print("5. Revenue Summary")
        print("6. Cancelled / No-show")
        print("7. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            todays_appointments()

        elif choice == "2":
            appointments_by_date_range()

        elif choice == "3":
            doctor_appointment_count()

        elif choice == "4":
            patient_visit_history()

        elif choice == "5":
            revenue_summary()

        elif choice == "6":
            cancelled_no_show_statistics()

        elif choice == "7":
            break

        else:
            print("Invalid choice!")


def main():

    while True:

        print("\n==========================================")
        print("       HOSPITAL APPOINTMENT SYSTEM")
        print("==========================================")
        print("1. Patient Module")
        print("2. Doctor Module")
        print("3. Department Module")
        print("4. Appointment Module")
        print("5. Billing Module")
        print("6. Reports Module")
        print("7. Exit")
        print("==========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            patient_menu()

        elif choice == "2":
            doctor_menu()

        elif choice == "3":
            department_menu()

        elif choice == "4":
            appointment_menu()

        elif choice == "5":
            billing_menu()

        elif choice == "6":
            reports_menu()

        elif choice == "7":
            print("Thank you for using Hospital Appointment System!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
