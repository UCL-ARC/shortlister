from model import Applicant, Criterion, Role, Shortlist
import csv
import glob
from pathlib import Path

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

def test_create_criterion(csv_file:str):
    with open(csv_file) as file:
        reader= csv.reader(file)
        next(reader)

        criteria = []

        for row in reader:
            criterion = Criterion(row[0],row[1],[])
            criteria.append(criterion)
        return(criteria)

def test_create_applicant(path):
    p = Path(path)
    files = glob.glob(str(p/"*.pdf"))
    applicants = []
    for file in files:
        file = Path(file)
        name_parts = file.stem.split("_")#removes .pdf 
        applicant = Applicant(" ".join(name_parts[0:2]),file,{})
        applicants.append(applicant)
    return applicants

def test_read():
    pass