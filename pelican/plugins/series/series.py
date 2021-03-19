"""
Series
======

This plugin extends the original series plugin
by FELD Boris <lothiraldan@gmail.com>

Joins articles in a series and provides variables to
manage the series in the template.
"""

from collections import defaultdict
from operator import itemgetter

from pelican import signals


def aggregate_series(generator):
    series = defaultdict(list)

    # This cycles through all articles in the given generator
    # and collects the 'series' metadata, if present.
    # The 'series_index' metadata is also stored, if specified
    for article in generator.articles:

        if "series" in article.metadata:
            article_entry = {
                "index": article.metadata.get("series_index", None),
                "date": article.metadata["date"],
                "content": article,
            }

            series[article.metadata["series"]].append(article_entry)

    for series_name, series_articles in series.items():
        forced_order_articles = [i for i in series_articles if i["index"] is not None]
        forced_order_articles.sort(key=itemgetter("index"))

        date_order_articles = [i for i in series_articles if i["index"] is None]
        date_order_articles.sort(key=itemgetter("date"))

        all_articles = forced_order_articles + date_order_articles
        ordered_articles = [i["content"] for i in all_articles]

        for index, article in enumerate(ordered_articles):
            article.series = {
                "name": series_name,
                "index": index + 1,
                "all": ordered_articles,
                "all_previous": ordered_articles[0:index],
                "all_next": ordered_articles[index + 1 :],
            }

            if index > 0:
                article.series["previous"] = ordered_articles[index - 1]
            else:
                article.series["previous"] = None

            try:
                article.series["next"] = ordered_articles[index + 1]
            except IndexError:
                article.series["next"] = None


def register():
    signals.article_generator_finalized.connect(aggregate_series)
