from datetime import datetime

import pytest

from devlog.models import Post
from devlog.tasks import action_from_markdown


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
        action_from_markdown(md)
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
            action_from_markdown(text)

    def test_import_no_date(self, mocker):
        dt = datetime(2020, 6, 12, 18, 34, 12)
        mocker.patch(
            'devlog.tasks.datetime',
            mocker.Mock(utcnow=mocker.Mock(return_value=dt)),
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
        action_from_markdown(md)
        rv = Post.get()
        assert rv.created == dt

    def test_updated_draft(self, mocker):
        dt = datetime(2020, 6, 12, 18, 34, 12)
        mocker.patch(
            'devlog.tasks.datetime',
            mocker.Mock(utcnow=mocker.Mock(return_value=dt)),
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
        action_from_markdown(md)
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
        action_from_markdown(md)
        rv = Post.get_by_id(post.pk)
        assert rv.text == text
