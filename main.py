#CRUD
#Pickle
import pickle
from model import *
from typing import List
from dataclasses import dataclass,field

#data class

def update():
    name = None
    age = None
    contact = None


#CRUD
#create
def create_person(name, age, contact):
    person = Applicant(name, age, contact)
    with open ("candidate.pkl","wb") as file:
        pickle.dump(person,file)
    return person

create_person("patrick",90,"2738497234")

#creats person object and store/pickle it as a file
#need a way to make 

#unpikles the file
def read_person(candidate):
    with open(candidate+".pkl","rb") as file:
        loaded_candidate = pickle.load(file)
        print(loaded_candidate)

#update 
def add_score_to_person(score, candidate):
    pass


 
def read_people(self):
    with open("candidate.pkl"+str(len(self.people))+".pkl","rb") as file:
        loaded_candidate = pickle.load(file)
        print(loaded_candidate)
        
    #print(f"Candidate name: {person(.name} , age: {person.age} , contact details: {person.contact} ")



#delete

def delete_person(list,person):
    list.remove(person)
# candidate positions

"""       
#person objects
spongebob = Person(name="Spongebob",age=30,contact="7238479825")
patrick = Person(name="Patrick",age=24,contact="2347929348")
squidward = Person(name="Squidward",age=98,contact="2784279384")

#tests
crew.add_person(spongebob)
crew.add_person(patrick)
crew.people.remove(patrick)
print(crew.people)

crew.read_people()"""

#questions and scores

questions = {"question 1":"What is your experience?",
                        "question 2": "What is your skill repetoire?",
                        "question 3": "aosufoasd",
                        "question 4": "ashdfaljslfjk",
                        "question 5": "asufiauoisufoiaus"}

score = ["Exceptional","Merit","Satisfactory","Unsatisfactory"]



#pickle
shortlist = {"candidates": None,
             "questions": questions}
pickle.save(shortlist)

#unpickle
pickle.load(shortlist)


"""with open("candidate.pkl","wb") as file:
    pickle.dump(spongebob,file)

with open("candidate.pkl","rb") as file:
    loaded_candidate = pickle.load(file)

print(loaded_candidate)"""


#repl

#