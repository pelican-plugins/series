Series: A Plugin for Pelican
============================

[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/series/build)](https://github.com/pelican-plugins/series/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-series)](https://pypi.org/project/pelican-series/)
![License](https://img.shields.io/pypi/l/pelican-series?color=blue)

Series is a Pelican plugin that joins multiple posts into a series.

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-series

Usage
-----

In order to mark reStructuredText-formatted posts as part of a series, use the `:series:` metadata:

    :series:  NAME_OF_THIS_SERIES

Or, for Markdown-formatted content:

    Series: NAME_OF_THIS_SERIES

The plugin collects all articles belonging to the same series and provides series-related variables that you can use in your template.

Indexing
--------

By default, articles in a series are ordered by date and then automatically numbered.

If you want to force a given order, specify the `:series_index:` (reST) or `series_index:` (Markdown) metadata, starting from 1. All articles with this enforced index are put at the beginning of the series and ordered according to the index itself. All the remaining articles come after them, ordered by date.

The plugin provides the following variables to your templates:

* `article.series.name` is the name of the series as specified in the article metadata
* `article.series.index` is the index of the current article inside the series
* `article.series.all` is an ordered list of all articles in the series (including the current one)
* `article.series.all_previous` is an ordered list of the articles published before the current one
* `article.series.all_next` is an ordered list of the articles published after the current one
* `article.series.previous` is the previous article in the series (a shortcut to `article.series.all_previous[-1]`)
* `article.series.next` is the next article in the series (a shortcut to `article.series.all_next[0]`)

For example:

```jinja
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

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/series/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the AGPL 3.0 license.
