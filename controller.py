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
    
    def show_role_info(self):
        self.view.view_role(self.shortlist.role)

    def show_shortlist(self):
        self.view.view_shortlist(self.shortlist)

"""job = Role("employee","18230123",[])
view = View()"""
control = Controller("test_role")

#control.show_role_info(view,job)
#control.show_shortlist()
control.show_role_info()