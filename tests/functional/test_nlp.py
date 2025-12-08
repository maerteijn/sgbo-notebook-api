from sgbo_notebook_api.nlp import NLPUtility


def test_extract_entities():
    expected_result = [
        {"text": "12:15", "start_char": 0, "end_char": 5, "label": "TIME"},
        {"text": "Jan Janssen", "start_char": 19, "end_char": 30, "label": "PERSON"},
        {
            "text": "ik ben geboren op",
            "start_char": 34,
            "end_char": 51,
            "label": "SIGNAL",
        },
        {"text": "15-01-1970", "start_char": 52, "end_char": 62, "label": "DATE"},
        {"text": "Arnhem", "start_char": 66, "end_char": 72, "label": "GPE"},
        {
            "text": "06123456789",
            "start_char": 97,
            "end_char": 108,
            "label": "PHONE_NUMBER",
        },
        {
            "text": "2 mannen rijden",
            "start_char": 121,
            "end_char": 136,
            "label": "SIGNAL",
        },
        {
            "text": "blauwe volkswagen polo",
            "start_char": 144,
            "end_char": 166,
            "label": "SIGNAL",
        },
        {"text": "14:30", "start_char": 177, "end_char": 182, "label": "TIME"},
    ]

    nlp_utility = NLPUtility(
        text="12:15 Mijn naam is Jan Janssen en ik ben geboren op 15-01-1970 in Arnhem, mijn telefoonnummer "
        "is 06123456789. Ik zag net 2 mannen rijden in een blauwe volkswagen polo "
        "Het is nu 14:30."
    )
    assert list(nlp_utility.entities) == expected_result
