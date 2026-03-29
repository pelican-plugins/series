def test_draft_article_gets_series_metadata(articles_with_draft):
    generator, _ = articles_with_draft

    # The draft should be in generator.drafts, not generator.articles
    assert len(generator.drafts) == 1
    draft = generator.drafts[0]

    # The draft's series attribute should be a dict, not a raw string
    assert isinstance(draft.series, dict), (
        f"Draft article's series is {type(draft.series).__name__}, "
        "expected dict with series metadata"
    )
    assert draft.series["name"] == "test_series"


def test_draft_is_included_in_series_ordering(articles_with_draft):
    generator, _ = articles_with_draft
    draft = generator.drafts[0]

    # The series should contain all 3 articles (2 published + 1 draft)
    assert len(draft.series["all"]) == 3


def test_published_articles_see_draft_in_series(articles_with_draft):
    _, articles = articles_with_draft

    # Published articles should also have all 3 in their series
    for article in articles:
        assert len(article.series["all"]) == 3


def test_draft_series_navigation(articles_with_draft):
    generator, _ = articles_with_draft
    draft = generator.drafts[0]

    # Draft is article 2 (by date), so it should have previous and next
    assert draft.series["index"] == 2
    assert draft.series["previous"] is not None
    assert draft.series["next"] is not None


def test_draft_not_in_context_series(articles_with_draft):
    generator, _ = articles_with_draft

    # Context series exists
    assert "test_series" in generator.context["series"]
