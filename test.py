from model import Applicant, Criterion, Role, Shortlist

def test_model():
    c1 = Criterion("PhD degree","degree or experience",["E","S","M","U"])
    c2 = Criterion("Programming","Language used for research",["E","S","M","U"])
    r = Role("apprentice programmer","28304982",[c1,c2])
    a1 = Applicant("Emma","cv1.pdf",{})
    a2 = Applicant("Michael","cv2.pdf",{})
    s = Shortlist(r,[a1,a2])
    print(s)

test_model()