import readline
import string
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List

from readchar import readkey
from startfile import startfile  # noqa - package name: universal-startfile

import shortlister.tournament as tournament
from shortlister.model import (RANK_AND_SCORE, Applicant, Criterion,  # noqa
                               InteractiveSorter, applicant_table, clear_score,
                               cv, load_shortlist, name, notes, rtw,
                               save_shortlist, score, sort_alpha,
                               sort_ascending_score, sort_descending_score,
                               update_applicant_notes, update_applicant_score)
from shortlister.view import View

try:
    import webview

    from shortlister.web import get_url_for_cv
except ImportError:
    webview = None
    get_url_for_cv = None


class ViewWidth(Enum):
    NARROW, WIDE = 1, 2

@dataclass
class Context:
    applicants: list[Applicant]  # selected applicants
    applicant_index: int  # selected applicant
    criterion: Criterion | None  # selected criterion to score
    table_view: ViewWidth  # selected applicants' table view

class Controller:

    def __init__(self, path, wv_window=None):
        self.path = path
        self.shortlist, msg = load_shortlist(path)
        print(msg)

        # basic setup
        self.view = View()
        self.options = None
        self.available_keys = string.digits + string.ascii_letters

        # application context
        self.ctx = Context(
            applicants=self.shortlist.applicants,
            applicant_index=0,
            criterion=None,
            table_view=ViewWidth.WIDE
        )

        # a window from pywebview to display PDFs
        self.wv_window = wv_window

        # add common filtering commands to readline history for easy access
        readline.add_history('score(applicant, "criterion-name", "score")')
        readline.add_history('cv(applicant, "regex")')
        readline.add_history('name(applicant, "name"')

        self.options_home = {
            "a": (self.show_applicants_table, "APPLICANTS"),
            "r": (self.show_role_info, "ROLE"),
            "R": (self.repl, "REPL"),
            "q": (self.quit, "QUIT"),
        }
        self.options_applicant_table = {
            "d": (self.show_applicant_details, "CHOOSE APPLICANT"),
            "s": (self.sort, "SORT"),
            "f": (self.filter_applicants, "FILTER"),
            "c": (self.clear_filter, "CLEAR FILTER"),
            "r": (self.rank_selected_applicants, "RANK"),
            "t": (self.show_applicants_table, "SWITCH TABLE"),
            "l": (self.show_table_legend, "LEGEND"),
            "a": (self.show_applicants_table, "APPLICANTS"),
            "q": (self.show_home_message, "HOME"),
        }
        self.options_sort = {
            "a": (self.sort, "ALPHABETICAL"),
            "s": (self.sort, "SCORE ASCENDING"),
            "d": (self.sort, "SCORE DESCENDING"),
            "c": (self.sort, "COMPARISON"),
        }
        self.options_applicant_detail = {
            "e": (self.score_applicant_step_1, "SCORE"),
            "N": (self.create_applicant_note, "NOTE"),
            "O": (self.open_applicant_pdf, "OPEN CV"),
            "n": (self.switch_applicant, "NEXT"),
            "p": (self.switch_applicant, "PREVIOUS"),
            "q": (self.show_applicants_table, "APPLICANTS"),
        }

    def repl(self, k=None):
        banner = "VARIABLES:\n  shortlist\n  controller"
        import code

        code.interact(
            banner=banner,
            local={"shortlist": self.shortlist, "controller": self},
            exitmsg="EXITING",
        )
        print()

    def quit(self, k=None):
        # if we've activated quit
        if k == "q":
            # ask for confirmation
            print("ARE YOU SURE?")
            self.options = {
                "n": (self.quit, "NO"),
                "y": (self.quit, "YES"),
            }
        elif k == "y":
            # quit confirmed - save and exit
            save_shortlist(self.path, self.shortlist)
            print("GOODBYE")
            print()
            return True
        else:
            # quit cancelled - back to home
            print("QUIT CANCELLED")
            print()
            self.options = self.options_home

    def show_home_message(self, k=None):
        """Display an overview of Shortlist."""
        self.view.home_message(self.path, len(self.shortlist.applicants))
        self.options = self.options_home

    def show_role_info(self, k=None):
        """Display role information."""
        self.view.view_role(self.shortlist.role)

    def show_applicant_details(self, k=None):
        """Select an applicant via input and view details."""
        try:
            i = int(input("№> "))
            print()
            self.ctx.applicant_index = i - 1  # Compensates for index
            self.view_applicant_details()
            self.options = self.options_applicant_detail
        except (ValueError, IndexError):
            pass

    def show_applicants_table(self, k=None):
        """Switches view only if already displaying applicants list or table"""

        # toggle the table view width, if requested
        if k == "t":
            if self.ctx.table_view == ViewWidth.WIDE:
                self.ctx.table_view = ViewWidth.NARROW
            else:
                self.ctx.table_view = ViewWidth.WIDE

        table = applicant_table(
            self.ctx.applicants,
            self.shortlist.role.criteria,
            "wide" if self.ctx.table_view == ViewWidth.WIDE else "narrow"
        )

        self.view.view_applicant_table(table)
        self.options = self.options_applicant_table

    def show_table_legend(self, k=None):
        self.view.view_table_legend(self.shortlist.role.criteria)

    def open_applicant_pdf(self, k=None):
        """Open selected applicant's CV in default viewer."""
        startfile(self.applicant(self.ctx.applicant_index).cv)

    def score_applicant_step_1(self, k=None):
        """Select a criteria to edit score for."""
        self.options = {
            str(self.available_keys[i]): (self.score_applicant_step_2, c.name)
            for i, c in enumerate(self.shortlist.role.criteria)
        }
        scored_criteria = [c.name for c in self.applicant(self.ctx.applicant_index).scores]
        self.view.view_criteria(self.options, scored_criteria)
        # press q to quit at next step
        self.options["q"] = (self.score_applicant_step_2, "APPLICANT")

    def score_applicant_step_2(self, k=None):
        """Select score for the selected criteria."""
        # return to applicant detail if key was "q", else continue to select criterion to score
        if k == "q":
            self.view_applicant_details()
            self.options = self.options_applicant_detail
        else:
            offset = self.available_keys.index(k)
            self.ctx.criterion = self.shortlist.role.criteria[offset]
            self.options = {
                str(i): (self.score_applicant_step_3, s)
                for i, s in enumerate(RANK_AND_SCORE)
            }
            self.options["c"] = (
                self.score_applicant_step_3,
                "CLEAR",
            )
            # returns to criterion selection
            self.options["q"] = (self.score_applicant_step_1, "CRITERION")
            self.view.view_selection_options(self.options)

    def score_applicant_step_3(self, k=None):
        """Updates the selected score of previously select criteria."""
        if k == "c":
            clear_score(self.applicant(self.ctx.applicant_index), self.ctx.criterion)
        else:
            update_applicant_score(
                self.applicant(self.ctx.applicant_index), self.ctx.criterion, int(k)
            )

        self.options = self.options_applicant_detail
        self.view_applicant_details()

    def switch_applicant(self, k=None):
        """Move to next or previous applicant"""

        # if next applicant, and not already at last
        if k == "n" and (self.ctx.applicant_index < len(self.ctx.applicants) - 1):
            self.ctx.applicant_index += 1
        # if previous and not already at first
        elif k == "p" and (self.ctx.applicant_index > 0):
            self.ctx.applicant_index -= 1
        # otherwise do nothing
        else:
            return

        self.view_applicant_details()

    def create_applicant_note(self, k=None):
        """Adds a new note to applicant's note section."""
        note = input("ADD NOTE> ")
        print()
        update_applicant_notes(self.applicant(self.ctx.applicant_index), note)
        self.view_applicant_details()

    def sort(self, k=None):
        """Activates sort"""
        if self.options != self.options_sort and k == "s":  # activate sort
            print("SORT> ", end="")
            self.options = self.options_sort
            self.print_options(self.options)
            return
        elif k == "a":
            sort_alpha(self.ctx.applicants)
        elif k == "s":
            sort_ascending_score(self.ctx.applicants)
        elif k == "d":
            sort_descending_score(self.ctx.applicants)
        elif k == "c":
            sorter = InteractiveSorter()

            print("FOR EACH PAIR, CHOOSE 1 OR 2")
            print()

            criteria = self.shortlist.role.criteria

            for first, second in sorter.sort(self.ctx.applicants):
                self.view.view_applicant_details(first, criteria, 1)
                self.view.view_applicant_details(second, criteria, 2)
                print("CHOICE> ", end="", flush=True)

                choice = None
                while choice not in ["1", "2"]:
                    choice = readkey()
                    if choice == "O":
                        startfile(first.cv)
                        startfile(second.cv)
                        choice = None  # user still needs to choose applicant
                    elif choice == "q":
                        print("CANCELED")
                        print()
                        self.show_applicants_table()
                        return

                if choice == "1":
                    sorter.selected = first
                elif choice == "2":
                    sorter.selected = second

                print(sorter.selected.name)
                print()

            result: List = sorter.sorted
            result.reverse()
            self.ctx.applicants = result
            print()

        self.show_applicants_table()

    def filter_applicants(self, k=None):
        """Allows user to filter applicants by with condition statement"""
        condition = input("FILTER> ")

        if condition == "?":
            self.view.view_filter_help()
            return

        try:
            selected_applicants = eval(
                f"[applicant for i, applicant in enumerate(self.shortlist.applicants) if {condition}]"
            )
        except (NameError, SyntaxError) as e:
            print(f"ERROR: {str(e).upper()}")
            print()
            return

        if selected_applicants:
            self.ctx.applicants = selected_applicants

            print()
            self.show_applicants_table()
        else:
            print("NO MATCHES")
        print()

    def clear_filter(self, k=None):
        self.ctx.applicants = self.shortlist.applicants
        self.show_applicants_table()

    def rank_selected_applicants(self, k=None):
        result = tournament.get_existing_result(
            Path(tournament.COMPARISON_RESULT_FILE_NAME)
        )
        result = tournament.comparison(self.ctx.applicants, result)

        ranked_list = tournament.rank(self.ctx.applicants, result)
        print("RESULT:", [applicant.name for applicant in ranked_list])
        print()

    # Utilities
    def applicant(self, index: int) -> Applicant:
        """Returns applicant using its index in applicants."""
        return self.ctx.applicants[index]

    def view_applicant_details(self):
        applicant: Applicant = self.applicant(self.ctx.applicant_index)
        applicant_number = self.ctx.applicant_index + 1
        self.view.view_applicant_details(applicant, self.shortlist.role.criteria, applicant_number)

        if self.wv_window is not None:
            path = self.applicant(self.ctx.applicant_index).cv
            url = get_url_for_cv(path.name)
            if self.wv_window.get_current_url() != url:
                self.wv_window.load_url(url)

    @staticmethod
    def print_options(options):
        # show available keypress options
        for keypress, func in options.items():
            print(f"{keypress}:{func[1]}  ", end="")
        print()
        print()

    def run(self):
        """Start the program and accepts keypress as argument for calling other functions."""
        self.view.title()
        self.show_home_message()

        while True:
            k = readkey()

            if k == "?":
                self.print_options(self.options)
            else:
                # get and execute the action for this keypress
                action = self.options.get(k)
                if action is not None:
                    quit_request = action[0](k=k)
                    if quit_request:
                        break
