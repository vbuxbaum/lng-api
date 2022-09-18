from typing import List
from fastapi import FastAPI, Query
from feedbacks.feedbacks import Feedbacks, LNGReport

app = FastAPI(title="LNG API")

feedback_handler = Feedbacks()


@app.get("/", response_model=List[LNGReport])
def process_text(
    input_text: str = Query(
        default="", example="João e Maria são ótimos amigos", lt=10000
    )
):
    return feedback_handler.find_avoided_expression(input_text)
