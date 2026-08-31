"""
CareBridge Hospital Management System — HTML rendering.

Plain string templates (no third-party templating engine). Every value
that came from user input is passed through esc() before being placed in
the page, so the front end can't be used to inject markup.
"""

import html

MENU_ITEMS = (
    ("register", "Register Patient", "Add a new patient record.", "dept-register"),
    ("appointment", "Book Appointment", "Schedule a GP or Specialist visit.", "dept-appointment"),
    ("bill", "Calculate Bill", "Consultation and lab test charges.", "dept-bill"),
    ("triage", "Assign Triage Room", "Severity-based room assignment.", "dept-triage"),
)


def esc(value):
    """Escape a value for safe insertion into HTML."""
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def layout(title, body, back_link=True):
    back = '<a class="back" href="/">&lsaquo; Back to menu</a>' if back_link else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} &middot; CareBridge</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header class="topbar">
  <span class="brand">CareBridge</span>
  <span class="portal">Staff Portal</span>
  {back}
</header>
<main class="content">
{body}
</main>
</body>
</html>"""


def menu_page():
    items_html = ""
    for slug, title, desc, css_var in MENU_ITEMS:
        items_html += f"""
        <li>
          <a class="menu-item" style="--tab-color: var(--{css_var})" href="/{slug}">
            <div class="item-title">{esc(title)}</div>
            <div class="item-desc">{esc(desc)}</div>
          </a>
        </li>"""

    body = f"""
    <div class="menu-intro">
      <h1>Front Desk Console</h1>
      <p>Choose a task to begin.</p>
    </div>
    <ul class="menu-list">{items_html}
    </ul>
    """
    return layout("Front Desk Console", body, back_link=False)


def _field(name, label, value="", error=None, hint=None, input_html=None):
    css_class = "field has-error" if error else "field"
    if input_html is None:
        input_html = (
            f'<input type="text" id="{name}" name="{name}" '
            f'value="{esc(value)}" autocomplete="off">'
        )
    extra = f'<div class="hint">{esc(hint)}</div>' if hint else ""
    error_html = f'<div class="error-msg">{esc(error)}</div>' if error else ""
    return f"""
    <div class="{css_class}">
      <label for="{name}">{esc(label)}</label>
      {input_html}
      {extra}
      {error_html}
    </div>"""


def _select(name, options, selected):
    opts = ['<option value="">-- Select --</option>']
    for value, label in options:
        is_selected = " selected" if selected == value else ""
        opts.append(f'<option value="{esc(value)}"{is_selected}>{esc(label)}</option>')
    return f'<select id="{name}" name="{name}">{"".join(opts)}</select>'


# ---------------------------------------------------------------------------
# 1. REGISTER PATIENT
# ---------------------------------------------------------------------------
def register_page(values=None, errors=None, result=None):
    values = values or {}
    errors = errors or {}

    if result:
        body = f"""
        <div class="page-intro">
          <h1>Register Patient</h1>
        </div>
        <div class="slip" style="--slip-color: var(--dept-register)">
          <h2>Patient registered successfully</h2>
          <div class="slip-row"><span class="label">Name</span><span class="value">{esc(result['name'])}</span></div>
          <div class="slip-row"><span class="label">Age</span><span class="value">{esc(result['age'])}</span></div>
          <div class="slip-row"><span class="label">Patient ID</span><span class="value">{esc(result['patient_id'])}</span></div>
        </div>
        <div class="actions">
          <a href="/register">Register another patient</a>
          <a href="/">Back to menu</a>
        </div>
        """
        return layout("Register Patient", body)

    body = f"""
    <div class="page-intro">
      <h1>Register Patient</h1>
      <p>Enter the patient's basic details.</p>
    </div>
    <form method="post" action="/register">
      {_field("name", "Full name", values.get("name", ""), errors.get("name"))}
      {_field("age", "Age", values.get("age", ""), errors.get("age"), hint="Whole number, greater than 0.")}
      {_field("patient_id", "Patient ID", values.get("patient_id", ""), errors.get("patient_id"))}
      <button class="submit-btn" type="submit">Register patient</button>
    </form>
    """
    return layout("Register Patient", body)


# ---------------------------------------------------------------------------
# 2. BOOK APPOINTMENT
# ---------------------------------------------------------------------------
def appointment_page(values=None, errors=None, result=None):
    values = values or {}
    errors = errors or {}

    if result:
        body = f"""
        <div class="page-intro">
          <h1>Book Appointment</h1>
        </div>
        <div class="slip" style="--slip-color: var(--dept-appointment)">
          <h2>Appointment booked successfully</h2>
          <div class="slip-row"><span class="label">Department</span><span class="value">{esc(result['department'])}</span></div>
          <div class="slip-row"><span class="label">Date</span><span class="value">{esc(result['date'])}</span></div>
        </div>
        <div class="actions">
          <a href="/appointment">Book another appointment</a>
          <a href="/">Back to menu</a>
        </div>
        """
        return layout("Book Appointment", body)

    dept_select = _select(
        "department",
        [("GP", "GP"), ("SPECIALIST", "Specialist")],
        (values.get("department", "")).upper(),
    )
    body = f"""
    <div class="page-intro">
      <h1>Book Appointment</h1>
      <p>Choose a department and preferred date.</p>
    </div>
    <form method="post" action="/appointment">
      {_field("department", "Department", input_html=dept_select, error=errors.get("department"))}
      {_field("date", "Appointment date", values.get("date", ""), errors.get("date"), hint="Format YYYY-MM-DD, more than 7 days from today.")}
      <button class="submit-btn" type="submit">Book appointment</button>
    </form>
    """
    return layout("Book Appointment", body)


# ---------------------------------------------------------------------------
# 3. CALCULATE BILL
# ---------------------------------------------------------------------------
def bill_page(values=None, errors=None, result=None):
    values = values or {}
    errors = errors or {}

    if result:
        body = f"""
        <div class="page-intro">
          <h1>Calculate Bill</h1>
        </div>
        <div class="slip" style="--slip-color: var(--dept-bill)">
          <h2>Bill calculated</h2>
          <div class="slip-row"><span class="label">Patient type</span><span class="value">{esc(result['patient_type'])}</span></div>
          <div class="slip-row"><span class="label">Lab tests</span><span class="value">{esc(result['num_tests'])}</span></div>
          <div class="slip-row"><span class="label">Subtotal</span><span class="value">${result['subtotal']:.2f}</span></div>
          <div class="slip-row total"><span class="label">Total to pay</span><span class="value">${result['total']:.2f}</span></div>
        </div>
        <div class="actions">
          <a href="/bill">Calculate another bill</a>
          <a href="/">Back to menu</a>
        </div>
        """
        return layout("Calculate Bill", body)

    type_select = _select(
        "patient_type",
        [("SUBSIDISED", "Subsidised"), ("PRIVATE", "Private")],
        (values.get("patient_type", "")).upper(),
    )
    body = f"""
    <div class="page-intro">
      <h1>Calculate Bill</h1>
      <p>Base consultation fee $100, plus $10 per lab test. Subsidised patients get 30% off.</p>
    </div>
    <form method="post" action="/bill">
      {_field("patient_type", "Patient type", input_html=type_select, error=errors.get("patient_type"))}
      {_field("num_tests", "Number of lab tests", values.get("num_tests", ""), errors.get("num_tests"))}
      <button class="submit-btn" type="submit">Calculate bill</button>
    </form>
    """
    return layout("Calculate Bill", body)


# ---------------------------------------------------------------------------
# 4. ASSIGN TRIAGE ROOM
# ---------------------------------------------------------------------------
def triage_page(values=None, errors=None, result=None):
    values = values or {}
    errors = errors or {}

    if result:
        body = f"""
        <div class="page-intro">
          <h1>Assign Triage Room</h1>
        </div>
        <div class="slip" style="--slip-color: var(--{result['room_class']})">
          <h2>Triage summary</h2>
          <div class="slip-row"><span class="label">Severity level</span><span class="value">{esc(result['severity'])} / 10</span></div>
          <div class="slip-row">
            <span class="label">Assigned room</span>
            <span class="value"><span class="triage-badge" style="--badge-color: var(--{result['room_class']})">{esc(result['room'])}</span></span>
          </div>
        </div>
        <div class="actions">
          <a href="/triage">Assign another room</a>
          <a href="/">Back to menu</a>
        </div>
        """
        return layout("Assign Triage Room", body)

    body = f"""
    <div class="page-intro">
      <h1>Assign Triage Room</h1>
      <p>Enter the severity of condition, from 1 (mild) to 10 (critical).</p>
    </div>
    <form method="post" action="/triage">
      {_field("severity", "Severity (1-10)", values.get("severity", ""), errors.get("severity"))}
      <button class="submit-btn" type="submit">Assign room</button>
    </form>
    """
    return layout("Assign Triage Room", body)


def not_found_page():
    body = """
    <div class="page-intro">
      <h1>Page not found</h1>
      <p>That page doesn't exist.</p>
    </div>
    <div class="actions"><a href="/">Back to menu</a></div>
    """
    return layout("Not found", body, back_link=False)
