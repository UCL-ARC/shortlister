"""
Functions to work with pywebview and pdf.js to present applicant CVs. This
is an optional feature, and can be activated with the "-w" option when starting
shortlister.
"""
import urllib
from pathlib import Path
from threading import Thread

import webview
from flask import Flask, send_file, send_from_directory

from shortlister.view import BANNER

ORIGIN = "http://localhost:8000"
ROUTE_PDFJS = "pdfjs"
ROUTE_CVS = "cvs"
ABS_PATH_PDFJS = "../pdfjs-4.6.82-dist/"
PDFJS_VIEWER_URL = f"{ORIGIN}/{ROUTE_PDFJS}/web/viewer.html"
CVS_URL = f"{ORIGIN}/{ROUTE_CVS}"

BANNER_HTML = f"""
<html>
  <head><style>body {{background-color: #e6e6e6}}</style></head>
  <body><pre>{BANNER}</pre></body>
</html>
"""


def setup_webview():
    """Create the pywebview window(s) for displaying applicant information.
    We disable closing the window using window decorations/CMD+q etc.
    Exiting the application in the terminal will close the window."""
    window = webview.create_window("shortlister", html=BANNER_HTML)
    window.events.closing += lambda: False
    return window


def get_url_for_cv(pdf_filename):
    """Return the URL for the pdf.js viewer and supplied PDF file"""
    pdf_url = f"{CVS_URL}/{pdf_filename}"
    pdf_url = urllib.parse.quote(pdf_url)
    viewer_url = f"{PDFJS_VIEWER_URL}?file={pdf_url}"
    return viewer_url


def start_httpd(path_to_pdfs: Path):
    """Start a Flask server to serve pdf.js and PDF files for pywebview.
    We use Flask instead of Python's built-in http.server because we want
    route pdf.js and applicant CVs to different paths."""
    def serve_forever():
        app = Flask(__name__)

        @app.route("/")
        def index():
            return BANNER_HTML

        @app.route(f"/{ROUTE_PDFJS}/<path:path>")
        def pdfjs(path):
            return send_from_directory(ABS_PATH_PDFJS, path)

        @app.route(f"/{ROUTE_CVS}/<file_name>")
        def get_pdf(file_name):
            return send_file(f"{path_to_pdfs / file_name}", mimetype="application/pdf")

        app.run(host="0.0.0.0", port=8000, debug=False, use_reloader=False)

    http_thread = Thread(target=serve_forever)
    http_thread.daemon = True
    http_thread.start()
