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
            print(f"Scores:",end=" ") 
            if applicant.scores is not None:
                for criterion,score in applicant.scores.items():
                    print(f"{criterion.name}: {score}")
            print()

    def view_applicants_list(self,shortlist):
        for index, applicant in enumerate(shortlist.applicants):
            print(f"{index+1}. {applicant.name}")

    def view_criteria(self,role,criteria):
        print(f"The criteria for {role.job_title} are:")
        print()
        
        for index,criterion in enumerate(criteria):
            print(f"{index}. {criterion.name}: {criterion.description}")
