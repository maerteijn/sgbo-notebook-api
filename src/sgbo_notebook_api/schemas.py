ENTITIES_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "start_char": {"type": "integer"},
            "end_char": {"type": "integer"},
            "label": {"type": "string"},
        },
        "required": [
            "text",
            "start_char",
            "end_char",
            "label",
        ],
        "additionalProperties": False,
    },
}
