from shortlister.controller import Controller
from pathlib import Path

controller = Controller(path=Path("test_role"))

def test_create_controller():
    result = []
    for applicant in controller.shortlist.applicants:
        result.append(applicant.name)
    expected = ["Emma Jones","Michael Davis","Sarah Thompson"]

    assert result == expected
        

def test_keycapture():
    controller.run()

    

