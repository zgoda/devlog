from datetime import datetime

import pytest

from devlog.utils.blog import post_from_markdown
from devlog.utils.pagination import get_page


def test_pagination_invalid_param(client, app):
    val = 'dummy'
    with app.test_request_context(f'/?p={val}'):
        page = get_page()
        assert page != val
        assert page == 1


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
        rv = post_from_markdown(md)
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
            'devlog.utils.blog.datetime',
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
        rv = post_from_markdown(md)
        assert rv.created == dt

    def test_updated_draft(self, mocker):
        dt = datetime(2020, 6, 12, 18, 34, 12)
        mocker.patch(
            'devlog.utils.blog.datetime',
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
        rv = post_from_markdown(md)
        assert rv.published is None
