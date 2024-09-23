#CRUD
#Pickle
from typing import List
import pickle
from dataclasses import dataclass,field

#data class

@dataclass
class Person:
    name: str
    age: int
    contact: str
        
@dataclass
class Candidates:
    position: str
    people: list[Person] = field(default_factory=list) #creates an empty list for all the Person classes

    #CRUD
    def add_person(self, person:Person):
        self.people.append(person)
        with open("candidate"+str(len(self.people))+".pkl","wb") as file:
            pickle.dump(self,file) 

    def read_people(self):
        with open("candidate"+str(len(self.people))+".pkl","rb") as file:
            loaded_candidate = pickle.load(file)

            print(loaded_candidate)
            
        #print(f"Candidate name: {person.name} , age: {person.age} , contact details: {person.contact} ")

    def update_person(self):
        pass

    def delete_person(self):
        self.people.remove(self)
        
# candidate positions
crew = Candidates(position="Krabby Patty employee")

#person objects
spongebob = Person(name="Spongebob",age=30,contact="7238479825")
patrick = Person(name="Patrick",age=24,contact="2347929348")
squidward = Person(name="Squidward",age=98,contact="2784279384")

#tests
crew.add_person(spongebob)
crew.add_person(patrick)
print(len(crew.people))

crew.read_people()
#pickle

"""with open("candidate.pkl","wb") as file:
    pickle.dump(spongebob,file)

with open("candidate.pkl","rb") as file:
    loaded_candidate = pickle.load(file)

print(loaded_candidate)"""


#