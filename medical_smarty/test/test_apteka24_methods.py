from medical_smarty.spiders.apteka24_items import Apteka24Items

exp1 = 'Дофамин 150 мг N60'.lower().split()
exp2 = 'Гофен 2г №30'.lower().split()
exp3 = 'Гофен 150мг N40'.lower().split()


def test_custom_title_splitter():
    assert Apteka24Items.custom_title_splitter(exp1) == ['дофамин', '150', 'мг', '№60']
    assert Apteka24Items.custom_title_splitter(exp2) == ['гофен', '2', 'г', '№30']
    assert Apteka24Items.custom_title_splitter(exp3) == ['гофен', '150', 'мг', '№40']