import joblib
import nltk
import ssl
from nltk import TokenSearcher, word_tokenize
from unidecode import unidecode

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("punkt")

TAGGER = joblib.load("POS_tagger_brill.pkl")


class TextAnalyzer:
    GENDER_MARKS = {"os", "ores", "ões", "ns", "ãos"}
    NEUTRAL_MARK = {"pessoas"}

    def __init__(self, text_message) -> None:
        self.raw_message = self.clear_message(text_message)
        raw_tokens = word_tokenize(self.raw_message)
        self.token_searcher = TokenSearcher(tokens=raw_tokens)
        self.pos_tags = dict(TAGGER.tag(raw_tokens))

    def check_for_avoided_expression(self, avoided_expression):
        if self.is_gender_related(avoided_expression):
            gender_analysis = self.check_gender_neutrality(avoided_expression)
            if gender_analysis:
                return gender_analysis
        elif avoided_expression in self.raw_message:
            return avoided_expression

    def check_gender_neutrality(self, target):
        word_target = target.split(" ")[1]
        this_prefix = self.prefix_for(word_target)
        this_sufix = self.sufix_for(word_target)

        if not (this_prefix or this_sufix):
            return None

        if this_prefix in self.NEUTRAL_MARK:
            return None

        result = word_target
        if this_prefix and self.marks_dominant_gender(this_prefix):
            result = this_prefix + " " + result
        if this_sufix and self.marks_dominant_gender(this_sufix):
            result = result + " " + this_sufix

        if self.marks_dominant_gender(word_target) or result != word_target:
            return result
        else:
            return None

    def marks_dominant_gender(self, target_word):
        gender_marked = any(
            mark for mark in self.GENDER_MARKS if target_word.endswith(mark)
        )
        return gender_marked and not self.is_verb_tag(target_word)

    def is_verb_tag(self, tagged_word):
        return self.pos_tags.get(tagged_word, "") == "V"

    def prefix_for(self, target_expression):
        found_prefix = self.token_searcher.findall(
            f"(<.*>) <{target_expression}>"
        )
        if not found_prefix:
            found_prefix = self.token_searcher.findall(
                f"(<.*>) <{unidecode(target_expression)}>"
            )

        return found_prefix[0][0] if found_prefix else None

    def sufix_for(self, target_expression):
        found_sufix = self.token_searcher.findall(
            f"<{target_expression}> (<.*>)"
        )
        if not found_sufix:
            found_sufix = self.token_searcher.findall(
                f"<{unidecode(target_expression)}> (<.*>)"
            )
        return found_sufix[0][0] if found_sufix else None

    def is_gender_related(self, avoided_expression):
        return avoided_expression.startswith("os ")

    def clear_message(self, text_message):
        try:
            clean_message = "".join(
                char
                for char in text_message.lower()
                if char.isalnum() or char in " ,.;!?()"
            )
        except AttributeError:
            raise TypeError(
                f"Argument needs to be a string, not {type(text_message)}"
            )

        return clean_message
