from src.ai_meiten_finder.sentiment_analyzer import calculate_review_score

if __name__ == "__main__":
    print("感情分析デモンストレーションを開始します。")

    # ポジティブなレビューの例
    positive_reviews = [
        "このお店の料理は本当に美味しいです！",
        "店員さんの対応が素晴らしく、また来たいと思いました。",
        "雰囲気が良くて、ゆっくり過ごせました。",
    ]
    positive_score = calculate_review_score(positive_reviews)
    print(f"\nポジティブなレビューのスコア: {positive_score:.2f}")

    # ネガティブなレビューの例
    negative_reviews = [
        "料理が冷めていて残念でした。",
        "サービスが悪く、不快な思いをしました。",
        "店内が騒がしくて落ち着けませんでした。",
    ]
    negative_score = calculate_review_score(negative_reviews)
    print(f"\nネガティブなレビューのスコア: {negative_score:.2f}")

    # 空のレビューリストの例
    empty_reviews = []
    empty_score = calculate_review_score(empty_reviews)
    print(f"\n空のレビューリストのスコア: {empty_score}")

    print("\nデモンストレーションを終了します。")
