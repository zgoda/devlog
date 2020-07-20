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
    'Flask-Babel',
    'Flask-FlatPages',
    'Flask-Assets',
    'Peewee',
    'text-unidecode',
    'pytz',
    'python-dotenv',
    'PyYAML',
    'requests',
    # Sentry
    'sentry-sdk[flask]',
    # simplified markup processors
    'markdown',
    'python-dateutil',
    'pygments',
]

REQ_TEST = [
    'pytest',
    'pytest-mock',
    'pytest-cov',
    'pytest-factoryboy',
    'pytest-flask',
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
    'flake8-mutable',
    'flake8-comprehensions',
    'flake8-pytest-style',
    'pep8-naming',
    'dlint',
    'rstcheck',
    'rope',
    'isort',
    'flask-shell-ipython',
    'watchdog',
]

REQ_PROD = [
    'gunicorn',
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    ],
    install_requires=REQ_BASE,
    tests_require=REQ_TEST,
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
        ],
        'markdown.extensions': [
            'centerblock=devlog.utils.text:CenterBlockExtension',
        ]
    },
    python_requires='~=3.7',
)
