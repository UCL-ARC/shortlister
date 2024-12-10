import argparse
import http
from http.server import HTTPServer
from pathlib import Path
from threading import Thread

from shortlister.controller import Controller

try:
    import webview
except ImportError:
    webview = None

# this creates an instance of parser
parser = argparse.ArgumentParser(description="loads shortlist data from role directory")

# creates some argument you can use when running the file
parser.add_argument("rolepath", type=Path)
parser.add_argument("-w", "--webview", action="store_true")

# set the value of the argument parsed in so it can be accessed later
cli_args = parser.parse_args()


def start_httpd():
    def serve_forever():
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory="/Users/tamuri/", **kwargs)

        httpd = HTTPServer(("localhost", 8000), Handler)
        httpd.serve_forever()

    http_thread = Thread(target=serve_forever)
    http_thread.daemon = True
    http_thread.start()


def run_controller(wv_window=None):
    if cli_args.rolepath.is_dir():
        if wv_window is not None:
            start_httpd()

        control = Controller(cli_args.rolepath, wv_window)
        control.run()
    else:
        print("ERROR: PATH DOES NOT EXIST")

    if wv_window is not None:
        wv_window.destroy()


if cli_args.webview and webview is not None:

    def on_closing():
        """Disable closing of the webview window"""
        return False

    window = webview.create_window("Shortlister", html="<h1>Shortlister<h1>")
    window.events.closing += on_closing
    webview.start(run_controller, args=[window])
else:
    run_controller(None)
