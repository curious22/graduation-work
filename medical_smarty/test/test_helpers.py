from core import helpers


def test_get_correct_tags_n():
    assert helpers.get_correct_tags('n60') == ['№60']
    assert helpers.get_correct_tags('n150') == ['№150']
    assert helpers.get_correct_tags('140') == ['140']


def test_get_correct_mg():
    assert helpers.get_correct_tags('150мг') == ['150', 'мг']
    assert helpers.get_correct_tags('150') == ['150']


def test_get_correct_g():
    assert helpers.get_correct_tags('1г') == ['1', 'г']
    assert helpers.get_correct_tags('5') == ['5']

