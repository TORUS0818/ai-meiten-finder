import pytest
import src.ai_meiten_finder.scraper as scraper


@pytest.fixture
def mock_html_content():
    return """
    <html>
        <body>
            <div class="rvw-item__rvw-comment">美味しすぎる</div>
            <div class="rvw-item__rvw-comment">まずい</div>
            <div class="rvw-item__rvw-comment">サービスがいまいち</div>
        </body>
    </html>
    """


def test_find_reviews(mock_html_content):
    reviews = scraper.find_reviews(mock_html_content)
    assert len(reviews) == 3
    assert reviews[0] == "美味しすぎる"
    assert reviews[1] == "まずい"
    assert reviews[2] == "サービスがいまいち"
