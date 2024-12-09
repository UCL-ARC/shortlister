from shortlister.controller import Controller
import argparse
from pathlib import Path

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
args = parser.parse_args()


def run_controller(wv_window=None):
    if args.rolepath.is_dir():
        control = Controller(args.rolepath, wv_window)
        control.run()
    else:
        print("ERROR: PATH DOES NOT EXIST")

    if wv_window is not None:
        wv_window.destroy()


if args.webview and webview is not None:

    def on_closing():
        """Disable closing of the webview window"""
        return False

    window = webview.create_window('Shortlister', html='<h1>Shortlister<h1>')
    window.events.closing += on_closing
    webview.start(run_controller, args=[window])
else:
    run_controller(None)

