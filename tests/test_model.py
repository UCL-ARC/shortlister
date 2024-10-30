import pytest
import source_code.model as mdl

def test_load_criteria(filepath= "test_role/criteria.csv"):
    result = mdl.load_criteria(filepath)
    expected = mdl.Criterion
    for criterion in result:
        assert type(criterion) is expected
        assert criterion.name and criterion.description and criterion.scores is not None
    ...

def test_load_applicants():
    result = mdl.load_applicants
    pass

def test_load_role():
    ...

def test_load_shortlist():
    ...