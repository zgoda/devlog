import os
from datetime import datetime

import pytest

from devlog.models import Post
from devlog.tasks import post_from_markdown, app, sitemap_generator


@pytest.mark.usefixtures('app')
class TestPostImport:

    def test_import_ok(self):
        md = '''---
title: Wpis testowy
date: 2020-06-21T18:24:12
tags:
  - tag1
  - tag2
author: Test Testowy
---

Pierwsza linijka tekstu, zawierająca *markup*.

<!-- more -->

Druga linijka tekstu, zawierająca *markup*.
'''
        post_from_markdown(md)
        rv = Post.get()
        assert rv.title == 'Wpis testowy'
        assert '<em>' in rv.summary
        assert len(rv.tags()) == 2

    @pytest.mark.parametrize('text', [
        '---\nauthor: somebody\n---\n\nSome text',
        'Some text',
    ], ids=['missing-title', 'missing-meta'])
    def test_invalid_meta(self, text):
        with pytest.raises(ValueError):
            post_from_markdown(text)

    def test_import_no_date(self, mocker):
        dt = datetime(2020, 6, 12, 18, 34, 12)
        mocker.patch(
            'devlog.utils.text._get_now', mocker.Mock(return_value=dt),
        )
        md = '''---
title: Wpis testowy
tags:
  - tag1
  - tag2
author: Test Testowy
---

Pierwsza linijka tekstu, zawierająca *markup*.

<!-- more -->

Druga linijka tekstu, zawierająca *markup*.
'''
        post_from_markdown(md)
        rv = Post.get()
        assert rv.created == dt

    def test_updated_draft(self, mocker):
        dt = datetime(2020, 6, 12, 18, 34, 12)
        mocker.patch(
            'devlog.utils.text._get_now', mocker.Mock(return_value=dt),
        )
        md = '''---
title: Wpis testowy
date: 2020-06-21T18:24:12
tags:
  - tag1
  - tag2
draft: true
author: Test Testowy
---

Pierwsza linijka tekstu, zawierająca *markup*.

<!-- more -->

Druga linijka tekstu, zawierająca *markup*.
'''
        post_from_markdown(md)
        rv = Post.get()
        assert rv.published is None

    def test_update(self, post_factory):
        dt = datetime(2020, 6, 21, 18, 24, 12)
        title = 'Wpis testowy'
        post = post_factory(title=title, created=dt, published=dt)
        text = 'Pierwsza linijka tekstu, zawierająca *markup*.'
        md = f'''---
title: Wpis testowy
date: 2020-06-21T18:24:12
tags:
  - tag1
  - tag2
---

{text}
'''
        post_from_markdown(md)
        rv = Post.get_by_id(post.pk)
        assert rv.text == text


@pytest.mark.usefixtures('app')
class TestSitemapGenerator:

    STATIC_URL_COUNT = 3

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.sitemap_path = os.path.join(app.static_folder, 'sitemap.xml')

    def test_generate_empty(self, mocker):
        mocker.patch.dict('os.environ', {'WHERE_AM_I': 'localhost'})
        sitemap_generator()
        with open(self.sitemap_path) as fp:
            content = fp.read()
        assert content.count('<url>') == self.STATIC_URL_COUNT

    def test_misconfigured(self, mocker):
        mocker.patch.dict('os.environ', {'WHERE_AM_I': ''})
        with pytest.raises(SystemExit):
            sitemap_generator()

    def test_with_post(self, mocker, post_factory):
        mocker.patch.dict('os.environ', {'WHERE_AM_I': 'localhost'})
        dt = datetime(2020, 6, 22, 18, 43, 15)
        post_factory(created=dt, published=dt, updated=dt)
        sitemap_generator()
        with open(self.sitemap_path) as fp:
            content = fp.read()
        assert content.count('<url>') == self.STATIC_URL_COUNT + 1
        assert dt.isoformat() in content

    def test_with_tagged_post(
                self, mocker, post_factory, tag_factory, tagged_post_factory
            ):
        mocker.patch.dict('os.environ', {'WHERE_AM_I': 'localhost'})
        dt = datetime(2020, 6, 22, 18, 43, 15)
        post = post_factory(created=dt, published=dt, updated=dt)
        tags = ['etykieta 1', 'etykieta 2']
        for t_name in tags:
            tag = tag_factory(name=t_name)
            tagged_post_factory(tag=tag, post=post)
        sitemap_generator()
        with open(self.sitemap_path) as fp:
            content = fp.read()
        assert content.count('<url>') == self.STATIC_URL_COUNT + 1 + len(tags)
        assert content.count(dt.isoformat()) == 1 + 1 + len(tags)
