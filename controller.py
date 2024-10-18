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
        self.current_view = "home"
        self.view = View()

    def show_boot_message(self):
        """Shortlist overview"""
        self.view.boot_message(self.path,len(self.shortlist.applicants))
        self.current_view = "home"

    def show_criteria(self):
        """Display criteria information"""
        self.view.view_criteria(self.shortlist.role,self.shortlist.role.criteria)
        self.current_view = "criteria"

    def show_role_info(self):
        """Display role information"""
        self.view.view_role(self.shortlist.role)
        self.current_view = "role"

    def show_applicants_list(self):
        """List all applicants"""
        self.view.view_applicants_list(self.shortlist)
        self.current_view = "applicants_list"

    def show_applicant_details(self):
        """Select an applicant and view details"""
        try:
            i = int(input("Please enter the applicant number:"))

            self.current_applicant = self.shortlist.applicants[i-1]
            self.view.view_applicant_details(self.current_applicant)
            self.current_view = "applicant_details"
        except (ValueError, IndexError):
            pass

    def open_applicant_pdf(self):
        """Open current applicant's CV"""
        startfile(self.current_applicant.cv)
        
    def edit_applicant_score(self):
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

            elif self.current_view == "home":
                options = {"r":self.show_role_info,
                           "a":self.show_applicants_list}
                
            elif self.current_view == "applicants_list":
                options = {"b":self.show_boot_message,
                           "d":self.show_applicant_details}
                
            elif self.current_view == "applicant_details":
                options = {"a":self.show_applicants_list,
                           "e":self.edit_applicant_score,
                           "b":self.show_boot_message,
                           "O":self.open_applicant_pdf}

            elif self.current_view == "role":
                options = {"b":self.show_boot_message}
                
            elif self.current_view == "criteria":
                options = {"b":self.show_boot_message}
            
            if options is not None:
                output = options.get(k)
                if k == "?":
                    print("---List of shortcuts---")
                    print("q: Exit the program")
                    for keypress,func in options.items():
                        print(f"{keypress}: {func.__doc__}")
                elif output is not None:
                    output()