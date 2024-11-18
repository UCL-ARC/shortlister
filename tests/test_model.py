from typing import List
import pytest
from shortlister import model
from pathlib import Path

SCORES_VALUES = {
    "Unsatisfactory": 0,
    "Moderate": 10,
    "Satisfactory": 20,
    "Excellent": 40,
}
SCORES = list(SCORES_VALUES.keys())
path = Path("test_role")
pickle_file_name = Path("shortlist.pickle")
csv_file = Path("criteria.csv")


def test_load_criteria():
    criteria_result = model.load_criteria(path / csv_file)
    expected = model.Criterion
    for criterion in criteria_result:
        assert type(criterion) is expected
        assert criterion.name and criterion.description is not None


@pytest.mark.parametrize(
    "folder_path,expected",
    [
        (path, ["Emma Jones", "Sarah Thompson"]),
        (Path("non_existing_folder"), []),
    ],
)
def test_load_applicants(folder_path, expected):
    applicants = model.load_applicants(folder_path)
    result = [applicant.name for applicant in applicants]
    assert result == expected


def test_load_role():
    criteria = [
        model.Criterion(
            name="PhD",
            description="Degree or relevant experience",
        ),
        model.Criterion(
            name="Research software",
            description="Authorship,development and maintenance",
        ),
        model.Criterion(
            name="Best practices",
            description="Issue tracking, testing, documentation etc.",
        ),
    ]

    result = model.load_role(path, model.load_criteria(path / csv_file))
    expected = model.Role(job_title="test_role", job_id="0001", criteria=criteria)

    assert result == expected


def test_save_load():
    c = [
        model.Criterion(name="c1", description="d1"),
        model.Criterion(name="c2", description="d2"),
        model.Criterion(name="c3", description="d3"),
    ]

    a = [
        model.Applicant(
            name="a1",
            cv="c1",
            email="e1",
            phone="p1",
            post_code="po1",
            country_region="r1",
            right_to_work=True,
            visa_requirement=None,
            scores={c[0]: SCORES[3], c[1]: SCORES[2], c[2]: SCORES[0]},
            notes="n1",
        ),
        model.Applicant(
            name="a2",
            cv="c2",
            email="e2",
            phone="p2",
            post_code="po2",
            country_region="r2",
            right_to_work=False,
            visa_requirement="text",
            scores={c[0]: SCORES[1], c[1]: SCORES[0]},
            notes="n2",
        ),
    ]

    shortlist = model.Shortlist(
        role=model.Role(job_title="tests", job_id="0000", criteria=c), applicants=a
    )

    model.save_shortlist(Path("tests"), shortlist)
    result: model.Shortlist = model.load_pickle(Path("tests") / pickle_file_name)

    applicant_criterion_list = [
        criterion
        for applicant in result.applicants
        for criterion in list(applicant.scores.keys())
    ]

    for criterion in applicant_criterion_list:
        assert criterion in c
    assert result.role.job_title == "tests"
    assert result.role.job_id == "0000"
    assert result.role.criteria == c
    assert result.applicants == a
    assert result.applicants[0].name == "a1"
    assert result.applicants[1].name == "a2"


def test_load_applicant_from_pdf():
    applicant: model.Applicant = model.load_applicants_from_pdf(
        Path("test_role\Emma_Jones_16743_Candidate_Pack.pdf")
    )
    assert applicant.name == "Emma Jones"
    assert applicant.email == "emmaj@outlook.com"
    assert applicant.phone == "+44 07871235436"
    assert applicant.post_code == "UB4 4RW"
    assert applicant.country_region == "United Kingdom, London"
