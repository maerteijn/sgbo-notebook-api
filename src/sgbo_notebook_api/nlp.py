from collections.abc import Generator
from typing import TypedDict

import spacy

regex_patterns = [
    {
        "label": "PHONE_NUMBER",
        "pattern": [{"TEXT": {"REGEX": "(\\+31|0|0031)6{1}[1-9]{1}[0-9]{7}"}}],
    },
    {
        "label": "DATE",
        "pattern": [
            {
                "TEXT": {
                    "REGEX": "(3[01]|[12][0-9]|0?[1-9])(\\-|\\.)(1[0-2]|0?[1-9])(\\-|\\.)[0-9]{2,4}"
                }
            }
        ],
    },
    {
        "label": "TIME",
        "pattern": [
            {
                "TEXT": {
                    "REGEX": "(24:00|2[0-3]\\:[0-5][0-9]|[0-1][0-9]\\:[0-5][0-9]|[0-9]\\:[0-5][0-9])"
                },
            }
        ],
    },
]

token_match_patterns = [
    # Match signals like "iemand kunnen bellen", "vrouw verdwaald" or "2 mannen waren op de vuist"
    {
        "label": "SIGNAL",
        "pattern": [
            {"LIKE_NUM": True, "OP": "?"},
            {"POS": {"IN": ["PRON", "NOUN"]}},
            {"POS": "AUX", "OP": "+"},
            {"POS": {"IN": ["VERB", "ADP"]}, "OP": "+"},
        ],
    },
    # Match objects like "blauwe auto"
    {
        "label": "SIGNAL",
        "pattern": [
            {"POS": "ADJ", "OP": "+"},
            {"POS": {"IN": ["VERB", "NOUN"]}, "OP": "+"},
        ],
    },
    # Match a number connected to a noun, like "100 mannen" or "2 autos", but <=100
    {
        "label": "SIGNAL",
        "pattern": [
            {
                "LIKE_NUM": True,
                "DEP": "nummod",
                "TEXT": {"REGEX": "\\b(0*(?:[1-9][0-9]?|100))\\b"},
            },
            {"POS": "NOUN"},
            {"POS": "VERB", "OP": "?"},
        ],
    },
]

# A poc to use dictionaries / lexicons / datasets
exact_match_patterns = [
    {"label": "SIGNAL", "pattern": [{"LOWER": "aanrijding"}]},
    {"label": "LOC", "pattern": [{"LOWER": "de"}, {"LOWER": "wallen"}]},
    {"label": "ORG", "pattern": [{"LOWER": "RTIC"}]},
    {
        "label": "LOC",
        "pattern": [{"LOWER": "pc"}, {"LOWER": "hoofdstraat"}, {"LIKE_NUM": True}],
    },
]


def setup_nlp() -> spacy.Language:
    nlp: spacy.Language = spacy.load("nl_core_news_sm")
    entity_ruler = nlp.add_pipe("entity_ruler", before="ner")
    entity_ruler.add_patterns(regex_patterns)  # type: ignore[attr-defined]

    config = {"spans_key": None, "annotate_ents": True, "overwrite": False}
    span_ruler = nlp.add_pipe("span_ruler", config=config, before="ner")
    span_ruler.add_patterns(token_match_patterns)  # type: ignore[attr-defined]
    span_ruler.add_patterns(exact_match_patterns)  # type: ignore[attr-defined]

    return nlp


nlp = setup_nlp()


class Entity(TypedDict):
    text: str
    start_char: int
    end_char: int
    label: str


class NLPUtility:
    ALLOWED_ENTITIES = (
        "GPE",
        "PERSON",
        "SUBJECT",
        "ORG",
        "LOC",
        "PHONE_NUMBER",
        "DATE",
        "TIME",
        "SIGNAL",
    )

    def __init__(self, text: str, nlp: spacy.Language = nlp):
        # Some cleanup so spacy has more success matching tokens / entities
        text = text.strip()
        text = text.replace("\r", "")

        self.nlp: spacy.Language = nlp
        self.doc: spacy.tokens.Doc = self.nlp(text)

        if self.ALLOWED_ENTITIES:
            self.doc.set_ents(
                [x for x in self.doc.ents if x.label_ in self.ALLOWED_ENTITIES]
            )

    @property
    def entities(self) -> Generator[Entity]:
        for entity in self.doc.ents:
            if entity.label_ in self.ALLOWED_ENTITIES:
                yield Entity(
                    text=entity.text,
                    start_char=entity.start_char,
                    end_char=entity.end_char,
                    label=entity.label_,
                )
