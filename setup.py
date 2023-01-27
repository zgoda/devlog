import ast
import codecs
import re
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))


def read(*parts):
    with codecs.open(path.join(here, *parts), 'r') as fp:
        return fp.read()


_version_re = re.compile(r"__version__\s+=\s+(.*)")


def find_version(*where):
    return str(ast.literal_eval(_version_re.search(read(*where)).group(1)))


REQ_BASE = [
    'Flask',
    'Jinja2',
    'MarkupSafe',
    'itsdangerous',
    'Flask-Babel',
    'Flask-FlatPages',
    'Flask-Assets',
    'Flask-Caching>=1.10',
    'Peewee',
    'text-unidecode',
    'pyuca',
    'pytz',
    'python-dotenv',
    'PyYAML',
    'requests',
    'markdown',
    'python-dateutil',
    'pygments',
    'jsx-lexer',
    'defusedxml',
]

REQ_TEST = [
    'fakeredis',
    'pytest',
    'pytest-mock',
    'pytest-cov',
    'pytest-factoryboy',
    'pytest-flask',
    'responses',
]

REQ_DEV = REQ_TEST + [
    'ipython',
    'ipdb',
    'pip',
    'setuptools',
    'wheel',
    'flake8',
    'flake8-builtins',
    'flake8-bugbear',
    'flake8-comprehensions',
    'flake8-pytest-style',
    'pep8-naming',
    'dlint',
    'rstcheck',
    'isort',
    'flask-shell-ipython',
    'watchdog',
]

REQ_PROD = [
    'gunicorn',
    'redis[hiredis]',
]


long_description = read('README.md')

setup(
    name='devlog',
    version=find_version('src', 'devlog', '_version.py'),
    author='Jarek Zgoda',
    author_email='jarek.zgoda@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    url='http://github.com/zgoda/devlog',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    ],
    install_requires=REQ_BASE,
    extras_require={
        'prod': REQ_PROD,
        'test': REQ_TEST,
        'dev': REQ_DEV,
    },
    entry_points={
        'console_scripts': [
            'devlog=devlog.cli:main',
            'postimport=devlog.tasks:import_posts',
            'sitemapgen=devlog.tasks:sitemap_generator',
            'linkimport=devlog.tasks:import_links',
        ],
        'markdown.extensions': [
            'centerblock=devlog.utils.text:CenterBlockExtension',
        ]
    },
    python_requires='~=3.8',
)
