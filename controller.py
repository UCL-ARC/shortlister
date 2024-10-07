from view import View
from readchar import readkey, key
from model import load_shortlist

class Controller:

    def __init__(self,path):
        self.path = path
        self.shortlist = load_shortlist(path)
        self.current_view = "home"
        self.view = View()

    def show_boot_message(self):
        self.view.boot_message(self.path,len(self.shortlist.applicants))
        self.current_view = "home"

    def show_applicants(self):
        self.view.view_applicants(self.shortlist.applicants)
        self.current_view = "applicants"

    def show_criteria(self):
        self.view.view_criteria(self.shortlist.role,self.shortlist.role.criteria)
        self.current_view = "criteria"

    def show_role_info(self):
        self.view.view_role(self.shortlist.role)
        self.current_view = "role"

    def show_shortlist(self):
        self.view.view_shortlist(self.shortlist)
        self.current_view = "shortlist"

    def run(self):

        self.show_boot_message()

        while True:
            k = readkey()

            if self.current_view == "home":
                options = {"b":self.show_boot_message,
                           "r":self.show_role_info,
                           "s":self.show_shortlist}
                
                output = options.get(k)
                if output is not None:
                    output()
                if k == key.ESC:
                    print("exiting the program...")
                    break
                
            if self.current_view == "shortlist":
                options = {"a":self.show_applicants,
                           "b":self.show_boot_message,
                           "c":self.show_criteria,
                           "r":self.show_role_info,
                           "s":self.show_shortlist
                           }
                
                output = options.get(k)
                if output is not None:
                    output()
                if k == key.ESC:
                    print("exiting the program...")
                    break
            
            if self.current_view == "criteria":
                options = {"b":self.show_shortlist}

                output = options.get(k)
                if output is not None:
                    output()

                if k == key.ESC:
                    print("exiting the program...")
                    break


""" bug """
# shortcuts for criteria does not limit to only "b"
# need to recheck current view

"""view"""

# home(default boot-up view) 
# > "s" to shortlist view
# > "h" for list of shortcut commands

# shortlist ()
# > "a" for list of applicants and their infos
# > "c" for criteria
# > "r" for role info and id
# > "h" for list of shortcut commands

