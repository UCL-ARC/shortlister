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

    def create_criteria(self,csv_file):
         with open(csv_file) as file:
            reader= csv.reader(file)
            next(reader)

            for row in reader:
                criterion = Criterion(row[0],row[1],[])
                self.criteria.append(criterion)
            return(self.criteria)

@dataclass
class Shortlist:
    role: Role
    applicants: List[Applicant]

    def creat_role(self,role):
        pass