def test_series_tag_is_assigned(articles_with_series):
    series_tags = [i.metadata["series"] for i in articles_with_series]

    assert set(series_tags) == set(["test_series"])


def test_first_article_series(articles_with_series):
    article = articles_with_series[0]

    assert article.series["index"] == 1
    assert len(article.series["all"]) == 3
    assert len(article.series["all_previous"]) == 0
    assert len(article.series["all_next"]) == 2
    assert article.series["previous"] is None
    assert article.series["next"] == articles_with_series[1]


def test_middle_article_series(articles_with_series):
    article = articles_with_series[1]

    assert article.series["index"] == 2
    assert len(article.series["all"]) == 3
    assert len(article.series["all_previous"]) == 1
    assert len(article.series["all_next"]) == 1
    assert article.series["previous"] == articles_with_series[0]
    assert article.series["next"] == articles_with_series[2]


def test_last_article_series(articles_with_series):
    article = articles_with_series[2]

    assert article.series["index"] == 3
    assert len(article.series["all"]) == 3
    assert len(article.series["all_previous"]) == 2
    assert len(article.series["all_next"]) == 0
    assert article.series["previous"] == articles_with_series[1]
    assert article.series["next"] is None
