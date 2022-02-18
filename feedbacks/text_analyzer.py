import joblib
import nltk
from nltk import TokenSearcher, word_tokenize

nltk.download('punkt')

TAGGER = joblib.load("POS_tagger_brill.pkl")


class TextAnalyzer:
    def __init__(self, raw_message) -> None:
        self.raw_message = raw_message
        raw_tokens = word_tokenize(raw_message)
        self.token_searcher = TokenSearcher(tokens=raw_tokens)
        self.pos_taggs = dict(TAGGER.tag(raw_tokens))

    def check_gender_neutrality(self, target):
        if self.is_verb_tag(self.prefix(target)):
            return None

        return self.prefix(target) + " " + target.split(" ")[1]

    def is_verb_tag(self, prefix_tag):
        return self.pos_taggs.get(prefix_tag, "") == "V"

    def prefix(self, target_expression):
        return self.token_searcher.findall(
            f"(<.*>) <{target_expression.split(' ')[1]}>"
        )[0][0]
