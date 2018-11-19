import svc.illumina as illumina


def test_generates_sample_sheet_with_valid_body():
    assert illumina.generate_sample_sheet({}) == {}
