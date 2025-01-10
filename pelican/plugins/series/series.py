"""Series plugin for Pelican.

This plugin extends the original series plugin
by FELD Boris <lothiraldan@gmail.com>

Joins articles in a series and provides variables to
manage the series in the template.
"""

from collections import defaultdict
from operator import itemgetter

from pelican import signals

ordered_articles_all = {}
ordered_pages_all = {}


def generate_serie(series_name, series_items, sort_key):
    forced_order_items = [i for i in series_items if i["index"] != 0]
    forced_order_items.sort(key=itemgetter("index"))

    custom_order_items = [i for i in series_items if i["index"] == 0]
    custom_order_items.sort(key=itemgetter(sort_key))

    all_items = forced_order_items + custom_order_items
    ordered_items = [i["content"] for i in all_items]

    for index, page in enumerate(ordered_items):
        page.series = {
            "name": series_name,
            "index": index + 1,
            "all": ordered_items,
            "all_previous": ordered_items[0:index],
            "all_next": ordered_items[index + 1 :],
            "lang": "en",
        }

        if index > 0:
            page.series["previous"] = ordered_items[index - 1]
        else:
            page.series["previous"] = None

        try:
            page.series["next"] = ordered_items[index + 1]
        except IndexError:
            page.series["next"] = None

    return ordered_items


def aggregate_series(generator):
    generator.context["series"] = {}

    series = defaultdict(list)

    # This cycles through all articles in the given generator
    # and collects the 'series' metadata, if present.
    # The 'series_index' metadata is also stored, if specified
    translations = defaultdict(dict)
    more = []
    for article in generator.articles:
        for trans in article.translations:
            more.append(trans)
    for article in generator.articles + more:
        if "series" in article.metadata:
            article_entry = {
                "index": int(article.metadata.get("series_index", 0)),
                "date": article.metadata["date"],
                "content": article,
                "lang": article.metadata.get("lang", generator.context['DEFAULT_LANG']),
            }

            series[article.metadata["series"]].append(article_entry)
    for series_name, series_items in series.items():
        translations = defaultdict(list)
        for item in series_items:
            translations[item["lang"]].append(item)
        default_language_series_items = []
        for lang, series in translations.items():
            ordered_items = generate_serie(series_name, series, "date")
            if lang == generator.context['DEFAULT_LANG']:
                default_language_series_items = ordered_items

        generator.context["series"][series_name] = default_language_series_items
        ordered_articles_all[series_name] = default_language_series_items


def aggregate_series_pages(generator):
    generator.context["series"] = {}

    series = defaultdict(list)

    for page in generator.pages:
        if "series" in page.metadata:
            page_entry = {
                "index": int(page.metadata.get("series_index", 0)),
                "content": page,
            }

            series[page.metadata["series"]].append(page_entry)

    for series_name, series_items in series.items():
        ordered_items = generate_serie(series_name, series_items, "title")

        generator.context["series"][series_name] = ordered_items
        ordered_pages_all[series_name] = ordered_items


def onGeneratorsFinalized(generators):
    for generator in generators:
        generator.context["article_series"] = ordered_articles_all
        generator.context["page_series"] = ordered_pages_all


def register():
    signals.article_generator_finalized.connect(aggregate_series)
    signals.page_generator_finalized.connect(aggregate_series_pages)
    signals.all_generators_finalized.connect(onGeneratorsFinalized)
