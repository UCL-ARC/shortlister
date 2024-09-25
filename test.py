from model import Applicant, Criterion, Role, Shortlist
import csv

def test_model():
    c1 = Criterion("PhD degree","degree or experience",["E","S","M","U"])
    c2 = Criterion("Programming","Language used for research",["E","S","M","U"])
    r = Role("apprentice programmer","28304982",[c1,c2])
    a1 = Applicant("Emma","cv1.pdf",{})
    a2 = Applicant("Michael","cv2.pdf",{})
    s = Shortlist(r,[a1,a2])
    print(s)

def test_read_criteria():
    csv_file = "test_role/criteria.csv"
    with open(csv_file,"r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

def test_create_criterion():
    csv_file = "test_role/criteria.csv"
    with open(csv_file) as file:
        reader= csv.reader(file)

        criteria = []

        for row in reader:
            criterion = Criterion(row[0],row[1],[])
            criteria.append(criterion)
        print(criteria)

test_create_criterion()

#csv library
# use csv library to read the criteria.csv and create criterion objects based on the file contents
#open file and step through each rows