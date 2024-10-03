from view import *

from model import *

class Controller:

    def __init__(self,path):
        self.shortlist = load_shortlist(path)
        self.applicants = load_applicants(path)
        self.view = View()

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

control = Controller("test_role")