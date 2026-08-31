"""
CareBridge Hospital Management System — core business logic.

Same validation rules and calculations as the original console prototype,
refactored into pure functions so the web front end can reuse them. None
of these functions read from the keyboard or print to the screen: each
takes plain form values in, and returns whether they were valid, any
error messages, and (when valid) the computed result.
"""

from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# CONSTANTS (identical to the console version)
# ---------------------------------------------------------------------------
BASE_CONSULTATION_FEE = 100.00
LAB_TEST_RATE = 10.00
SUBSIDISED_DISCOUNT_MULTIPLIER = 0.70
MIN_DAYS_AHEAD_FOR_APPOINTMENT = 7
DATE_FORMAT = "%Y-%m-%d"

VALID_DEPARTMENTS = ("GP", "SPECIALIST")
VALID_PATIENT_TYPES = ("SUBSIDISED", "PRIVATE")

MIN_SEVERITY = 1
MAX_SEVERITY = 10

# (low, high, room name, css class used to colour the result)
TRIAGE_BANDS = (
    (1, 4, "Waiting Room", "waiting"),
    (5, 7, "Room 1", "room1"),
    (8, 10, "Room 2", "room2"),
)


def validate_patient(name, age_input, patient_id):
    """Inputs: name, age, ID strings. Output: (is_valid, errors, data)."""
    errors = {}
    name = (name or "").strip()
    patient_id = (patient_id or "").strip()
    age_input = (age_input or "").strip()

    if name == "":
        errors["name"] = "Name cannot be blank."

    age = None
    if not age_input.isdigit():
        errors["age"] = "Age must be a positive whole number."
    else:
        age = int(age_input)
        if age <= 0:
            errors["age"] = "Age must be a positive whole number."

    if patient_id == "":
        errors["patient_id"] = "Patient ID cannot be blank."

    if errors:
        return False, errors, {}
    return True, {}, {"name": name, "age": age, "patient_id": patient_id}


def validate_appointment(department_input, date_input):
    """Inputs: department, date strings. Output: (is_valid, errors, data)."""
    errors = {}
    department = (department_input or "").strip().upper()
    date_input = (date_input or "").strip()

    if department not in VALID_DEPARTMENTS:
        errors["department"] = "Choose GP or Specialist."

    appointment_date = None
    try:
        appointment_date = datetime.strptime(date_input, DATE_FORMAT).date()
        earliest_allowed = datetime.now().date() + timedelta(days=MIN_DAYS_AHEAD_FOR_APPOINTMENT)
        if appointment_date <= earliest_allowed:
            errors["date"] = (
                f"Date must be more than {MIN_DAYS_AHEAD_FOR_APPOINTMENT} days from today."
            )
    except ValueError:
        errors["date"] = "Enter a valid date in YYYY-MM-DD format."

    if errors:
        return False, errors, {}

    department_display = "GP" if department == "GP" else "Specialist"
    return True, {}, {
        "department": department_display,
        "date": appointment_date.strftime(DATE_FORMAT),
    }


def validate_bill(patient_type_input, tests_input):
    """Inputs: patient type, lab test count strings. Output: (is_valid, errors, data)."""
    errors = {}
    patient_type = (patient_type_input or "").strip().upper()
    tests_input = (tests_input or "").strip()

    if patient_type not in VALID_PATIENT_TYPES:
        errors["patient_type"] = "Choose Subsidised or Private."

    num_tests = None
    if not tests_input.isdigit():
        errors["num_tests"] = "Number of lab tests must be a whole number."
    else:
        num_tests = int(tests_input)

    if errors:
        return False, errors, {}

    subtotal = BASE_CONSULTATION_FEE + (num_tests * LAB_TEST_RATE)
    if patient_type == "SUBSIDISED":
        total = subtotal * SUBSIDISED_DISCOUNT_MULTIPLIER
    else:
        total = subtotal
    patient_type_display = "Subsidised" if patient_type == "SUBSIDISED" else "Private"

    return True, {}, {
        "patient_type": patient_type_display,
        "num_tests": num_tests,
        "subtotal": subtotal,
        "total": total,
    }


def validate_triage(severity_input):
    """Input: severity string. Output: (is_valid, errors, data)."""
    errors = {}
    severity_input = (severity_input or "").strip()

    severity = None
    if not severity_input.isdigit():
        errors["severity"] = (
            f"Severity must be a whole number from {MIN_SEVERITY} to {MAX_SEVERITY}."
        )
    else:
        severity = int(severity_input)
        if severity < MIN_SEVERITY or severity > MAX_SEVERITY:
            errors["severity"] = (
                f"Severity must be a whole number from {MIN_SEVERITY} to {MAX_SEVERITY}."
            )

    if errors:
        return False, errors, {}

    for low, high, room_name, room_class in TRIAGE_BANDS:
        if low <= severity <= high:
            return True, {}, {"severity": severity, "room": room_name, "room_class": room_class}
