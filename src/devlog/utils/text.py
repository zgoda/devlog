import io
import re

from markdown import Markdown
from text_unidecode import unidecode

_punctuation_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text: str, delim: str = '-') -> str:
    result = []
    for word in _punctuation_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return delim.join(result)


def unmark_element(element, stream=None):
    if stream is None:
        stream = io.StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


def stripping_markdown() -> Markdown:
    Markdown.output_formats['plain'] = unmark_element
    md = Markdown(output_format='plain')
    md.stripTopLevelTags = False
    return md
