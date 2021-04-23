from operator import attrgetter
import os

import pytest

from pelican.generators import ArticlesGenerator
from pelican.tests.support import get_context, get_settings

from . import series


def create_generator(data_path, sort_key=None):
    @pytest.fixture
    def _create_generator(tmp_path):
        series.register()

        settings = get_settings()
        settings["CACHE_CONTENT"] = False
        settings["PLUGINS"] = [series]

        context = get_context(settings)

        base_path = os.path.dirname(os.path.abspath(__file__))
        test_data_path = os.path.join(base_path, data_path)

        generator = ArticlesGenerator(
            context=context,
            settings=settings,
            path=test_data_path,
            theme=settings["THEME"],
            output_path=tmp_path,
        )

        generator.generate_context()

        items = generator.articles

        if sort_key:
            items = sorted(items, key=sort_key)

        return generator, items

    return _create_generator


articles_no_index = create_generator("test_data/articles_no_index", attrgetter("date"))
articles_with_index = create_generator(
    "test_data/articles_with_index", attrgetter("date")
)
