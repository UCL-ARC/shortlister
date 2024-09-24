from typing import List
from dataclasses import dataclass,field

@dataclass
class Person:
    name: str
    age: int
    contact: str

@dataclass
class Candidates:
    people: List[Person] = field(default_factory=list) #creates an empty list for all the Person classes

@dataclass
class Role:
    pass

@dataclass 
class Questions: #library
    pass
