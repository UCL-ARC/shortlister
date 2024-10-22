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
        self.view = View()
        self.options = None # intial state
        self.options_home = {"r":self.show_role_info,
                            "a":self.show_applicants_list}
        self.options_applist = {"b":self.show_boot_message,
                                 "d":self.show_applicant_details}
        self.options_appdetail = {"a":self.show_applicants_list,
                                   "e":self.edit_applicant_score,
                                   "b":self.show_boot_message,
                                   "O":self.open_applicant_pdf}

    def edit_appscore_start(self,k=None):
        print("Select an criteria to edit score for:")
        self.options = None

    def edit_criteria_select(self, k=None):
        print("You selected A. Select more...")
        self.options = {
            "0": self.step3,
            "1": self.step3,
            "2": self.step3
        }

    def edit_criteria_quit(self, k=None):
        print(f"You selected B. Back to start...")
        self.options = self.step1_options

    def edit_score_select(self, k=None):
        print(f"You selected {k}. Back to start...")
        self.options = self.step1_options
    
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
        self.options = self.options_applist

    def show_applicant_details(self,k=None):
        """Select an applicant and view details"""
        try:
            i = int(input("Please enter the applicant number:"))

            self.current_applicant = self.shortlist.applicants[i-1]
            self.view.view_applicant_details(self.current_applicant)
            self.options = self.options_appdetail
        except (ValueError, IndexError):
            pass

    def open_applicant_pdf(self,k=None):
        """Open current applicant's CV"""
        startfile(self.current_applicant.cv)
        
    def edit_applicant_score(self,k=None):
        """View and score applicants based on criteria"""
        print("Select the criteria you would like to mark:")

        self.view.view_criteria(self.shortlist.role,self.shortlist.role.criteria) #prints out criteria
        options = [str(i) for i in range(len(self.shortlist.role.criteria))] #sets avaliable keypress based on how many criterions in the criteria 

        k = readkey() #gets the keypress (0,1,2,3.etc)

        #shows the select criterion that you would like mark(might move into view.py)
        print(f"{self.shortlist.role.criteria[int(k)].name} selected")

        if k in options: #checks if keypress is one of the avaliable options
            self.current_criterion = self.shortlist.role.criteria[int(k)] #sets the current criterion editing 
            for index,score in enumerate(self.current_criterion.scores): #prints list of avaliable scoring for the criterion
                print(f"{index}: {score}")

            scoring_options = [str(i) for i in range(len(self.current_criterion.scores))] #sets the list of avaliable key for scoring

            k = readkey() #gets keypress again
            print(k)
            if k in scoring_options: #checks if keypress is in avaliable options
                self.current_applicant.scores.update({self.current_criterion.name:self.current_criterion.scores[int(k)]}) #updates the score dictionary in applicant instance

                #shows the updated scores (might move into view.py)
                print(f"Updated score for {self.current_applicant.name}")
                print(self.current_applicant.scores)
            else:
                print("process aborted...")
        else:
            print("please press a valid key!")

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