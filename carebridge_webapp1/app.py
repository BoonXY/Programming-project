

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

import hospital_logic as logic
import templates


HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8000))
STATIC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "static"
)


class Handler(BaseHTTPRequestHandler):
    server_version = "CareBridge/1.0"

    # -- small helpers --------------------------------------------------

    def _send_html(self, html_str, status=200):
        body = html_str.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def _send_file(self, path, content_type):
        try:
            with open(path, "rb") as f:
                data = f.read()
        except OSError:
            self._send_html(
                templates.not_found_page(),
                status=404
            )
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        self.wfile.write(data)

    def _read_form(self):
        length = int(self.headers.get("Content-Length", 0))

        raw = (
            self.rfile.read(length).decode("utf-8")
            if length
            else ""
        )

        parsed = parse_qs(raw, keep_blank_values=True)

        return {
            key: values[0]
            for key, values in parsed.items()
        }

    # -- routing --------------------------------------------------------

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            self._send_html(templates.menu_page())

        elif path == "/static/style.css":
            self._send_file(
                os.path.join(STATIC_DIR, "style.css"),
                "text/css; charset=utf-8"
            )

        elif path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()

        elif path == "/register":
            self._send_html(templates.register_page())

        elif path == "/appointment":
            self._send_html(templates.appointment_page())

        elif path == "/bill":
            self._send_html(templates.bill_page())

        elif path == "/triage":
            self._send_html(templates.triage_page())

        else:
            self._send_html(
                templates.not_found_page(),
                status=404
            )

    def do_POST(self):
        path = urlparse(self.path).path
        form = self._read_form()

        if path == "/register":
            ok, errors, data = logic.validate_patient(
                form.get("name"),
                form.get("age"),
                form.get("patient_id")
            )

            self._send_html(
                templates.register_page(
                    values=form,
                    errors=errors,
                    result=data if ok else None
                )
            )

        elif path == "/appointment":
            ok, errors, data = logic.validate_appointment(
                form.get("department"),
                form.get("date")
            )

            self._send_html(
                templates.appointment_page(
                    values=form,
                    errors=errors,
                    result=data if ok else None
                )
            )

        elif path == "/bill":
            ok, errors, data = logic.validate_bill(
                form.get("patient_type"),
                form.get("num_tests")
            )

            self._send_html(
                templates.bill_page(
                    values=form,
                    errors=errors,
                    result=data if ok else None
                )
            )

        elif path == "/triage":
            ok, errors, data = logic.validate_triage(
                form.get("severity")
            )

            self._send_html(
                templates.triage_page(
                    values=form,
                    errors=errors,
                    result=data if ok else None
                )
            )

        else:
            self._send_html(
                templates.not_found_page(),
                status=404
            )

    def log_message(self, format, *args):
        # Keep console output quiet.
        # Remove this override if you want request logs.
        pass


def main():
    server = ThreadingHTTPServer(
        (HOST, PORT),
        Handler
    )

    print(
        f"CareBridge web front end running at "
        f"http://localhost:{PORT}"
    )
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()