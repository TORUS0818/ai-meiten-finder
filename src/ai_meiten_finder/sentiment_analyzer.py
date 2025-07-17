from transformers.pipelines import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 感情分析パイプラインをモジュールレベルで初期化（モジュール読み込み時に一度だけ実行）
model_name = 'llm-book/bert-base-japanese-v3-marc_ja'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_pipeline = pipeline(
    'sentiment-analysis',
    model=model,
    tokenizer=tokenizer,
)  # type: ignore


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
        result = sentiment_pipeline(review)  # type: ignore
        # 結果は [{'label': 'POSITIVE', 'score': 0.9998}] のような形式
        # 'POSITIVE' ならスコアをそのまま、'NEGATIVE' ならスコアを反転して使用
        if result[0]['label'] == 'POSITIVE':
            scores.append(result[0]['score'])
        elif result[0]['label'] == 'NEGATIVE':
            scores.append(-result[0]['score'])
        # 'NEUTRAL' の場合はスコアを0として扱うか、含めないか、要件による
        # 今回は簡易的にPOSITIVE/NEGATIVEのみを考慮
        else:
            scores.append(0.0)  # NEUTRALの場合

    return sum(scores) / len(scores)
