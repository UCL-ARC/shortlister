import pytest
import source_code.model as mdl
from pathlib import Path

path = "test_role"
pickle_file_name = "shortlist.pickle"

def test_load_criteria(filepath= "test_role/criteria.csv"):
    criteria_result = mdl.load_criteria(filepath)
    expected = mdl.Criterion
    for criterion in criteria_result:
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

def test_save_load():
    expected = mdl.Shortlist(role= mdl.Role(job_title="test_role",
                                             job_id="0000",
                                             criteria=[]),
                              applicants=[mdl.Applicant(name="George Smith",
                                                        cv="placeholder",
                                                        scores=[]),
                                          mdl.Applicant(name = "Jim Chapman",
                                                        cv="placeholder",
                                                        scores=[])]
                                                        )
    
    mdl.save_shortlist(path=Path("tests"), shortlist=expected)
    result:mdl.Shortlist = mdl.load_pickle("tests/shortlist.pickle")

    assert result.role.job_title == "test_role"
    assert result.role.job_id == "0000"
    assert result.role.criteria == []
    assert result.applicants[0].name == "George Smith"
    assert result.applicants[1].name == "Jim Chapman"

    