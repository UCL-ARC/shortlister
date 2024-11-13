from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
import pickle
import csv


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
SCORE_AND_VALUE = {
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
        applicants = load_applicants(path)
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
    return applicants


def load_criteria(csv_file):
    """Generate criteria(list of criterion instances) from csv file."""
    criteria = []
    with open(csv_file) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            criterion = Criterion(
                name=row[0], description=row[1]
            )
            criteria.append(criterion)
    return criteria


def update_applicant_score(
    applicant: Applicant, criterion: Criterion, score_index: int
):
    """Updates applicant's score field with selected criterion and selected score from criterion."""
    scores = SCORE_AND_VALUE.keys()
    applicant.scores[criterion] = scores[score_index]


def update_applicant_notes(applicant: Applicant, new_note: str):
    """Appends new note to applicant's notes section."""

    if len(applicant.notes):
        applicant.notes += "; "

    applicant.notes += new_note


def total_score(scores: Dict[Criterion, str]) -> int:
    """Takes applicant scores dictionary and returns a total score as a single number"""

    values = [SCORE_AND_VALUE.get(score) for score in scores.values()]
    return sum(values)

def clear_score(applicant:Applicant,criterion:Criterion):
    """Removes criterion from Applicant's scores dictionary."""
    if criterion in applicant.scores:
        del applicant.scores[criterion]