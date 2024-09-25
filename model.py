from typing import Dict, List
from dataclasses import dataclass


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