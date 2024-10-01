from view import *

from model import *

class Controller:

    def show_applicant():
        applicants:Applicant = []
        response = View()
        response.view_applicants(applicants)
    
    def show_role_info(role):
        response = View()
        response.view_role(role)