from typing import Dict
from shortlister.view import View
from readchar import readkey
from shortlister.model import (
    Applicant,
    total_score,
    load_shortlist,
    save_shortlist,
    update_applicant_score,
    update_applicant_notes,
    clear_score,
    sort_alpha,
    sort_ascending_score,
    sort_descending_score
)
from startfile import startfile


class Controller:
    def __init__(self, path):
        self.path = path
        self.shortlist = load_shortlist(path)
        self.applicant_index: int = 0
        self.current_criterion = None
        self.view = View()
        self.options = None
        self.options_home = {"r": (self.show_role_info,"Show role information"), 
                             "a": (self.show_applicants_list,"List of applicants"),}
        self.options_sort = {"a": self.sort,
                             "s": self.sort,
                             "d": self.sort}
        self.options_applicant_list = {
            "b": (self.show_boot_message,"Home"),
            "S": self.sort,
            "d": (self.show_applicant_details,"Select an applicant to view their details"),
        }
        self.options_applicant_detail = {
            "a": (self.show_applicants_list,"Back to applicant list"),
            "n": (self.switch_next_applicant,"Next applicant"),
            "p": (self.switch_prev_applicant,"Previous applicant"),
            "e": (self.edit_score_start,"Edit score"),
            "N": (self.create_applicant_note,"New note"),
            "b": (self.show_boot_message,"Home"),
            "O": (self.open_applicant_pdf,"Open applicant's CV"),
        }

    def show_boot_message(self, k=None):
        """Display an overview of Shortlist."""
        self.view.boot_message(self.path, len(self.shortlist.applicants))
        self.options = self.options_home

    def show_criteria(self, k=None):
        """Display criteria information."""
        self.view.view_criteria(self.shortlist.role, self.shortlist.role.criteria)

    def show_role_info(self, k=None):
        """Display role information."""
        self.view.view_role(self.shortlist.role)

    def show_applicants_list(self, k=None):
        """List all applicants."""
        self.view.view_applicants_list(self.shortlist)
        self.options = self.options_applicant_list

    def show_applicant_details(self, k=None):
        """Select an applicant via input and view details."""
        try:
            i = int(input("Please enter the applicant number:"))
            print()
            self.applicant_index = i - 1  # Compensates for index
            self.view_applicant_details()
            self.options = self.options_applicant_detail
        except (ValueError, IndexError):
            pass

    def open_applicant_pdf(self, k=None):
        """Open selected applicant's CV."""
        startfile(self.applicant(self.applicant_index).cv)

    def edit_score_start(self, k=None):
        """select a criteria to edit score for."""
        self.view.view_criteria(self.shortlist.role, self.shortlist.role.criteria)
        self.options = {
            str(i): (self.edit_criteria_select,c.name)
            for i, c in enumerate(self.shortlist.role.criteria)
        }

    def edit_criteria_select(self, k=None):
        """Select score to change to for previously selected criteria."""
        self.current_criterion = self.shortlist.role.criteria[int(k)]
        self.view.view_selection_options(self.current_criterion)
        self.options = {
            str(i): (self.edit_score_confirm,s)
            for i, s in enumerate(self.current_criterion.scores)
        }
        self.options["c"] = (self.clear_score,f"Clear score: {self.current_criterion.name}")

    def edit_score_confirm(self, k=None):
        """Updates the selected score of previously select criteria."""
        self.view.view_update(
            self.current_criterion.name, self.current_criterion.scores[int(k)]
        )
        update_applicant_score(
            self.applicant(self.applicant_index), self.current_criterion, int(k)
        )

        self.view_applicant_details()
        self.options = self.options_applicant_detail

    def switch_prev_applicant(self, k=None):
        """Display details of the previous applicant in the shortlist."""

        # ignores input if already at first applicant
        if self.applicant_index > 0:
            self.applicant_index -= 1
        self.view_applicant_details()

    def switch_next_applicant(self, k=None):
        """Display details of the next applicant in the shortlist."""
        self.applicant_index += 1

        # loop back to the first applicant if at last applicant
        if self.applicant_index > len(self.shortlist.applicants) - 1:
            self.applicant_index = 0

        self.view_applicant_details()


    def create_applicant_note(self, k=None):
        """Adds a new note to applicant's note section."""
        note = input("New note: ")
        update_applicant_notes(self.applicant(self.applicant_index),note)
        self.view_applicant_details()

    def clear_score(self, k=None):
        clear_score(self.applicant(self.applicant_index),self.current_criterion)
        self.view_applicant_details()
        self.options = self.options_applicant_detail
    
        self.view_applicant_details()    
    
    def sort(self,k=None):
        """Activates sort"""
        if k == "S":  #activate sort
            print("Entering sorting mode")
            self.options = self.options_sort
            return
        elif k == "a":
            sort_alpha(self.shortlist.applicants)
        elif k == "s":
            sort_ascending_score(self.shortlist.applicants)
        elif k == "d":
            sort_descending_score(self.shortlist.applicants)
            
        self.show_applicants_list()
        

# Utilities
    def applicant(self, index:int) -> Applicant:
        """Returns applicant using its index in applicants."""
        return self.shortlist.applicants[index]
        
    def view_applicant_details(self):
        applicant:Applicant = self.applicant(self.applicant_index)
        total = total_score(applicant.scores)
        applicant_number = self.applicant_index + 1
        total_applicant = len(self.shortlist.applicants)
        self.view.view_applicant_details(applicant,self.shortlist.role.criteria,total,applicant_number,total_applicant)
    
    def run(self):
        """Start the program and accepts keypress as argument for calling other functions."""
        self.show_boot_message()

        while True:
            k = readkey()
            #print(k)

            if k == "q":
                save_shortlist(self.path, self.shortlist)
                print("\nexiting the program...")
                break

            if k == "?":
                print("\n---List of shortcuts---")
                print("q: Exit the program")

                for keypress, func in self.options.items():
                    print(f"{keypress}: {func[1]}")

            else:
                output = self.options.get(k)
                #print(type(output))
                
                if output is not None:
                    #print(output)
                    output[0](k=k)
