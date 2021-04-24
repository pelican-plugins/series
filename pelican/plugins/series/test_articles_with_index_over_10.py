def test_series_is_assigned_to_articles(articles_with_index_over_10):
    _, articles = articles_with_index_over_10
    series_names = [i.series["name"] for i in articles]

    assert len(set(series_names)) == 1
    assert series_names[0] == "test_series"


def test_last_article_series(articles_with_index_over_10):
    _, articles = articles_with_index_over_10
    article = articles[-1]

    assert article.series["index"] == 4
    assert len(article.series["all"]) == 4
    assert len(article.series["all_previous"]) == 3
    assert len(article.series["all_next"]) == 0
    assert article.series["previous"] == articles[-2]
    assert article.series["next"] is None
