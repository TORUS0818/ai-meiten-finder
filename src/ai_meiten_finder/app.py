from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from ai_meiten_finder.scraper import search_restaurant_reviews
from ai_meiten_finder.sentiment_analyzer import calculate_review_score

import logging
import structlog

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(message)s",
)

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger(__name__)

load_dotenv()

app = FastAPI(title="Restaurant Sentiment API", version="1.0.0")


class ReviewScore(BaseModel):
    text: str
    score: float


class RestaurantScoreResponse(BaseModel):
    display_name: str
    review_score: float | None
    review_sentences: list[str]


@app.get("/score/search", response_model=RestaurantScoreResponse)
def score_restaurant(
    query: str,
    language_code: str = "ja",
    region_code: str = "JP",
    page_size: int = 5,
):
    # ▼ ここを try/except で保護（外部API失敗に対応）
    try:
        reviews = search_restaurant_reviews(
            query,
            language_code=language_code,
            region_code=region_code,
            page_size=page_size,
        )
    except HTTPException:  # もし内部で HTTPException を投げる実装なら通す
        logger.error(
            "search_reviews_error",
            kind="http_exception_from_search",
            query=query,
            language_code=language_code,
            region_code=region_code,
            page_size=page_size,
            exc_info=True,
        )
        raise
    except Exception as e:
        logger.error(
            "search_reviews_error",
            status_code=502,
            kind="external_api_error_in_search",
            error=str(e),
            query=query,
            language_code=language_code,
            region_code=region_code,
            page_size=page_size,
            exc_info=True,  # スタックトレースをJSONに
        )
        raise HTTPException(
            status_code=502,
            detail="レビュー検索の外部APIでエラーが発生しました。しばらくしてから再度お試しください。",
        )

    if not reviews or not reviews.review_sentences:
        logger.warning(
            "score_restaurant_response",
            status_code=404,
            detail="レビューが見つかりませんでした。",
            query=query,
            language_code=language_code,
            region_code=region_code,
            page_size=page_size,
        )
        raise HTTPException(status_code=404, detail="レビューが見つかりませんでした。")

    review_score = calculate_review_score(reviews.review_sentences)

    logger.info(
        "score_restaurant_response",
        status_code=200,
        display_name=reviews.display_name,
        review_score=review_score,
        review_sentences=reviews.review_sentences,
        query=query,
        language_code=language_code,
        region_code=region_code,
        page_size=page_size,
    )
    return RestaurantScoreResponse(
        display_name=reviews.display_name,
        review_score=review_score,
        review_sentences=reviews.review_sentences,
    )
