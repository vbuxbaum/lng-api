from typing import List
from fastapi import FastAPI, Query
from feedbacks.feedbacks import AnalyzerOptions, Feedbacks, LNGReport

app = FastAPI(title="LNG API")

feedback_handler = Feedbacks()


@app.get("/", response_model=List[LNGReport])
def process_text(
    input_text: str = Query(
        default="", example="João e Maria são ótimos amigos", max_length=10000
    )
):
    return feedback_handler.find_avoided_expression(input_text)


@app.post("/", response_model=List[LNGReport])
def process_text_custom_options(
    analyzer_options: AnalyzerOptions,
    input_text: str = Query(
        default="", example="João e Maria são ótimos amigos", max_length=10000
    ),
):
    return Feedbacks(analyzer_options.dict()).find_avoided_expression(
        input_text
    )
