import os
import argparse
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import structlog
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(message)s",
)

structlog.configure(
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
)

logger = structlog.get_logger(__name__)

load_dotenv()
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
if not GOOGLE_PLACES_API_KEY:
    raise RuntimeError("GOOGLE_PLACES_API_KEY is not set")

SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"


class ReviewText(BaseModel):
    text: str


class Review(BaseModel):
    text: ReviewText


class DisplayName(BaseModel):
    text: str


class Place(BaseModel):
    id: str | None = None
    display_name: DisplayName = Field(alias="displayName")
    reviews: list[Review] = []


class SearchResponse(BaseModel):
    places: list[Place] = []


class RestaurantReviews(BaseModel):
    display_name: str
    review_sentences: list[str]


def search_restaurant_reviews(
    text_query: str,
    *,
    language_code: str = "ja",
    region_code: str = "JP",
    page_size: int = 1,
) -> RestaurantReviews | None:
    """テキスト検索で最上位候補 reviewのうち5件と、その要約を返す"""
    if not text_query:
        logger.error("empty_text_query")
        raise ValueError("text_query must be non-empty")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": ",".join(
            [
                "places.id",
                "places.displayName",
                "places.reviews.text.text",
                "places.reviewSummary",
            ]
        ),
    }
    body = {
        "textQuery": text_query,
        "includedType": "restaurant",
        "languageCode": language_code,
        "regionCode": region_code,
        "pageSize": page_size,
    }

    try:
        r = requests.post(SEARCH_URL, headers=headers, json=body, timeout=30)
        r.raise_for_status()
        parsed_response = SearchResponse.model_validate(r.json())
        if not parsed_response.places:
            logger.info(
                "search_restaurant_reviews_not_found",
                text_query=text_query,
                page_size=page_size,
                status_code=r.status_code,
            )
            return None

        place = parsed_response.places[0]
        result = _extract_restaurant_name_and_reviews_from(place)
        logger.info(
            "search_restaurant_reviews_success",
            text_query=text_query,
            page_size=page_size,
            status_code=r.status_code,
            place_id=place.id,
            place_name=place.display_name.text,
            review_count=len(place.reviews),
        )
        return result

    except requests.HTTPError as e:
        logger.error(
            "search_restaurant_reviews_http_error",
            text_query=text_query,
            page_size=page_size,
            status_code=e.response.status_code,
            response_text=e.response.text,
            exc_info=True,
        )
        raise


def _extract_restaurant_name_and_reviews_from(place: Place) -> RestaurantReviews:
    """place から、レビューの関連性の高いもの最大5件(Google APIの仕様)を抽出する"""
    display_name = place.display_name.text
    review_sentences = []
    for review in place.reviews:
        review_sentences.append(review.text.text)
    return RestaurantReviews(
        display_name=display_name,
        review_sentences=review_sentences,
    )


def main():
    parser = argparse.ArgumentParser(description="Places API(New) で口コミを取�?")
    parser.add_argument(
        "--query",
        help="店名などのテキスト（店名: 'スターバックス 渋谷駅前",
        required=True,
    )
    args = parser.parse_args()
    reviews = search_restaurant_reviews(
        args.query,
    )
    return reviews


if __name__ == "__main__":
    main()
