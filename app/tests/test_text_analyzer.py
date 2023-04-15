from src.feedback.text_analyzer import TextAnalyzer


def test_can_instantiate_analyzer(random_good_message, random_bad_message):
    TextAnalyzer(random_good_message)
    TextAnalyzer(random_bad_message[1])


def test_find_sufix(analyzer_instance):
    splitted_raw = analyzer_instance.raw_message.split(" ")
    for index, word in enumerate(splitted_raw[:-1]):
        assert analyzer_instance.sufix_for(word) == splitted_raw[index + 1]


def test_returns_none_when_has_no_sufix(analyzer_instance):
    first_word = analyzer_instance.raw_message.split(" ")[-1]
    assert analyzer_instance.sufix_for(first_word) is None


def test_returns_none_when_sufix_target_does_not_exist(analyzer_instance):
    assert analyzer_instance.sufix_for("fake") is None


def test_find_prefix(analyzer_instance):
    splitted_raw = analyzer_instance.raw_message.split(" ")
    for prev_index, word in enumerate(splitted_raw[1:]):
        assert analyzer_instance.prefix_for(word) == splitted_raw[prev_index]


def test_returns_none_when_has_no_prefix(analyzer_instance):
    first_word = analyzer_instance.raw_message.split(" ")[0]
    assert analyzer_instance.prefix_for(first_word) is None


def test_returns_none_when_prefix_target_does_not_exist(analyzer_instance):
    assert analyzer_instance.prefix_for("fake") is None


def test_check_when_word_is_verb(analyzer_instance):
    assert analyzer_instance.is_verb_tag("verificamos")
    assert analyzer_instance.is_verb_tag("comunicando")


def test_check_when_word_is_not_verb(analyzer_instance):
    assert not analyzer_instance.is_verb_tag("pessoas")
    assert not analyzer_instance.is_verb_tag("ativos")
    assert not analyzer_instance.is_verb_tag("estudantes")
    assert not analyzer_instance.is_verb_tag("usuários")
