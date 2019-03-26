import re

from text_unidecode import unidecode

_punctuation_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

SUPPORTED_LANGUAGES = ["pl", "en"]


def slugify(text, delim="-"):
    result = []
    for word in _punctuation_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return delim.join(result)
