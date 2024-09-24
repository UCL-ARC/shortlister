#CRUD
#Pickle
from typing import List
import pickle
from dataclasses import dataclass,field

#data class

    def  update_person(self):
            choice = input(f"What do you want to update for {self.name} ? (name, age or contact?):")
            if choice.lower() == "name":
                new_name = input("Please enter the new name:")
                print(f"Updated {self.name}'s grade to {new_name}")
            if choice.lower() == "age":
                new_age = input("Please enter the new age:")
                print(f"Updated {self.age}'s grade to {new_age}")
            if choice.lower() == "contact":
                new_contact = input("Please enter the new contact:")
                print(f"Updated {self.contact}'s grade to {new_contact}")
            else:
                pass


    #CRUD
    def add_person(self, person:Person):
        self.people.append(person)
        with open("candidate"+str(len(self.people))+".pkl","wb") as file:
            pickle.dump(self.people,file) 

    def read_people(self):
        with open("candidate"+str(len(self.people))+".pkl","rb") as file:
            loaded_candidate = pickle.load(file)

            print(loaded_candidate)
            
        #print(f"Candidate name: {person(.name} , age: {person.age} , contact details: {person.contact} ")



    def delete_person(self,person):
        self.people.remove(person)
        
# candidate positions
crew = Candidates(position="Krabby Patty employee")

#person objects
spongebob = Person(name="Spongebob",age=30,contact="7238479825")
patrick = Person(name="Patrick",age=24,contact="2347929348")
squidward = Person(name="Squidward",age=98,contact="2784279384")

#tests
crew.add_person(spongebob)
crew.add_person(patrick)
crew.people.remove(patrick)
print(crew.people)

crew.read_people()
#pickle

"""with open("candidate.pkl","wb") as file:
    pickle.dump(spongebob,file)

with open("candidate.pkl","rb") as file:
    loaded_candidate = pickle.load(file)

print(loaded_candidate)"""


#repl