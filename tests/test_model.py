import pytest
from  shortlister import model
from pathlib import Path

path = "test_role"
pickle_file_name = "shortlist.pickle"

def test_load_criteria(filepath= "test_role/criteria.csv"):
    criteria_result = model.load_criteria(filepath)
    expected = model.Criterion
    for criterion in criteria_result:
        assert type(criterion) is expected
        assert criterion.name and criterion.description and criterion.scores is not None

@pytest.mark.parametrize("folder_path,expected",
                         [("test_role",["Emma Jones","Michael Davis","Sarah Thompson"]),
                          ("non_existing_folder",[])])
def test_load_applicants(folder_path,expected):
    applicants = model.load_applicants(folder_path)
    result = [applicant.name for applicant in applicants]
    assert result == expected

def test_load_role():
    criteria = [model.Criterion(name="PhD",
                              description="Degree or relevant experience",
                              scores = ("Unsatisfactory","Moderate","Satisfactory","Excellent")),
                model.Criterion(name="Research software",
                              description="Authorship,development and maintenance",
                              scores = ("Unsatisfactory","Moderate","Satisfactory","Excellent")),
                model.Criterion(name="Best practices",
                              description="Issue tracking, testing, documentation etc.",
                              scores = ("Unsatisfactory","Moderate","Satisfactory","Excellent"))]
    result = model.load_role(path,criteria)
    

    expected = model.Role(job_title="test_role",
                        job_id="0001",
                        criteria=criteria)

    assert result == expected

def test_save_load():
    expected = model.Shortlist(role= model.Role(job_title="test_role",
                                             job_id="0000",
                                             criteria=[]),
                              applicants=[model.Applicant(name="George Smith",
                                                        cv="placeholder",
                                                        scores=[]),
                                          model.Applicant(name = "Jim Chapman",
                                                        cv="placeholder",
                                                        scores=[])]
                                                        )
    
    model.save_shortlist(path=Path("tests"), shortlist=expected)
    result:model.Shortlist = model.load_pickle("tests/shortlist.pickle")

    assert result.role.job_title == "test_role"
    assert result.role.job_id == "0000"
    assert result.role.criteria == []
    assert result.applicants[0].name == "George Smith"
    assert result.applicants[1].name == "Jim Chapman"

    