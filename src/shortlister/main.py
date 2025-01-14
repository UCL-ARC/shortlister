import argparse
from pathlib import Path

from src.shortlister.controller import Controller
from src.shortlister.web import start_httpd, setup_webview

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


def run_controller(wv_window: webview.Window=None): # type: ignore
    if cli_args.rolepath.is_dir():
        if wv_window is not None:
            start_httpd(cli_args.rolepath)

        control = Controller(cli_args.rolepath, wv_window)
        control.run()
    else:
        print("ERROR: PATH DOES NOT EXIST")

    if wv_window is not None:
        wv_window.destroy()


if cli_args.webview and webview is not None:
    window = setup_webview()
    webview.start(run_controller, args=[window])
else:
    run_controller(None)
