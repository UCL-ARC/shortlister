import glob
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
import csv

@dataclass
class Criterion:
    name: str
    description: str
    scores: List[str]

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

def load_shortlist(path):
    criteria = load_criteria(path+"/criteria.csv")
    role = load_role(path,criteria)
    applicants = load_applicants(path)
    shortlist = Shortlist(role,applicants)
    return shortlist

def load_role(path,criteria):
    role = (path,"0001",criteria)
    return role
    


def load_applicants(path):
    p = Path(path)
    files = glob.glob(str(p/"*.pdf"))
    applicants = []
    for file in files:
        file = Path(file)
        name_parts = file.stem.split("_")#removes .pdf 

       # type(" ".join(name_parts[0,1]))
        applicant = Applicant(" ".join(name_parts[0:2]),file,{})
        applicants.append(applicant)
    return applicants

def load_criteria(csv_file):
    criteria = []
    with open(csv_file) as file:
        reader= csv.reader(file)
        next(reader)

        for row in reader:
            criterion = Criterion(row[0],row[1],[])
            criteria.append(criterion)
    return criteria
