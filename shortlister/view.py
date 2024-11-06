from shortlister.model import Applicant,Role,Criterion,Shortlist
class View: 

    def __init__(self):
        return
    
    def boot_message(self,role,num_applicants):
        print(f"\nShortlist for {role} loaded:")
        print(f"{num_applicants} applicants found")
        print("('?' to show list of avaliable shortcuts)")
    
    def view_role(self,role:Role):
        print(f"\nRole title: {role.job_title}")
        print(f"Role ID: {role.job_id}")
        
    def view_applicant_details(self,applicant:Applicant):
        print(f"Details for {applicant.name}: ")
        print(f"CV Path: {applicant.cv}")
        print("Scores:")
        if applicant.scores is not None:
            for criterion,score in applicant.scores.items():
                print(f"{criterion.name:^20}: {score:^20}")
        print(f"Notes: {applicant.notes}\n")

    def view_applicants_list(self,shortlist:Shortlist):
        print("\nList of applicants:")
        for index, applicant in enumerate(shortlist.applicants):
            print(f"{index+1}. {applicant.name}")
        print()

    def view_criteria(self,role:Role,criteria:list[Criterion]):
        print(f"The criteria for {role.job_title} are:")
        print()
        
        for index,criterion in enumerate(criteria):
            print(f"{index}. {criterion.name}: {criterion.description}")

    def view_selection_options(self,criterion:Criterion):
        print(f"\nYou selected {criterion.name}. Select the score you want to change to:\n")

        for index,score in enumerate(criterion.scores):
                    print(f"{index}: {score}")

    def view_update(self,attribute,change):
        print(f"Updated: {attribute} to: {change}\n")