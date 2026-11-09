from riverfmt import normalize


def test_special_case():
    assert normalize("QTY") == "quantity"
