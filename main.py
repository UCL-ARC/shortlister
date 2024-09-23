#CRUD
#Pickle
import pickle

class Candidate:
    
    def __init__(self,name,age,contact):
        self.name = name
        self.age = age
        self.contact = contact

    def read_candidate(self):
        print(self.name, self.age, self.contact)
        
    def update_candidate():
        pass

    def delete_candidate():
        pass

    def __reduce__(self):
        return (self.__class__,(self.name, self.age,self.contact))

#objects
candidate1 = Candidate("Spongebob",30,"7238479825")

#CRUD
'''def create_candidate():
    candidate = Candidate(name,age,contact)
    return'''

#pickle 
with open("candidate1.pkl","wb") as file:
    pickle.dump(candidate1,file)

with open("candidate1.pkl","rb") as file:
    loaded_candidate = pickle.load(file)

print(loaded_candidate)