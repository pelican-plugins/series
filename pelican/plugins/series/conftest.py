from operator import attrgetter
import os

import pytest

from pelican.generators import ArticlesGenerator
from pelican.tests.support import get_context, get_settings, temporary_folder

from . import series


@pytest.fixture
def tmp_folder():
    with temporary_folder() as tf:
        yield tf


@pytest.fixture
def articles_with_series(tmp_folder):
    series.register()
    settings = get_settings()
    settings["CACHE_CONTENT"] = False
    settings["PLUGINS"] = [series]
    context = get_context(settings)

    base_path = os.path.dirname(os.path.abspath(__file__))
    test_data_path = os.path.join(base_path, "test_data")

    generator = ArticlesGenerator(
        context=context,
        settings=settings,
        path=test_data_path,
        theme=settings["THEME"],
        output_path=tmp_folder,
    )

    generator.generate_context()

    # Test articles are in the same series in order of date
    return sorted(generator.articles, key=attrgetter("date"))
