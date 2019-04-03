from os import path

from setuptools import setup, find_packages

import versioneer


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='devlog',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
    install_requires=(
        'Flask',
        'Flask-Babel',
        'Flask-Login',
        'Flask-FlatPages',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Bootstrap-Flask',
        'SQLAlchemy-Utils',
        'Authlib',
        'WTForms-Alchemy',
        'docutils',
        'markdown2',
        'textile',
        'attrs',
        'text-unidecode',
        'pytz',
        'babel',
        'sentry_sdk[flask]',
        # pinned
        'SQLAlchemy<1.3',
    ),
    setup_requires=(
        'pytest-runner',
    ),
    tests_require=(
        'pytest',
        'pytest-mock',
        'pytest-cov',
        'pytest-flask',
        'pytest-factoryboy',
    ),
    extras_require={
        'prod': [
            'psycopg2-binary',
            'uwsgi',
        ]
    },
    entry_points={
        'console_scripts': [
            'devlog=devlog.cli:main',
        ],
    },
    python_requires='~=3.7',
)
