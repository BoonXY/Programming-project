# CareBridge Hospital — Web Front End

A web front end for the CareBridge console prototype. Same four functions,
same validation rules, same calculations — now served as web pages instead
of a terminal menu.

## Run it

No installation needed — it only uses Python's standard library.

```
python3 app.py
```

Then open **http://localhost:8000** in a browser.

## How it's put together

- **`hospital_logic.py`** — the business rules (validation + calculations).
  Same constants and same rules as the console version, just rewritten as
  functions that take a value in and return `(is_valid, errors, result)`
  instead of using `input()`/`print()`.
- **`templates.py`** — builds the HTML for each page (menu, the four forms,
  and their confirmation screens).
- **`app.py`** — the web server. It reads the incoming request, calls the
  matching function in `hospital_logic.py`, and asks `templates.py` to
  render either the form again (with error messages) or a confirmation
  screen.
- **`static/style.css`** — the page styling.

## Why no Flask

This is built with Python's built-in `http.server` module only, so there's
nothing to `pip install` — which keeps the next step (Docker) simple, since
the image won't need a `requirements.txt` or a package install layer.
