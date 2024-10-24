class View: 

    def __init__(self):
        return
    
    def boot_message(self,role,num_applicants):
        print(f"Shortlist for {role} loaded:")
        print(f"{num_applicants} applicants found")
        print("('?' to show list of avaliable shortcuts)")
    
    def view_role(self,role):
        print(f"Role title: {role.job_title}")
        print(f"Role ID: {role.job_id}")
        
    def view_applicant_details(self,applicant):
            print(f"Details for {applicant.name}: ")
            print(f"CV Path: {applicant.cv}")
            print(f"Scores: {applicant.scores}")

    def view_applicants_list(self,shortlist):
        for index, applicant in enumerate(shortlist.applicants):
            print(f"{index+1}. {applicant.name}")

    def view_criteria(self,role,criteria):
        print(f"The criteria for {role.job_title} are:")
        print()
        
        for criterion in criteria:
            i = criteria.index(criterion)
            print(f"{i+1}. {criterion.name}")
            print(f"{criterion.description}")
            print()
