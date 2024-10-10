class View: 

    def __init__(self):
        return
    
    def boot_message(self,role,num_applicants):
        print(f"Shortlist for {role} loaded:")
        print(f"{num_applicants} applicants found")
    
    def view_role(self,role):
        print(f"Role title: {role.job_title}")
        print(f"Role ID: {role.job_id}")
        
    def view_applicant_details(self,applicants):
        i = int(input("Please enter the applicant number:"))
        while i-1 > len(applicants):
            i = int(input("Please enter a valid applicant number:"))
        else:
            applicant = applicants[i-1]
            print(f"Details for {applicant.name}: ")
            print(f"CV Path: {applicant.cv}")
            print(f"Scores: {applicant.scores}")

    def view_applicants_list(self,shortlist):
        print(f"List of applicants for {shortlist.role.job_title}:")

        for applicant in shortlist.applicants:
            i = shortlist.applicants.index(applicant)
            print(f"{i+1}. {applicant.name}")

    def view_criteria(self,role,criteria):
        print(f"The criteria for {role.job_title} are:")
        print()
        

        for criterion in criteria:
            i = criteria.index(criterion)
            print(f"{i+1}. {criterion.name}")
            print(f"{criterion.description}")
            print()
