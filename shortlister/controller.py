import string
from pathlib import Path
import sys
from typing import List

from shortlister.view import View
from shortlister.model import (
    Applicant,
    total_score,
    load_shortlist,
    save_shortlist,
    update_applicant_score,
    update_applicant_notes,
    clear_score,
    RANK_AND_SCORE,
    sort_alpha,
    sort_ascending_score,
    sort_descending_score,
    name,
    score,
    rtw,
    cv,
    notes,

)

from shortlister.tournament import comparison,rank,get_existing_result,COMPARISON_RESULT_FILE_NAME
from readchar import readkey
from startfile import startfile


class Controller:
    def __init__(self, path):
        self.path = path
        self.shortlist = load_shortlist(path)
        self.applicant_index: int = 0
        self.current_criterion = None
        self.current_applicant_view = "Table"
        self.selected_applicants = self.shortlist.applicants
        self.view = View()
        self.options = None
        self.available_keys = string.digits + string.ascii_letters

        self.options_home = {
            "a": (self.show_applicants_list_table, "APPLICANTS"),
            "r": (self.show_role_info, "ROLE"),
            "R": (self.repl, "REPL"),
            "q": (self.quit, "QUIT"),
        }
        self.options_applicant_list = {
            "d": (self.show_applicant_details, "CHOOSE APPLICANT"),
            "s": (self.sort, "SORT"),
            "f": (self.filter_applicants,"FILTER"),
            "c": (self.clear_filter,"CLEAR FILTER"),
            "t": (self.show_applicants_list_table, "SWITCH TABLE"),
            "r": (self.rank_selected_applicants,"RANK"),
            "q": (self.show_home_message, "HOME"),
        }
        self.options_sort = {
            "a": (self.sort, "ALPHABETICAL"),
            "s": (self.sort, "SCORE ASCENDING"),
            "d": (self.sort, "SCORE DESCENDING"),
        }
        self.options_applicant_detail = {
            "e": (self.edit_score_start, "SCORE"),
            "N": (self.create_applicant_note, "NOTE"),
            "O": (self.open_applicant_pdf, "OPEN CV"),
            "n": (self.switch_applicant, "NEXT"),
            "p": (self.switch_applicant, "PREVIOUS"),
            "q": (self.show_applicants_list_table, "APPLICANTS"),
        }

    def repl(self, k=None):
        banner = "VARIABLES:\n  shortlist\n  controller"
        import code
        code.interact(banner=banner, local={"shortlist": self.shortlist, "controller": self}, exitmsg="EXITING")
        print()

    def quit(self, k=None):
        # if we've activated quit
        if k == "q":
            # ask for confirmation
            print("ARE YOU SURE?")
            print()
            self.options = {
                "n": (self.quit, "NO"),
                "y": (self.quit, "YES"),
            }
        elif k == "y":
            # quit confirmed - save and exit
            save_shortlist(self.path, self.shortlist)
            print("GOODBYE.")
            sys.exit(0)
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

    def show_applicants(self):
        """Show applicants in either list or table view."""
        if self.current_applicant_view == "List":
            self.view.view_applicants_list(self.selected_applicants)
        else:
            self.view.view_applicant_table(self.selected_applicants,self.shortlist.role.criteria)

    def show_applicant_details(self, k=None):
        """Select an applicant via input and view details."""
        try:
            i = int(input("№> "))
            print()
            self.applicant_index = i - 1  # Compensates for index
            self.view_applicant_details()
            self.options = self.options_applicant_detail
        except (ValueError, IndexError):
            pass

    def switch_applicants_list_table(self):
        """Switch between list and table view of applicants"""
        if self.current_applicant_view == "List":
            # switch to table view if already displaying applicant list
            self.current_applicant_view = "Table"
        else:
            # display applicant list if the above doesn't apply
            self.current_applicant_view = "List"

    def show_applicants_list_table(self,k=None):
        """Switches view only if already displaying applicants list or table"""
        if k == "t":
            self.switch_applicants_list_table()
        self.show_applicants()
        self.options = self.options_applicant_list

    def open_applicant_pdf(self, k=None):
        """Open selected applicant's CV."""
        startfile(self.applicant(self.applicant_index).cv)

    def edit_score_start(self, k=None):
        """select a criteria to edit score for."""

        self.options = {
            str(self.available_keys[i]): (self.edit_criteria_select, c.name)
            for i, c in enumerate(self.shortlist.role.criteria)
        }
        scored_criteria = [c.name for c in self.applicant(self.applicant_index).scores]
        self.view.view_criteria(self.options, scored_criteria)
        # press q to quit at next step
        self.options["q"] = (self.edit_criteria_select, "APPLICANT")

    def edit_criteria_select(self, k=None):
        """Select score to change to for previously selected criteria."""
        # return to applicant detail if key was "q", else continue to select criterion to score
        if k == "q":
            self.view_applicant_details()
            self.options = self.options_applicant_detail
        else:
            offset = self.available_keys.index(k)
            self.current_criterion = self.shortlist.role.criteria[offset]
            self.options = {
                str(i): (self.edit_score_confirm, s) for i, s in enumerate(RANK_AND_SCORE)
            }
            self.options["c"] = (
                self.clear_score,
                "CLEAR",
            )
            # returns to criterion selection
            self.options["q"] = (self.edit_score_start, "CRITERION")
            self.view.view_selection_options(self.current_criterion,self.options)

    def edit_score_confirm(self, k=None):
        """Updates the selected score of previously select criteria."""
        update_applicant_score(
            self.applicant(self.applicant_index), self.current_criterion, int(k)
        )

        self.options = self.options_applicant_detail
        self.view_applicant_details()

    def switch_applicant(self, k=None):
        """Move to next or previous applicant"""

        # if next applicant, and not already at last
        if k == "n" and (self.applicant_index < len(self.selected_applicants) - 1):
            self.applicant_index += 1
        # if previous and not already at first
        elif k == "p" and (self.applicant_index > 0):
            self.applicant_index -= 1
        # otherwise do nothing
        else:
            return

        self.view_applicant_details()

    def create_applicant_note(self, k=None):
        """Adds a new note to applicant's note section."""
        note = input("ADD NOTE> ")
        print()
        update_applicant_notes(self.applicant(self.applicant_index), note)
        self.view_applicant_details()

    def clear_score(self, k=None):
        clear_score(self.applicant(self.applicant_index), self.current_criterion)
        self.options = self.options_applicant_detail
        self.view_applicant_details()

    def sort(self, k=None):
        """Activates sort"""
        if k == "s":  # activate sort
            print("SORT> ", end="")
            self.options = self.options_sort
            self.print_options(self.options)
            return
        elif k == "a":
            sort_alpha(self.selected_applicants)
        elif k == "s":
            sort_ascending_score(self.selected_applicants)
        elif k == "d":
            sort_descending_score(self.selected_applicants)

        self.show_applicants_list_table()

    def filter_applicants(self,k=None):
        """Allows user to filter applicants by with condition statement"""
        filter = input("FILTER> ")

        try:
            selected_applicants = eval(f"[applicant for applicant in self.shortlist.applicants if {filter}]")
        except Exception as e:
            print(f"ERROR: {str(e).upper()}")
            print()
            return
        
        if selected_applicants:
            self.selected_applicants = selected_applicants

            print()
            self.show_applicants_list_table()
        else:
            print("NO MATCHES")
        print()
    
    def clear_filter(self,k=None):
        self.selected_applicants = self.shortlist.applicants
        self.show_applicants_list_table()

    def rank_selected_applicants(self,k=None):

        result = get_existing_result(Path(COMPARISON_RESULT_FILE_NAME))
            
        comparison(self.selected_applicants,result)
        ranked_list = rank(self.selected_applicants,result)
        print([applicant.name for applicant in ranked_list])

    # Utilities
    def applicant(self, index: int) -> Applicant:
        """Returns applicant using its index in applicants."""
        return self.selected_applicants[index]

    def view_applicant_details(self):
        applicant: Applicant = self.applicant(self.applicant_index)
        total = total_score(applicant.scores)
        applicant_number = self.applicant_index + 1
        total_applicant = len(self.selected_applicants)
        self.view.view_applicant_details(
            applicant,
            self.shortlist.role.criteria,
            total,
            applicant_number,
            total_applicant,
        )

    def print_options(self, options):
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
                    action[0](k=k)
