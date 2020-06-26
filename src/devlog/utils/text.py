import io
import re
import xml.etree.ElementTree as etree  # noqa: DUO107,N813

from markdown import Markdown
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from text_unidecode import unidecode

_punctuation_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


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
        extensions=[
            'full_yaml_metadata', 'fenced_code', 'codehilite', CenterBlockExtension()
        ],
        output_format='html'
    )
    return md.convert(raw_summary)


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
