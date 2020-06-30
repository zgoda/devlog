from datetime import date, datetime

import pytest
import pytz

from devlog.utils.blog import post_from_markdown
from devlog.utils.pagination import get_page
from devlog.utils.text import normalize_post_date


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


class TestPostDateNormalization:

    TZ = pytz.timezone('Europe/Warsaw')

    @pytest.mark.parametrize('value', ['', None], ids=['empty-str', 'none'])
    def test_noop(self, value):
        assert normalize_post_date(value) == value

    def test_date(self, mocker):
        value = date(2020, 6, 12)
        now = datetime(2020, 6, 14, 20, 21, 44)
        mocker.patch(
            'devlog.utils.text._get_now', mocker.Mock(return_value=now)
        )
        rv = normalize_post_date(value)
        assert rv.time() == (now - self.TZ.utcoffset(now, is_dst=False)).time()
        assert rv.date() == value

    @pytest.mark.parametrize('value', [
        '2020-06-12T20:21:44+02:00',
        '2020-06-12 20:21:44 CET',
        'June 12, 2020 9:21:44 PM'
    ])
    def test_str_valid_datetime(self, value):
        rv = normalize_post_date(value)
        assert isinstance(rv, datetime)
        assert rv.utcoffset() is None

    def test_datetime_aware(self):
        now = datetime(2020, 6, 14, 20, 21, 44)
        value = self.TZ.localize(now, is_dst=False)
        rv = normalize_post_date(value)
        assert rv.utcoffset() is None
