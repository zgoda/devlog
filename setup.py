import codecs
import re
from os import path

from setuptools import find_packages, setup

# parts below shamelessly stolen from pypa/pip
here = path.abspath(path.dirname(__file__))


def read(*parts):
    with codecs.open(path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


REQ_BASE = [
    'Flask',
    'Flask-Login',
    'Flask-FlatPages',
    'Flask-Babel',
    'Flask-WTF',
    'Flask-SQLAlchemy',
    'SQLAlchemy-Utils',
    'WTForms-Alchemy',
    'text-unidecode',
    'python-dateutil',
    'passlib[argon2]',
    'requests',
    'itsdangerous',
    # Sentry
    'sentry-sdk[flask]',
    # simplified markup processors
    'docutils',
    'textile',
    'markdown2',
    # RQ requirements
    'rq',
    'hiredis',
]

REQ_TEST = [
    'pytest',
    'pytest-mock',
    'pytest-cov',
    'pytest-factoryboy',
    'pytest-flask',
    'fakeredis',
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
    'pep8-naming',
    'dlint',
    'doc8',
    'pyroma',
    'rope',
    'isort',
    'towncrier',
    'Sphinx',
    'sphinx-autodoc-typehints',
    'python-dotenv',
    'flask-shell-ipython',
    'termcolor',
    'watchdog',
]

REQ_PROD = [
    'psycopg2-binary',
    'uwsgi',
    'supervisor',
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
    packages=find_packages('src', exclude=['*.secrets']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    url='http://github.com/zgoda/devlog',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
        'Natural Language :: Polish',
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
        ],
    },
    python_requires='~=3.7',
)
