Series: A Plugin for Pelican
============================

[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/series/main.yml?branch=main)](https://github.com/pelican-plugins/series/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-series)](https://pypi.org/project/pelican-series/)
[![Downloads](https://img.shields.io/pypi/dm/pelican-series)](https://pypi.org/project/pelican-series/)
![License](https://img.shields.io/pypi/l/pelican-series?color=blue)

Series is a Pelican plugin that joins multiple posts into a series. Globally, it provides a list of all the series, and for each article it provides a list of all articles in the same series and links to the next and previous articles in the series.

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-series

As long as you have not explicitly added a `PLUGINS` setting to your Pelican settings file, then the newly-installed plugin should be automatically detected and enabled. Otherwise, you must add `series` to your existing `PLUGINS` list. For more information, please see the [How to Use Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) documentation.

Usage
-----

In order to mark reStructuredText-formatted posts as part of a series, use the `:series:` metadata:

    :series:  NAME_OF_THIS_SERIES

Or, for Markdown-formatted content:

    Series: NAME_OF_THIS_SERIES

The plugin collects all articles or pages belonging to the same series and provides series-related variables that you can use in your template.

Articles and pages
------------------

This plugin works both with articles and pages. As Pelican uses the specific variable `article` for article templates and `page` for page templates it is complicated to give examples that work for both cases. In the following documentation all example will mention `article.` (e.g. `article.series`, `article.title`) but the code works in the same way with `page` (e.g. `page.series`, `page.title`).

Article series and page series are created separately, so even if an article and a page have the same series they won't appear together.

Indexing
--------

By default, articles in a series are ordered by date and then automatically numbered. Pages in a series are ordered by title and automatically numbered.

If you want to force a given order, specify `:series_index:` (reST) or `series_index:` (Markdown) in the article metadata, starting from 1. All articles with this enforced index are put at the beginning of the series and ordered according to the index itself. All the remaining articles come after them, ordered with the default ordering (date for articles and title for pages).

The plugin provides the following variables to your templates:

* `article.series.name` is the name of the series as specified in the article metadata
* `article.series.index` is the index of the current article inside the series
* `article.series.all` is an ordered list of all articles in the series (including the current one)
* `article.series.all_previous` is an ordered list of the articles published before the current one
* `article.series.all_next` is an ordered list of the articles published after the current one
* `article.series.previous` is the previous article in the series (a shortcut to `article.series.all_previous[-1]`) or `None` for the first article
* `article.series.next` is the next article in the series (a shortcut to `article.series.all_next[0]`) or `None` for the last one

For example:

```html+jinja
{% if article.series %}
    <p>This post is part {{ article.series.index }} of the "{{ article.series.name }}" series:</p>
    <ol class="parts">
        {% for part_article in article.series.all %}
            <li {% if part_article == article %}class="active"{% endif %}>
                <a href='{{ SITEURL }}/{{ part_article.url }}'>{{ part_article.title }}</a>
            </li>
        {% endfor %}
    </ol>
{% endif %}
```

Global Context
--------------

**Warning**: in version 3 the global key `series` has been renamed to `article_series` to differentiate it from the new global key `page_series`.

The plugin also adds the keys `article_series` and `page_series` to the global context. They are dictionaries of all series names (as keys) and items (as values). You can use that to list all the series in your site, for example

```html+jinja
{% for series_name, series_articles in article_series.items() %}
{% set article = series_articles[0] %}
<article class="card">
	<a href="{{ article.url }}" class="image">
		<img src="/images/{{ article.image }}.jpg" alt="{{ article.image }}" />
	</a>
	<div class="card-body">
    	<a href="{{ article.url }}"><h3 class="card-title">{{ series_name }}</h3></a>
     	<ul class="actions">
     		<li><a href="{{ article.url }}" class="button">Start</a></li>
     	</ul>
	</div>
</article>
{% endfor %}
```

As it is not possible to create pages from plugins you can leverage it to create a page for a specific series, even though you have to hard code the name of the series in the template.

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/series/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the AGPL 3.0 license.
