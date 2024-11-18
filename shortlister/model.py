from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import csv
import pickle
import fitz
import re


@dataclass(frozen=True)
class Criterion:
    """A property of Role - contained within the attribute criteria(list of Criterion objects)."""

    name: str
    description: str


@dataclass
class Applicant:
    """A property of Shortlist - contained within the attribute applicants(list of Applicant objects)."""

    name: str
    cv: str  # path to cv
    email: str
    phone: str
    post_code: str
    country_region: str
    right_to_work: bool
    visa_requirement: str
    scores: Dict[Criterion, str]
    notes: str


@dataclass
class Role:
    """A property of Shortlist."""

    job_title: str
    job_id: str
    criteria: List[Criterion]


@dataclass
class Shortlist:
    """Major class object containing all relevant role, applicant, criteria information for shortlisting."""

    role: Role
    applicants: List[Applicant]


# Constant variables

PICKLE_FILE_NAME = "shortlist.pickle"
CRITERIA_FILE_NAME = "criteria.csv"
RANK_AND_SCORE = {
    "Unsatisfactory": 0,
    "Moderate": 10,
    "Satisfactory": 20,
    "Excellent": 40,
}

# Functions


def load_pickle(file_path):
    """Load shortlist from existing pickle file."""
    with open(file_path, "rb") as f:
        shortlist = pickle.load(f)
    return shortlist


def save_shortlist(path, shortlist):
    """Save shortlist as a pickle file within the role directory path."""
    with open(path / PICKLE_FILE_NAME, "wb") as f:
        pickle.dump(shortlist, f)


def load_shortlist(path: Path):
    """Import shortlist data from either: 1. Pickle file or 2. Role directory (when there is no existing pickle data)."""
    file = path / PICKLE_FILE_NAME
    if file.exists():
        shortlist = load_pickle(file)

    else:
        criteria = load_criteria(path / CRITERIA_FILE_NAME)
        role = load_role(path, criteria)
        applicants = load_applicants_from_pdf(path)
        shortlist = Shortlist(role, applicants)

    return shortlist


def load_role(path, criteria):
    """Generates role object instance."""
    role = Role(str(path), "0001", criteria)
    return role


def load_applicants(path: Path):
    """Generate a list of applicant instances from pdf format CVs."""
    files = path.glob("*.pdf")
    applicants = []
    for file in files:
        name_parts = file.stem.split("_")
        applicant = Applicant(
            name=" ".join(name_parts[0:2]), cv=file, scores={}, notes=""
        )
        applicants.append(applicant)
    sort_alpha(applicants)
    return applicants

# wip
def load_applicants_from_pdf(path: Path):
    fields = ("First Name","Last Name","Known as","Email Address","Preferred Phone Number","Postcode","Country & Region")
    applicants = []
    files = path.glob("*.pdf")
    for file in files:

        doc = fitz.open(file)  # example document
        page = doc[0]
        text = page.get_text(sort=True) # extract text in reading order 

        # turns text into a list of string for each line
        lines = text.splitlines()

        # remove empty lines
        for line in lines:
            if line == "":
                lines.remove(line)

        # removes starting/trailling whitespaces in each line
        cleaned = list(line.strip() for line in lines)
        
        # takes the section with simple field and info
        applicant_info = cleaned[1:-7]
        right_to_work = cleaned[-7:-3]

        # finds where the question is and checks the next index which contains the answer to the question
        if 'Do you have the unrestricted right to work in the UK?' in right_to_work:
            i = right_to_work.index('Do you have the unrestricted right to work in the UK?')
            if right_to_work[i+1] == "No":
                j = right_to_work.index("If no, please give details of your VISA requirements")
                visa_req_text = right_to_work[j+1] 
                applicant_right_to_work = False
                
            elif right_to_work[i+1] == "Yes":
                right_to_work = True
                visa_req_text = None
            else:
                print("Something went wrong")
        else:
            raise ValueError("Right to work is not identified")

        info = get_info(fields,applicant_info)
        first_name = info[0]
        last_name = info[1]
        email = info[3]
        phone = info[4]
        post_code = info[5]
        country_region = info[6]

        applicant = Applicant(name=f"{first_name} {last_name}",
                              cv=file, 
                              email=email, 
                              phone=phone, 
                              post_code=post_code, 
                              country_region=country_region, 
                              right_to_work=applicant_right_to_work, 
                              visa_requirement=visa_req_text,
                              scores={},
                              notes="")
        applicants.append(applicant)
    
    return applicants

def load_criteria(csv_file):
    """Generate criteria(list of criterion instances) from csv file."""
    criteria = []
    with open(csv_file) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            criterion = Criterion(name=row[0], description=row[1])
            criteria.append(criterion)
    return criteria


def update_applicant_score(
    applicant: Applicant, criterion: Criterion, score_index: int
):
    """Updates applicant's score field with selected criterion and selected score"""
    applicant.scores[criterion] = list(RANK_AND_SCORE)[score_index]


def update_applicant_notes(applicant: Applicant, new_note: str):
    """Appends new note to applicant's notes section."""

    if len(applicant.notes):
        applicant.notes += "; "

    applicant.notes += new_note


def total_score(scores: Dict[Criterion, str]) -> int:
    """Takes applicant scores dictionary and returns a total score as a single number"""

    values = [RANK_AND_SCORE.get(score) for score in scores.values()]
    return sum(values)


def sort_alpha(applicants: List[Applicant]):
    """Sort by alphabetical order."""
    return applicants.sort(key=lambda applicant: applicant.name)


def sort_ascending_score(applicants: List[Applicant]):
    """Sort by score (lowest to highest)."""
    return applicants.sort(key=lambda applicant: total_score(applicant.scores))


def sort_descending_score(applicants: List[Applicant]):
    """Sort by score(highest to lowest)."""
    return applicants.sort(
        reverse=True, key=lambda applicant: total_score(applicant.scores)
    )


def clear_score(applicant: Applicant, criterion: Criterion):
    """Removes criterion from Applicant's scores dictionary."""
    if criterion in applicant.scores:
        del applicant.scores[criterion]

# text extraction

def get_info(fields,applicant_info):
    """gets the section containing applicant information from extracted text"""
    info = []
    for field in fields:
        for i in applicant_info:
            if field in i:
                unclean = i.replace(field,"")
                clean = re.sub(r'\s{2,}', ' ', unclean)
                info.append(clean.strip())
    return info


# creating tabular data


def applicant_table(applicants: List[Applicant], criteria: List[Criterion]) -> List:
    """Generates applicant and score data for summary table"""
    # tab is a list of lists:
    # each list in tab has the format of ["1","name1","score1","score2","score3","score*n"]
    tab = []
    i = 0  # sets the applicant number
    for applicant in applicants:
        i += 1
        applicant_info = []  # list with correct information format for each row
        applicant_info.append(i)  # applicant number
        applicant_info.append(applicant.name)  # applicant name
        # append criterion score in the order criteria
        for criterion in criteria:
            if criterion in applicant.scores:
                applicant_info.append(applicant.scores.get(criterion)[0])
            else:
                # fills in N/A if a score is not marked yet
                applicant_info.append("-")
        tab.append(applicant_info)
    return tab


def abbreviate(list_of_strings: List[str]) -> list[str]:
    """Create abbreviations for all strings in a list."""
    abbreviations = []
    for string in list_of_strings:
        if " " in string:
            separated = string.split(
                " "
            )  # separates individual words in string into a list
            abbrev = "".join(
                word[0].upper() for word in separated
            )  # combine intial of all words and return as uppercase
            abbreviations.append(abbrev)
        else:
            abbreviations.append(string)
    return abbreviations
