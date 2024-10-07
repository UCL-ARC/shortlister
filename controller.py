from view import View
from readchar import readkey, key
from model import load_shortlist,load_applicants

class Controller:

    def __init__(self,path):
        self.path = path
        self.shortlist = load_shortlist(path)
        self.applicants = load_applicants(path)
        self.view = View()

    def show_boot_message(self):
        self.view.boot_message(self.path,len(self.shortlist.applicants))

    def show_applicant_info(self):
        self.view.view_applicants(self.shortlist.applicants)
    
    def show_applicants(self):
        self.view.view_applicants(self.applicants)

    def show_criteria(self):
        self.view.view_criteria(self.shortlist.role,self.shortlist.role.criteria)
    
    def show_role_info(self):
        self.view.view_role(self.shortlist.role)

    def show_shortlist(self):
        self.view.view_shortlist(self.shortlist)

    def run(self):
        self.show_boot_message()

        while True:
            options = {"a":self.show_applicants,
                       "b":self.show_boot_message,
                       "c":self.show_criteria,
                       "r":self.show_role_info,
                       "s":self.show_shortlist,} 

            k = readkey()
            output = options.get(k)
            if output is not None:
                output()
            if k == "o":
                print("(´⊙ω⊙`)!")
            if k == key.CTRL_U:
                print("ctrl u")
            if k == key.ESC:
                print("exiting the program...")
                break
