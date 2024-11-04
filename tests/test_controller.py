from shortlister.controller import Controller
from pathlib import Path
from readchar import readkey
import unittest

controller = Controller(path=Path("test_role"))

def test_create_controller():
    result = []
    for applicant in controller.shortlist.applicants:
        result.append(applicant.name)
    expected = ["Emma Jones","Michael Davis","Sarah Thompson"]

    assert result == expected
        
def detect_keypress():
    key = readkey()
    if key == 'a':
        return controller.show_applicants_list
    return "Unknown key"

class TestKeyPress(unittest.TestCase):
    @unittest.mock.patch('builtins.input', return_value='a')
    def test_detect_keypress(self, mock_read_key):
        result = detect_keypress() 
        self.assertEqual(result, "You pressed 'a' for show applicant")


    

