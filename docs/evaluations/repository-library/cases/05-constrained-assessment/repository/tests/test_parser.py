from signal_window import parse_lines


def test_valid_and_blank():
    assert parse_lines(["a=2", "", "b=-1"]) == [("a", 2), ("b", -1)]


def test_bad_integer():
    try:
        parse_lines(["a=no"])
    except ValueError as error:
        assert "line 1" in str(error)
    else:
        raise AssertionError("expected ValueError")
