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

    def show_criteria(self):
        self.view.view_criteria(self.shortlist.role,self.shortlist.role.criteria)
        self.current_view = "criteria"

    def show_role_info(self):
        self.view.view_role(self.shortlist.role)
        self.current_view = "role"

    def show_applicants_list(self):
        self.view.view_applicants_list(self.shortlist)
        self.current_view = "applicants_list"

    def show_applicant_details(self):
        try:
            i = int(input("Please enter the applicant number:"))
            self.view.view_applicant_details(self.shortlist.applicants[i-1])
            self.current_view = "applicant_details"
        except (ValueError, IndexError):
            pass
    

    def run(self):

        self.show_boot_message()

        while True:
            k = readkey()

            if self.current_view == "home":
                options = {"r":self.show_role_info,
                           "a":self.show_applicants_list}
                
                output = options.get(k)
                if output is not None:
                    output()
                if k == key.ESC:
                    print("exiting the program...")
                    break
                
            elif self.current_view == "applicants_list":
                options = {"b":self.show_boot_message,
                           "d":self.show_applicant_details}
                
                output = options.get(k)
                if output is not None:
                    output()
                if k == key.ESC:
                    print("exiting the program...")
                    break
            
            elif self.current_view == "applicant_details":
                options = {"q":self.show_applicants_list,
                           "b":self.show_boot_message}

                output = options.get(k)
                if output is not None:
                    output()

                if k == key.ESC:
                    print("exiting the program...")
                    break

            elif self.current_view == "role":
                options = {"b":self.show_boot_message}

                output = options.get(k)
                if output is not None:
                    output()

                if k == key.ESC:
                    print("exiting the program...")
                    break

            elif self.current_view == "criteria":
                options = {"b":self.show_boot_message}

                output = options.get(k)
                if output is not None:
                    output()

                if k == key.ESC:
                    print("exiting the program...")
                    break

"""view"""

# home(default boot-up view) 
# > "s" to shortlist view
# > "h" for list of shortcut commands

# applicant_list
# shows only number and name

# > "a" for list of applicants and their infos
# > "c" for criteria
# > "r" for role info and id
# > "h" for list of shortcut commands

