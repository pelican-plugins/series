def test_series_is_assigned_to_articles(articles_with_index):
    _, articles = articles_with_index
    series_names = [i.series["name"] for i in articles]

    assert len(set(series_names)) == 1
    assert series_names[0] == "test_series"


def test_first_article_series(articles_with_index):
    _, articles = articles_with_index
    article = articles[0]

    assert article.series["index"] == 3
    assert len(article.series["all"]) == 3
    assert len(article.series["all_previous"]) == 2
    assert len(article.series["all_next"]) == 0
    assert article.series["previous"] == articles[1]
    assert article.series["next"] is None


def test_middle_article_series(articles_with_index):
    _, articles = articles_with_index
    article = articles[1]

    assert article.series["index"] == 2
    assert len(article.series["all"]) == 3
    assert len(article.series["all_previous"]) == 1
    assert len(article.series["all_next"]) == 1
    assert article.series["previous"] == articles[2]
    assert article.series["next"] == articles[0]


def test_last_article_series(articles_with_index):
    _, articles = articles_with_index
    article = articles[2]

    assert article.series["index"] == 1
    assert len(article.series["all"]) == 3
    assert len(article.series["all_previous"]) == 0
    assert len(article.series["all_next"]) == 2
    assert article.series["previous"] is None
    assert article.series["next"] == articles[1]
