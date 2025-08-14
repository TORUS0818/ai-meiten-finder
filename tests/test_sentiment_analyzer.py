import pytest
from unittest.mock import MagicMock
from src.ai_meiten_finder.sentiment_analyzer import calculate_review_score

# テストケースを定義
test_cases = [
    (
        "positive_reviews",  # test_id
        ["とても良い商品でした。", "素晴らしいサービスです。"],  # reviews
        [
            [{"label": "positive", "score": 0.9}],
            [{"label": "positive", "score": 0.8}],
        ],  # mock_return
        (0.9 + 0.8) / 2,  # expected_score
    ),
    (
        "negative_reviews",
        ["最悪でした。", "がっかりです。"],
        [[{"label": "negative", "score": 0.7}], [{"label": "negative", "score": 0.6}]],
        (-0.7 - 0.6) / 2,
    ),
    (
        "mixed_reviews",
        ["良いです。", "悪い。", "普通。"],
        [
            [{"label": "positive", "score": 0.9}],
            [{"label": "negative", "score": 0.7}],
            [{"label": "positive", "score": 0.5}],
        ],
        (0.9 - 0.7 + 0.5) / 3,
    ),
    (
        "empty_list",
        [],
        [],
        None,
    ),
    (
        "neutral_average",
        ["良い", "悪い"],
        [[{"label": "positive", "score": 0.8}], [{"label": "negative", "score": 0.8}]],
        0.0,
    ),
]


@pytest.mark.parametrize(
    "test_id, reviews, mock_return, expected_score",
    test_cases,
    ids=[case[0] for case in test_cases],  # test_idをテスト名として使用
)
def test_calculate_review_score(
    test_id, reviews, mock_return, expected_score, monkeypatch
):
    """
    様々なレビューリストに対するスコア計算をテスト
    """
    mock_sentiment_pipeline = MagicMock()
    monkeypatch.setattr(
        "src.ai_meiten_finder.sentiment_analyzer.sentiment_pipeline",
        mock_sentiment_pipeline,
    )

    if not reviews:
        assert calculate_review_score(reviews) is None
        mock_sentiment_pipeline.assert_not_called()
        return

    mock_sentiment_pipeline.side_effect = mock_return

    assert calculate_review_score(reviews) == pytest.approx(expected_score)
    assert mock_sentiment_pipeline.call_count == len(reviews)
