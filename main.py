#CRUD
#Pickle
from typing import List
import pickle
from dataclasses import dataclass

#data class
@dataclass
class Person:
    name: str
    age: int
    contact: str

@dataclass
class Candidates():
    candidates: List[Person]

candidates=[]

spongebob = Person(name="Spongebob",age=30,contact="7238479825")
patrick = Person(name="Patrick",age=24,contact="2347929348")


#objects


#CRUD
'''def create_candidate():
    candidate = Candidate(name,age,contact)
    return'''

#pickle
with open("candidate.pkl","wb") as file:
    pickle.dump(spongebob,file)

with open("candidate.pkl","rb") as file:
    loaded_candidate = pickle.load(file)

print(loaded_candidate)


#