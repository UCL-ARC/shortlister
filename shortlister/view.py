from shortlister.model import (
    Applicant,
    Role,
    Criterion,
    Shortlist,
    tab,
    abbreviate,
    RANK_AND_SCORE,
)
from tabulate import tabulate
import pydoc
from typing import List


class View:
    def __init__(self):
        return

    def title(self):
        print("""
     _                _   _ _     _            
 ___| |__   ___  _ __| |_| (_)___| |_ ___ _ __ 
/ __| '_ \ / _ \| '__| __| | / __| __/ _ \ '__|
\__ \ | | | (_) | |  | |_| | \__ \ ||  __/ |   
|___/_| |_|\___/|_|   \__|_|_|___/\__\___|_|

""")

    def home_message(self, role, num_applicants):
        """Prints overview of shortlist to console."""
        print(f"Shortlist for {role} loaded:")
        print(f"{num_applicants} applicants found")
        print("('?' to show list of avaliable shortcuts)")
        print()

    def view_role(self, role: Role):
        """Prints overview of role to console."""
        print(f"Role title: {role.job_title}")
        print(f"Role ID: {role.job_id}")
        print()

    def view_applicant_details(
        self,
        applicant: Applicant,
        criteria: List[Criterion],
        total_score,
        applicant_number,
        total_applicant,
    ):
        """Prints details of applicant to console."""
        print(f"** {applicant_number}/{total_applicant} {applicant.name} **")
        print(f"CV Path: {applicant.cv}")

        if applicant.scores:
            print(f"Scores: ({total_score})")
            for order in criteria:
                if order in applicant.scores:
                    print(f"{order.name:^20}: {applicant.scores[order]:^20}")
        else:
            print("No scores")

        if applicant.notes:
            print(f"Notes: {applicant.notes}")

        print()

    def view_applicants_list(self, shortlist: Shortlist):
        """Prints list of all applicants to console."""
        for index, applicant in enumerate(shortlist.applicants):
            print(f"{index+1}. {applicant.name}")
        print()

    def view_applicant_table(self, applicants:List[Applicant], criteria:List[Criterion]):
        """Prints a table summary of applicants and their scores"""

        # creates heading
        criteria_headings = abbreviate(
            [criterion.name for criterion in criteria]
        )
        header = ["No.", "Name"] + criteria_headings

        # creates applicant and score data
        applicant_data = tab(applicants, criteria)

        # displays table
        pydoc.pager(tabulate(applicant_data, headers=header))

    def view_criteria(self, role: Role, criteria: list[Criterion]):
        """Prints list of all criterion for the role to console."""
        print(f"The criteria for {role.job_title} are:")
        print()

        for index, criterion in enumerate(criteria):
            print(f"{index}. {criterion.name}: {criterion.description}")

    def view_selection_options(
        self,
        criterion: Criterion,
    ):
        """Prints list of avaliable scoring option for selected criterion to console."""
        print(
            f"You selected {criterion.name}. Select the score you want to change to:\n"
        )

        for index, score in enumerate(RANK_AND_SCORE.keys()):
            print(f"{index}: {score}")
        print("c: Clear scores\n")
        print()

    def view_update(self, attribute, change):
        print(f"Updated: {attribute} to: {change}\n")
        print()
