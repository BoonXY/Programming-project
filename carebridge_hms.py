"""
CareBridge Hospital Management System
IC33006FP - Programming 1 Project

A simple text-based, menu-driven prototype covering four core functions:
    1. Register Patient
    2. Book Appointment
    3. Calculate Bill
    4. Assign Triage Room

All user input is validated: invalid entries trigger an error message and
the program re-prompts until a valid value is supplied.
"""

from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------
BASE_CONSULTATION_FEE = 100.00          # Flat fee charged for every consultation
LAB_TEST_RATE = 10.00                   # Cost per lab test
SUBSIDISED_DISCOUNT_MULTIPLIER = 0.70   # Subsidised patients pay 70% of subtotal (30% off)
MIN_DAYS_AHEAD_FOR_APPOINTMENT = 7      # Appointment date must be MORE than this many days away
DATE_FORMAT = "%Y-%m-%d"

VALID_DEPARTMENTS = ("GP", "SPECIALIST")
VALID_PATIENT_TYPES = ("SUBSIDISED", "PRIVATE")

MIN_SEVERITY = 1
MAX_SEVERITY = 10


# ---------------------------------------------------------------------------
# FUNCTION 1: REGISTER PATIENT
# ---------------------------------------------------------------------------
def register_patient():
    """
    Register a new patient.

    Inputs:
        - Patient name    (non-blank string)
        - Patient age     (positive whole number)
        - Patient ID      (non-blank string)
    Process:
        - Repeatedly prompt for each value until it passes validation,
          displaying an error message on every invalid attempt.
    Outputs:
        - A confirmation message showing the registered patient's details.
    """
    print("\n--- Register Patient ---")

    # --- Name: must not be blank ---
    while True:
        name = input("Enter patient's name: ").strip()
        if name == "":
            print("Error: Name cannot be blank. Please try again.")
        else:
            break

    # --- Age: must be a positive whole number ---
    while True:
        age_input = input("Enter patient's age: ").strip()
        if not age_input.isdigit():
            print("Error: Age must be a positive whole number. Please try again.")
            continue
        age = int(age_input)
        if age <= 0:
            print("Error: Age must be a positive whole number. Please try again.")
            continue
        break

    # --- ID: must not be blank ---
    while True:
        patient_id = input("Enter patient's ID: ").strip()
        if patient_id == "":
            print("Error: Patient ID cannot be blank. Please try again.")
        else:
            break

    print("\nPatient registered successfully!")
    print(f"Name : {name}")
    print(f"Age  : {age}")
    print(f"ID   : {patient_id}")


# ---------------------------------------------------------------------------
# FUNCTION 2: BOOK APPOINTMENT
# ---------------------------------------------------------------------------
def book_appointment():
    """
    Book an appointment for a patient.

    Inputs:
        - Department       (GP or Specialist)
        - Appointment date (valid date, more than 7 days from today)
    Process:
        - Repeatedly prompt for each value until it passes validation,
          displaying an error message on every invalid attempt.
    Outputs:
        - A confirmation message showing the booked department and date.
    """
    print("\n--- Book Appointment ---")

    # --- Department: must be GP or Specialist ---
    while True:
        department = input("Enter department (GP / Specialist): ").strip().upper()
        if department not in VALID_DEPARTMENTS:
            print("Error: Department must be 'GP' or 'Specialist'. Please try again.")
        else:
            break

    # --- Appointment date: must be valid AND more than 7 days from today ---
    while True:
        date_input = input("Enter appointment date (YYYY-MM-DD): ").strip()
        try:
            appointment_date = datetime.strptime(date_input, DATE_FORMAT).date()
        except ValueError:
            print("Error: Date must be a valid date in YYYY-MM-DD format. Please try again.")
            continue

        earliest_allowed_date = datetime.now().date() + timedelta(days=MIN_DAYS_AHEAD_FOR_APPOINTMENT)
        if appointment_date <= earliest_allowed_date:
            print(f"Error: Appointment date must be more than {MIN_DAYS_AHEAD_FOR_APPOINTMENT} "
                  f"days from today. Please try again.")
            continue
        break

    department_display = "GP" if department == "GP" else "Specialist"
    print("\nAppointment booked successfully!")
    print(f"Department : {department_display}")
    print(f"Date       : {appointment_date.strftime(DATE_FORMAT)}")


# ---------------------------------------------------------------------------
# FUNCTION 3: CALCULATE BILL
# ---------------------------------------------------------------------------
def calculate_bill():
    """
    Calculate a patient's bill.

    Inputs:
        - Patient type          (Subsidised or Private)
        - Number of lab tests   (whole number, zero or more)
    Process:
        - subtotal = BASE_CONSULTATION_FEE + (number_of_lab_tests * LAB_TEST_RATE)
        - Subsidised patients receive a 30% discount (total = subtotal * 0.70)
        - Private patients pay the full subtotal
    Outputs:
        - The patient type and the final amount to pay.
    """
    print("\n--- Calculate Bill ---")

    # --- Patient type: must be Subsidised or Private ---
    while True:
        patient_type = input("Enter patient type (Subsidised / Private): ").strip().upper()
        if patient_type not in VALID_PATIENT_TYPES:
            print("Error: Patient type must be 'Subsidised' or 'Private'. Please try again.")
        else:
            break

    # --- Number of lab tests: must be a whole number ---
    while True:
        tests_input = input("Enter number of lab tests completed: ").strip()
        if not tests_input.isdigit():
            print("Error: Number of lab tests must be a whole number. Please try again.")
            continue
        num_lab_tests = int(tests_input)
        break

    subtotal = BASE_CONSULTATION_FEE + (num_lab_tests * LAB_TEST_RATE)

    if patient_type == "SUBSIDISED":
        total = subtotal * SUBSIDISED_DISCOUNT_MULTIPLIER
    else:
        total = subtotal

    patient_type_display = "Subsidised" if patient_type == "SUBSIDISED" else "Private"
    print("\nBill calculated successfully!")
    print(f"Patient Type : {patient_type_display}")
    print(f"Total to Pay : ${total:.2f}")


# ---------------------------------------------------------------------------
# FUNCTION 4: ASSIGN TRIAGE ROOM
# ---------------------------------------------------------------------------
def assign_triage_room():
    """
    Assign a triage room based on severity of condition.

    Inputs:
        - Severity of condition (whole number from 1 to 10)
    Process:
        - 1-4  -> Waiting Room
        - 5-7  -> Room 1
        - 8-10 -> Room 2
    Outputs:
        - A triage summary showing the severity level and assigned room.
    """
    print("\n--- Assign Triage Room ---")

    while True:
        severity_input = input(f"Enter severity of condition ({MIN_SEVERITY}-{MAX_SEVERITY}): ").strip()
        if not severity_input.isdigit():
            print(f"Error: Severity must be a whole number from {MIN_SEVERITY} to {MAX_SEVERITY}. "
                  f"Please try again.")
            continue
        severity = int(severity_input)
        if severity < MIN_SEVERITY or severity > MAX_SEVERITY:
            print(f"Error: Severity must be a whole number from {MIN_SEVERITY} to {MAX_SEVERITY}. "
                  f"Please try again.")
            continue
        break

    if severity <= 4:
        room = "Waiting Room"
    elif severity <= 7:
        room = "Room 1"
    else:
        room = "Room 2"

    print("\nTriage Summary")
    print(f"Severity Level : {severity}")
    print(f"Assigned Room  : {room}")


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------
def display_menu():
    print("\n===== CareBridge Hospital Management System =====")
    print("1. Register Patient")
    print("2. Book Appointment")
    print("3. Calculate Bill")
    print("4. Assign Triage Room")
    print("5. Exit")


def main():
    while True:
        display_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            register_patient()
        elif choice == "2":
            book_appointment()
        elif choice == "3":
            calculate_bill()
        elif choice == "4":
            assign_triage_room()
        elif choice == "5":
            print("\nExiting the system. Goodbye!")
            break
        else:
            print("Error: Please select a valid option (1-5).")


if __name__ == "__main__":
    main()
