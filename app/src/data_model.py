from pydantic import BaseModel


class AnalyzerOptions(BaseModel):
    feedbacks: dict
    alternatives: dict

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "feedbacks": {
                    "os amigos": "os_amigos",
                    "os trabalhadores": "os_trabalhadores",
                },
                "alternatives": {
                    "os_amigos": ["as amizades", "as pessoas amigas"],
                    "os_trabalhadores": [
                        "quem trabalha",
                        "as pessoas trabalhadoras",
                    ],
                },
            }
        }


class LNGReport(BaseModel):
    used_expression: str
    expression_alternatives: list = []
