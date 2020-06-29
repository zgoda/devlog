import io
import os
import re
import xml.etree.ElementTree as etree  # noqa: DUO107,N813
from datetime import date, datetime
from typing import Optional, Union

import markdown
import pytz
from markdown import Markdown
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from text_unidecode import unidecode

_punctuation_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

DEFAULT_MD_EXTENSIONS = [
    'abbr', 'def_list', 'full_yaml_metadata', 'fenced_code', 'codehilite',
    'centerblock',
]

METADATA_RE = re.compile(r'\A---.*?---', re.S | re.MULTILINE)


def slugify(text: str, delim: str = '-') -> str:
    result = []
    for word in _punctuation_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return delim.join(result)


def stripping_markdown() -> Markdown:

    def unmark_element(element, stream=None) -> str:
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


def rich_summary(post_text: str) -> str:
    summary_end_pos = post_text.find('<!-- more -->')
    raw_summary = post_text[:summary_end_pos].strip()
    md = Markdown(
        extensions=DEFAULT_MD_EXTENSIONS, output_format='html'
    )
    return md.convert(raw_summary)


def post_summary(text: str) -> str:
    plain_text = stripping_markdown().convert(text)
    summary_end_pos = plain_text.find('<!-- more -->')
    if summary_end_pos > -1:
        return rich_summary(text)
    return markdown.markdown(
        ' '.join(plain_text.split()[:50]), extensions=DEFAULT_MD_EXTENSIONS,
        output_format='html',
    )


def normalize_post_date(dt: Optional[Union[date, datetime]]) -> datetime:
    if dt:
        if isinstance(dt, date):
            dt = datetime.utcnow().replace(
                year=dt.year, month=dt.month, day=dt.day
            )
        if dt.tzinfo is None:
            tz = pytz.timezone(
                os.environ.get('BABEL_DEFAULT_TIMEZONE', 'Europe/Warsaw')
            )
            dt = dt.astimezone(tz).astimezone(pytz.utc)
        else:
            dt = dt.astimezone(pytz.utc)
        dt.replace(tzinfo=None)
    return dt


class CenterBlockProcessor(BlockProcessor):
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
