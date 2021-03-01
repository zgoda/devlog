import xml.etree.ElementTree as ET  # noqa: DUO107,N817
from collections import namedtuple

NO_CACHE_HEADERS = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0',
}

PageDef = namedtuple('PageDef', ['loc', 'lastmod'])
URLSet = namedtuple('URLSet', ['config', 'pagedefs'])
URLSetConfig = namedtuple(
    'URLSetConfig', ['changefreq', 'priority'], defaults=('0.5', )
)


def url_data(el: ET.Element, page: PageDef, config: URLSetConfig):
    """Generate sitemap data for single URL

    :param el: URL element
    :type el: ET.Element
    :param page: page definition
    :type page: PageDef
    :param config: config for the set of URLs of the same kind
    :type config: URLSetConfig
    """
    ET.SubElement(el, 'loc').text = page.loc
    ET.SubElement(el, 'lastmod').text = page.lastmod
    ET.SubElement(el, 'changefreq').text = config.changefreq
    ET.SubElement(el, 'priority').text = config.priority


def url_set(el: ET.Element, urlset: URLSet):
    """Generate URL elements for the set of URLs of the same kind, sharing the
    same configuration.

    :param el: root sitemap element
    :type el: ET.Element
    :param urlset: set of pages with config
    :type urlset: URLSet
    """
    for page in urlset.pagedefs:
        url_element = ET.SubElement(el, 'url')
        url_data(url_element, page, urlset.config)


def generate_sitemap(*urlsets) -> ET.Element:
    """Generate sitemap document content from sets of pages with shared
    configuration.

    :return: document root element
    :rtype: ET.Element
    """
    root = ET.Element('urlset')
    root.attrib['xmlns'] = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    for urlset in urlsets:
        url_set(root, urlset)
    return root


def save_sitemap_file(path: str, element: ET.Element):
    """Write sitemap content as XML document.

    :param path: file path where document will be stored
    :type path: str
    :param element: sitemap root element
    :type element: ET.Element
    """
    tree = ET.ElementTree(element)
    tree.write(path, encoding='utf-8', xml_declaration=True)
