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
        [{'label': 'positive', 'score': 0.9}],
        [{'label': 'positive', 'score': 0.8}],
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
        [{'label': 'negative', 'score': 0.7}],
        [{'label': 'negative', 'score': 0.6}],
    ]
    reviews = ['最悪でした。', 'がっかりです。']
    expected_score = (-0.7 + -0.6) / 2
    assert calculate_review_score(reviews) == pytest.approx(expected_score)
    assert mock_sentiment_pipeline.call_count == len(reviews)


def test_calculate_review_score_mixed_reviews(monkeypatch):
    """
    ポジティブ、ネガティブが混ざったレビューのスコアが正しく計算されることをテスト
    (2値分類モデルの特性を考慮)
    """
    mock_sentiment_pipeline = MagicMock()
    monkeypatch.setattr(
        'src.ai_meiten_finder.sentiment_analyzer.sentiment_pipeline',
        mock_sentiment_pipeline,
    )

    # 2値分類モデルなので、中立的なレビューもpositiveかnegativeに分類されると仮定
    mock_sentiment_pipeline.side_effect = [
        [{'label': 'positive', 'score': 0.9}],
        [{'label': 'negative', 'score': 0.7}],
        [
            {'label': 'positive', 'score': 0.5}
        ],  # 「普通」のレビューがpositiveに分類されたと仮定
    ]
    reviews = ['良いです。', '悪い。', '普通。']
    expected_score = (
        0.9 + (-0.7) + 0.5
    ) / 3  # 0.5は「普通」のレビューがpositiveとされたスコア
    assert calculate_review_score(reviews) == pytest.approx(expected_score)
    assert mock_sentiment_pipeline.call_count == len(reviews)
