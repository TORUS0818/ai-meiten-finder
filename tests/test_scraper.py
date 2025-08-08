import src.ai_meiten_finder.scraper as sm


def test_extract_helper():
    place = sm.Place.model_validate(
        {
            "displayName": {"text": "Foo"},
            "reviews": [{"text": {"text": "bar"}}],
        }
    )
    review = sm._extract_restaurant_name_and_reviews_from(place)
    assert review.display_name == "Foo"
    assert review.review_sentences == ["bar"]
