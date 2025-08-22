from transformers.pipelines import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "llm-book/bert-base-japanese-v3-marc_ja"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_pipeline = pipeline(
    "sentiment-analysis",
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
    if not reviews:
        return None

    scores = []
    for review in reviews:
        result = sentiment_pipeline(review)
        if result[0]["label"] == "positive":
            scores.append(result[0]["score"])
        elif result[0]["label"] == "negative":
            scores.append(-result[0]["score"])

    return sum(scores) / len(scores)
