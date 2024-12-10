from shortlister.model import (
    Applicant,
    Role,
    Criterion,
    Shortlist,
    applicant_table,
    abbreviate,
)
from tabulate import tabulate
import pydoc
from typing import Dict, List

BANNER = r"""
     _                _   _ _     _            
 ___| |__   ___  _ __| |_| (_)___| |_ ___ _ __ 
/ __| '_ \ / _ \| '__| __| | / __| __/ _ \ '__|
\__ \ | | | (_) | |  | |_| | \__ \ ||  __/ |   
|___/_| |_|\___/|_|   \__|_|_|___/\__\___|_|

"""

class View:
    def __init__(self):
        return

    def title(self):
        print(BANNER)

    def home_message(self, role, num_applicants):
        """Prints overview of shortlist to console."""
        print(f"PATH: {role}")
        print(f"APPLICANTS: {num_applicants}")
        print("? FOR HELP")
        print()

    def view_role(self, role: Role):
        """Prints overview of role to console."""
        print(f"PATH: {role.job_title}")
        print(f"  ID: {role.job_id}")
        print()

    def view_applicant_details(self, applicant: Applicant, criteria: List[Criterion], applicant_number):
        """Prints details of applicant to console."""
        print(f"{applicant_number: >2}  {applicant.name}")
        if not applicant.right_to_work:
            print(f"    RIGHT TO WORK: NO ({applicant.visa_requirement})")

        if applicant.notes:
            print(f"    NOTES: {applicant.notes}")

        if applicant.scores:
            print("    SCORES:")
            for order in criteria:
                if order in applicant.scores:
                    print(f"      {order.name}: {applicant.scores[order]}")

        print()

    def view_applicants_list(self, applicants: List[Applicant]):
        """Prints list of all applicants to console."""
        for index, applicant in enumerate(applicants):
            print(f"{index+1}. {applicant.name}")
        print()

    def view_applicant_table(self, table: str):
        """Prints a table summary of applicants and their scores"""
        pydoc.pager(table)
        print()
        print()

    def view_criteria(self, criteria_options, scored_criteria):
        """Prints list of all criterion for the role to console."""
        for key, (_, criterion) in criteria_options.items():
            if criterion in scored_criteria:
                print(f"\033[9m{key}: {criterion}\033[29m  ", end="")
            else:
                print(f"{key}: {criterion}  ", end="")
        print()
        print()

    def view_selection_options(self, options: Dict[str, tuple]):
        """Prints list of avaliable scoring option for selected criterion to console."""
        # prints all of the available options
        for index, action in options.items():
            print(f"{index}: {action[1]}  ", end="")
        print()
        print()

    def view_update(self, attribute, change):
        print(f"Updated: {attribute} to: {change}\n")
        print()

    def view_filter_help(self):
        print("""
        VARIABLES:
            applicant  # APPLICANT OBJECT
            i          # APPLICANT INDEX

        FUNCTIONS:
            name(applicant, "<contains>")
            cv(applicant, "<python regex>")
            score(applicant, "<criterion name>", "<score>")
            rtw(applicant) [has right to work]
            total_score(applicant.scores)

        EXAMPLES:
            cv(applicant, "(?i)nvidia")
            total_score(applicant.scores) >= 50
            score(applicant, "Professional experience", "Excellent")
            score(applicant, "Cover letter", None)
            i < 10 and not rtw(applicant)
        """)

    def view_table_legend(self, criteria):
        criteria_names = [criteria.name for criteria in criteria]
        abbreviations = abbreviate(criteria_names)
        legend = dict(zip(abbreviations, criteria_names))
        legend = dict(sorted(legend.items()))
        for line in legend.items():
            print(f"{line[0]}: {line[1]}")
        print()


