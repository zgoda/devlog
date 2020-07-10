import datetime
import io
import os
import re
import xml.etree.ElementTree as etree  # noqa: DUO107,N813
from collections import namedtuple
from typing import Optional, Union

import markdown
import pytz
import yaml
from dateutil import parser
from markdown import Markdown
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from text_unidecode import unidecode

_punctuation_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

DEFAULT_MD_EXTENSIONS = [
    'abbr', 'def_list', 'fenced_code', 'codehilite', 'centerblock',
]

METADATA_RE = re.compile(r'\A---(.*?)---', re.S | re.MULTILINE)


def slugify(text: str, delim: str = '-') -> str:
    result = []
    for word in _punctuation_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return delim.join(result)


def stripping_markdown() -> Markdown:

    def unmark_element(element, stream=None) -> str:  # pragma: nocover
        if stream is None:
            stream = io.StringIO()
        if element.text:
            stream.write(element.text)
        for sub in element:
            unmark_element(sub, stream)
        if element.tail:
            stream.write(element.tail)
        return stream.getvalue()

    Markdown.output_formats['plain'] = unmark_element
    md = Markdown(output_format='plain')
    md.stripTopLevelTags = False
    return md


def _get_now(utc: bool = False) -> datetime.datetime:  # pragma: nocover
    """Workaround over datetime C module to be able to mock & patch in tests.
    """
    if utc:
        return datetime.datetime.utcnow()
    return datetime.datetime.now()


def normalize_post_date(
            dt: Optional[Union[str, datetime.date, datetime.datetime]]
        ) -> Optional[datetime.datetime]:
    """This function normalizes input to UTC datetime tithout timezone
    information (naive). If input object does not have timezone information,
    it is assumed to be local time and this may produce wrong result if at
    the time of processing DST is different than for input date.

    :param dt: input date, datetime or string representation in "common"
               format
    :type dt: Optional[Union[str, datetime.date, datetime.datetime]]
    :return: datetime in UTC without timezone information
    :rtype: Optional[datetime.datetime]
    """
    if dt:
        if isinstance(dt, str):
            dt = parser.parse(dt)
        if isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
            dt = _get_now().replace(
                year=dt.year, month=dt.month, day=dt.day
            )
        if dt.tzinfo is None:
            tz = pytz.timezone(
                os.environ.get('BABEL_DEFAULT_TIMEZONE', 'Europe/Warsaw')
            )
            dt = tz.localize(dt).astimezone(pytz.utc)
        else:
            dt = dt.astimezone(pytz.utc)
        dt = dt.replace(tzinfo=None)
    return dt


class CenterBlockProcessor(BlockProcessor):  # pragma: nocover
    RE_START = r'^->'
    RE_END = r'<-$'

    def test(self, parent, block):
        return re.match(self.RE_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        blocks[0] = re.sub(self.RE_START, '', blocks[0])
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_END, block):
                blocks[block_num] = re.sub(self.RE_END, '', block)
                e = etree.SubElement(parent, 'div')
                e.set('style', 'text-align:center')
                self.parser.parseBlocks(e, blocks[0:block_num + 1])
                for _ in range(0, block_num + 1):
                    blocks.pop(0)
                return True
        blocks[0] = original_block
        return False


class CenterBlockExtension(Extension):

    def extendMarkdown(self, md):  # noqa: N802
        md.parser.blockprocessors.register(
            CenterBlockProcessor(md.parser), 'centerblock', 175
        )


PostMeta = namedtuple(
    'PostMeta',
    [
        'title', 'slug', 'author', 'created', 'updated', 'draft',
        'c_year', 'c_month', 'c_day', 'summary',
    ]
)


class PostProcessor:

    MD_KWARGS = {
        'extensions': DEFAULT_MD_EXTENSIONS, 'output_format': 'html'
    }

    def __init__(self, text: str):
        doc_parts = METADATA_RE.split(text.strip())
        if len(doc_parts) < 2:
            raise ValueError('Metadata part missing')
        meta = yaml.safe_load(doc_parts[-2])
        if 'title' not in meta:
            raise ValueError('Title missing in post metadata')
        self.meta = meta
        self.text = doc_parts[-1].strip()

    @property
    def tags(self):
        return [str(t) for t in self.meta.get('tags', [])]

    @staticmethod
    def summary_src(text: str) -> str:
        plain_text = stripping_markdown().convert(text)
        summary_end_pos = text.find('<!-- more -->')
        if summary_end_pos > -1:
            return text[:summary_end_pos].strip()
        return ' '.join(plain_text.replace('<!-- more -->', '').split()[:50])

    def summary(self) -> str:
        return markdown.markdown(self.summary_src(self.text), **self.MD_KWARGS)

    def published(self, new_post: bool, meta: PostMeta) -> datetime.datetime:
        if meta.draft:
            return None
        if new_post:
            return meta.created
        return meta.updated

    def process_meta(self) -> PostMeta:
        title = self.meta['title'].strip().replace("'", '')
        created = updated = _get_now(True)
        post_date = self.meta.get('date')
        if post_date:
            created = normalize_post_date(post_date)
        slug = slugify(title)
        c_year, c_month, c_day = created.year, created.month, created.day
        author = self.meta.get('author', '').strip()
        draft = self.meta.get('draft', False)
        summary = self.summary()
        return PostMeta(
            title, slug, author, created, updated, draft, c_year, c_month, c_day,
            summary,
        )

    def as_dict(
                self, meta: PostMeta, published: Optional[datetime.datetime],
                update: bool = False,
            ) -> dict:
        data = {
            'published': published,
            'text': self.text,
            'text_html': markdown.markdown(self.text, **self.MD_KWARGS)
        }
        data.update(meta._asdict())
        del data['draft']
        if update:
            del data['created']
        return data
