from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
import pickle
import csv

@dataclass (frozen=True)
class Criterion:
    name: str
    description: str
    scores: tuple
    
@dataclass
class Applicant:
    name: str
    cv: str #path to cv
    scores: Dict[Criterion,str]

@dataclass
class Role:
    job_title: str
    job_id: str
    criteria: List[Criterion]

@dataclass
class Shortlist:
    role: Role
    applicants: List[Applicant]

#functions

pickle_file_name = "shortlist.pickle"
criteria_file_name = "criteria.csv"

def load_pickle(file_path):
    """load shortlist from existing pickle file"""
    with open(file_path, "rb") as f:
        shortlist = pickle.load(f)
    return shortlist

def save_shortlist(path,shortlist):
    """save shortlist as a pickle file inside the role_directory"""
    with open(path/pickle_file_name, "wb") as f:
        pickle.dump(shortlist, f)

def load_shortlist(path):
    """import shortlist data from either pickle file or role directory if the former doesn't exist"""
    file = path/pickle_file_name
    if file.exists():
        shortlist = load_pickle(file)

    else:
        criteria = load_criteria(path/criteria_file_name)
        role = load_role(path,criteria)
        applicants = load_applicants(path,criteria) 
        shortlist = Shortlist(role,applicants)
    
    return shortlist

def load_role(path,criteria):
    """generates role object instance"""
    role = Role(str(path),"0001",criteria)
    return role

def load_applicants(path,criteria:list[Criterion]):
    """generate a list of applicant instances from pdf format CVs"""
    p = Path(path)
    files = p.glob("*.pdf")
    applicants = []

    for file in files:
        name_parts = file.stem.split("_")
        applicant = Applicant(" ".join(name_parts[0:2]),file,{criterion:"Not marked" for criterion in criteria})
        applicants.append(applicant)
    return applicants

def load_criteria(csv_file):
    """generate criteria(list of criterion instances) from csv file"""
    criteria = []
    with open(csv_file) as file:
        reader= csv.reader(file)
        next(reader)

        for row in reader:
            criterion = Criterion(name=row[0],description=row[1],scores= tuple(row[2].split(",")))
            criteria.append(criterion)
    return criteria

def update_applicant_score(applicant: Applicant, criterion: Criterion, score_index: int):
    applicant.scores[criterion] = criterion.scores[score_index]