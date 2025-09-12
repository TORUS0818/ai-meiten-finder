import pprint

from transformers import pipeline


def classify_reviews():
    """
    ゼロショット分類モデルを使って、レビューがどのカテゴリに属するかを判定するデモ。
    """
    print(
        'ゼロショット分類パイプラインを準備しています...（初回はモデルのダウンロードに時間がかかります）'
    )
    # ゼロショット分類のパイプラインを準備
    classifier = pipeline(
        'zero-shot-classification',
        model='MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7',
    )
    print('パイプラインの準備が完了しました。')

    reviews = [
        'ラーメンは美味しかったけど、店員の態度が最悪だった。',
        'お店の雰囲気が良くて、ゆっくり過ごせました。',
        '値段の割に、量が少なくてがっかり。',
        'とにかくスープの味が絶品。また来たい。',
        '駅から遠いのが少し難点かな。',
    ]

    candidate_labels = ['味の評価', '接客の評価', '店の雰囲気', '料金', '立地']

    # hypothesis_templateのおまじないを入れると精度が上がります
    hypothesis_template = 'この文章のトピックは{}です。'

    print('\n--- 分類結果 ---')
    for review in reviews:
        print(f'\nレビュー: 「{review}」')
        output = classifier(
            review, candidate_labels, hypothesis_template=hypothesis_template
        )
        # 結果を整形して表示
        pprint.pprint(output)


if __name__ == '__main__':
    classify_reviews()
