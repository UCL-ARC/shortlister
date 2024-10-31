import pytest
import source_code.model as mdl

path = "test_role"

def test_load_criteria(filepath= "test_role/criteria.csv"):
    result = mdl.load_criteria(filepath)
    expected = mdl.Criterion
    for criterion in result:
        assert type(criterion) is expected
        assert criterion.name and criterion.description and criterion.scores is not None
    ...
@pytest.mark.parametrize("folder_path,expected",
                         [("test_role",["Emma Jones","Michael Davis","Sarah Thompson"]),
                          ("non_existing_folder",[])])
def test_load_applicants(folder_path,expected):
    applicants = mdl.load_applicants(folder_path)
    result = [applicant.name for applicant in applicants]
    assert result == expected

def test_load_role():
    result = mdl.load_role(path,test_load_criteria)
    expected = "test_role"
    assert result.job_title == expected

def test_load_shortlist():
    shortlist = mdl.load_shortlist(path)
    assert type(shortlist) is mdl.Shortlist