from view import View
from readchar import readkey
from model import load_shortlist
from startfile import startfile

class Controller:

    def __init__(self,path):
        self.path = path
        self.shortlist = load_shortlist(path)
        self.current_applicant = None
        self.current_criterion = None
        self.current_score = None
        self.view = View()
        self.options = None # intial state
        self.options_home = {"r":self.show_role_info,
                             "a":self.show_applicants_list}
        self.options_applicant_list = {"b":self.show_boot_message,
                                       "d":self.show_applicant_details}
        self.options_applicant_detail = {"a":self.show_applicants_list,
                                         "e":self.edit_score_start,
                                         "b":self.show_boot_message,
                                         "O":self.open_applicant_pdf}

    def show_boot_message(self,k=None):
        """Shortlist overview"""
        self.view.boot_message(self.path,len(self.shortlist.applicants))
        self.options = self.options_home

    def show_criteria(self,k=None):
        """Display criteria information"""
        self.view.view_criteria(self.shortlist.role,self.shortlist.role.criteria)

    def show_role_info(self,k=None):
        """Display role information"""
        self.view.view_role(self.shortlist.role)

    def show_applicants_list(self,k=None):
        """List all applicants"""
        self.view.view_applicants_list(self.shortlist)
        self.options = self.options_applicant_list

    def show_applicant_details(self,k=None):
        """Select an applicant and view details"""
        try:
            i = int(input("Please enter the applicant number:"))

            self.current_applicant = self.shortlist.applicants[i-1]
            self.view.view_applicant_details(self.current_applicant)
            self.options = self.options_applicant_detail
        except (ValueError, IndexError):
            pass

    def open_applicant_pdf(self,k=None):
        """Open current applicant's CV"""
        startfile(self.current_applicant.cv)

    def edit_score_start(self,k=None):
        """select a criteria to edit score for"""
        self.view.view_criteria(self.shortlist.role,self.shortlist.role.criteria)
        self.options = {str(i):self.edit_criteria_select for i, _ in enumerate(self.shortlist.role.criteria)} 
        #generate options based on how many criteria there are
        #if a criteria number is selected, call the next function

    def edit_criteria_select(self, k=None):
        self.current_criterion = self.shortlist.role.criteria[int(k)]
        
        print(f"You selected {self.current_criterion.name}. Select the score you want to edit")
        self.options = {str(i):self.edit_score_confirm for i, _ in enumerate(self.current_criterion.scores)}
        
        for index,score in enumerate(self.current_criterion.scores):
                print(f"{index}: {score}")
        
        self.current_score = self.current_criterion.scores[int(k)]

    def edit_score_confirm(self,k=None):
        """Confirm changes to score"""
        print(f"Updated score: {self.current_criterion.name}:{self.current_score} and back to (applicant details)...")
        
        self.current_applicant.scores[self.current_criterion] = self.current_score
        self.view.view_applicant_details(self.current_applicant)
        self.options = self.options_applicant_detail

    def run(self):

        self.show_boot_message()

        while True:
            k = readkey()

            if k == "q":
                print("exiting the program...")
                break

            if k == "?":
                print("---List of shortcuts---")
                print("q: Exit the program")

                for keypress,func in self.options.items():
                    print(f"{keypress}: {func.__doc__}")
            
            else :
                output = self.options.get(k)

                if output is not None:
                    output(k=k)