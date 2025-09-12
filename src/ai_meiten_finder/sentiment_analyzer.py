from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers.pipelines import pipeline

from .logger import get_logger

logger = get_logger(__name__)

model_name = 'llm-book/bert-base-japanese-v3-marc_ja'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_pipeline = pipeline(
    'sentiment-analysis',
    model=model,
    tokenizer=tokenizer,
)


def calculate_review_score(reviews: list[str]) -> float | None:
    """
    レビューのリストを受け取り、感情分析モデルで評価したスコアを平均化して返します。

    Args:
        reviews (list[str]): 感情分析を行うレビューの文字列のリスト。

    Returns:
        float: レビューの感情スコアの平均値。スコアは-1（非常にネガティブ）から1（非常にポジティブ）の範囲。
               レビューがない場合はNoneを返します。
    """
    logger.info('sentiment_analysis_start', review_count=len(reviews) if reviews else 0)

    if not reviews:
        logger.warning('sentiment_analysis_empty_reviews')
        return None

    try:
        scores = []
        for review in reviews:
            result = sentiment_pipeline(review)
            if result[0]['label'] == 'positive':
                scores.append(result[0]['score'])
            elif result[0]['label'] == 'negative':
                scores.append(-result[0]['score'])

        if not scores:
            logger.warning('sentiment_analysis_no_valid_scores')
            return None

        final_score = sum(scores) / len(scores)

        logger.info(
            'sentiment_analysis_complete',
            final_score=final_score,
            valid_reviews=len(scores),
            total_reviews=len(reviews),
        )

        return final_score

    except Exception as e:
        logger.error(
            'sentiment_analysis_error',
            error=str(e),
            review_count=len(reviews),
            exc_info=True,
        )
        raise
