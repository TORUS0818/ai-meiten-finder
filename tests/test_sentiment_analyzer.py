import pytest
from unittest.mock import MagicMock
from src.ai_meiten_finder.sentiment_analyzer import calculate_review_score


def test_calculate_review_score_empty_reviews(monkeypatch):
    """
    空のレビューリストが渡された場合にNoneを返すことをテスト
    """
    mock_sentiment_pipeline = MagicMock()
    monkeypatch.setattr(
        'src.ai_meiten_finder.sentiment_analyzer.sentiment_pipeline',
        mock_sentiment_pipeline,
    )

    assert calculate_review_score([]) is None
    mock_sentiment_pipeline.assert_not_called()


def test_calculate_review_score_positive_reviews(monkeypatch):
    """
    ポジティブなレビューのスコアが正しく計算されることをテスト
    """
    mock_sentiment_pipeline = MagicMock()
    monkeypatch.setattr(
        'src.ai_meiten_finder.sentiment_analyzer.sentiment_pipeline',
        mock_sentiment_pipeline,
    )

    # モックされたpipelineの戻り値を設定
    mock_sentiment_pipeline.side_effect = [
        [{'label': 'POSITIVE', 'score': 0.9}],
        [{'label': 'POSITIVE', 'score': 0.8}],
    ]

    reviews = ['とても良い商品でした。', '素晴らしいサービスです。']
    expected_score = (0.9 + 0.8) / 2
    assert calculate_review_score(reviews) == pytest.approx(expected_score)
    assert mock_sentiment_pipeline.call_count == len(reviews)


def test_calculate_review_score_negative_reviews(monkeypatch):
    """
    ネガティブなレビューのスコアが正しく計算されることをテスト
    """
    mock_sentiment_pipeline = MagicMock()
    monkeypatch.setattr(
        'src.ai_meiten_finder.sentiment_analyzer.sentiment_pipeline',
        mock_sentiment_pipeline,
    )

    mock_sentiment_pipeline.side_effect = [
        [{'label': 'NEGATIVE', 'score': 0.7}],
        [{'label': 'NEGATIVE', 'score': 0.6}],
    ]
    reviews = ['最悪でした。', 'がっかりです。']
    expected_score = (-0.7 + -0.6) / 2
    assert calculate_review_score(reviews) == pytest.approx(expected_score)
    assert mock_sentiment_pipeline.call_count == len(reviews)


def test_calculate_review_score_neutral_reviews(monkeypatch):
    """
    中立なレビューのスコアが正しく計算されることをテスト
    """
    mock_sentiment_pipeline = MagicMock()
    monkeypatch.setattr(
        'src.ai_meiten_finder.sentiment_analyzer.sentiment_pipeline',
        mock_sentiment_pipeline,
    )

    mock_sentiment_pipeline.side_effect = [
        [{'label': 'NEUTRAL', 'score': 0.5}],
        [{'label': 'NEUTRAL', 'score': 0.4}],
    ]
    reviews = ['特に問題ありません。', '普通でした。']
    expected_score = (0.0 + 0.0) / 2  # NEUTRALは0として扱われる
    assert calculate_review_score(reviews) == pytest.approx(expected_score)
    assert mock_sentiment_pipeline.call_count == len(reviews)


def test_calculate_review_score_mixed_reviews(monkeypatch):
    """
    ポジティブ、ネガティブ、中立が混ざったレビューのスコアが正しく計算されることをテスト
    """
    mock_sentiment_pipeline = MagicMock()
    monkeypatch.setattr(
        'src.ai_meiten_finder.sentiment_analyzer.sentiment_pipeline',
        mock_sentiment_pipeline,
    )

    mock_sentiment_pipeline.side_effect = [
        [{'label': 'POSITIVE', 'score': 0.9}],
        [{'label': 'NEGATIVE', 'score': 0.7}],
        [{'label': 'NEUTRAL', 'score': 0.5}],
    ]
    reviews = ['良いです。', '悪い。', '普通。']
    expected_score = (0.9 + (-0.7) + 0.0) / 3
    assert calculate_review_score(reviews) == pytest.approx(expected_score)
    assert mock_sentiment_pipeline.call_count == len(reviews)
