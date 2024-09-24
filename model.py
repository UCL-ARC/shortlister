from typing import List
from dataclasses import dataclass,field

@dataclass
class Person:
    name: str
    age: int
    contact: str

@dataclass
class Role:
    job_title: str
    job_id: str
    people: List[Person] = field(default_factory=list)


@dataclass 
class Questions: #library
    score = ["Exceptional","Merit","Satisfactory","Unsatisfactory"]

#want to make it so questions have a property called score, and the options for this property can be choose from a list with score ratings


# candidate class, under role

# question class: bunch of question objects