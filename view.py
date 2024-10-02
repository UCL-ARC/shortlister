
#view applicants
class View: 

    def __init__(self):
        return
    
    def view_role(self,role):
        print(f"The role is:{role}")

    def view_applicants(self,applicants):
        print(f"Here are all of the applicants:")
        print()

        for applicant in applicants:
          index = applicants.index(applicant)
          print(f"{index+1}.Name: {applicant.name}")
          print(f"CV Path: {applicant.cv}")
          print(f"Scores: {applicant.scores}")
          print()
    
    def view_shortlist(self,shortlist):
        print(shortlist)

    def view_criteria(self,criteria):
        print(f"The criteria for this role are:{criteria}")
