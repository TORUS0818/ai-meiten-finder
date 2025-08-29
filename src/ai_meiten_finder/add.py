from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from scraper import search_restaurant_reviews
from sentiment_analyzer import calculate_review_score

load_dotenv()


app = FastAPI(title="Restaurant Sentiment API", version="1.0.0")


class ReviewScore(BaseModel):
    text: str
    score: float


class RestaurantScoreResponse(BaseModel):
    display_name: str
    review_score: float
    review_sentences: list[str]


@app.get("/score/search", response_model=RestaurantScoreResponse)
def score_restaurant(
    query: str,
    language_code: str = "ja",
    region_code: str = "JP",
    page_size: int = 5,
):
    reviews = search_restaurant_reviews(
        query,
        language_code=language_code,
        region_code=region_code,
        page_size=page_size,
    )
    if not reviews or not reviews.review_sentences:
        raise HTTPException(status_code=404, detail="レビューが見つかりませんでした。")
    review_score = calculate_review_score(reviews.review_sentences)
    return RestaurantScoreResponse(
        display_name=reviews.display_name,
        review_score=review_score,
        review_sentences=reviews.review_sentences,
    )
