import urllib
from pathlib import Path
from threading import Thread

from flask import Flask, send_file, send_from_directory

ROUTE_PDFJS = "pdfjs"
ROUTE_CVS = "cvs"
ABS_PATH_PDFJS = "/Users/tamuri/Documents/2024/shiying-shortlister/pdfjs-4.6.82-dist/"
PDFJS_VIEWER_URL = f"http://127.0.0.1:8000/{ROUTE_PDFJS}/web/viewer.html"
CVS_URL = f"http://127.0.0.1:8000/{ROUTE_CVS}"


def get_url_for_cv(pdf_file):
    url = f"{CVS_URL}/{pdf_file}"
    url = urllib.parse.quote(url)
    url = f"{PDFJS_VIEWER_URL}?file={url}"
    return url


def start_httpd(role_path: Path):
    def serve_forever():
        app = Flask(__name__)

        @app.route(f"/{ROUTE_PDFJS}/<path:path>")
        def pdfjs(path):
            # Using request args for path will expose you to directory traversal attacks
            return send_from_directory(ABS_PATH_PDFJS, path)

        @app.route(f"/{ROUTE_CVS}/<file_name>")
        def get_pdf(file_name):
            return send_file(f"{role_path / file_name}", mimetype="application/pdf")

        app.run(host="0.0.0.0", port=8000, debug=False, use_reloader=False)

    http_thread = Thread(target=serve_forever)
    http_thread.daemon = True
    http_thread.start()
