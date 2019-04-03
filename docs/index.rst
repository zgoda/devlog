Devlog files
============

Devlog is my personal project done mostly as a playground for different things
related to web application development with Flask and architecting software in
general. Other goal is to make *ideal package* of Flask based web application,
with clean structure and modern tooling. I'm almost there with that.

Speaking of functionality, the application implements or aims to implement
*simple blog*:

* authentication
* authorization
* inline content management (no *admin interface*)
* strict and extensible content access management

Please note this application does not strive to be neither complete nor even
working. It's just a playground. Initial plan was to deploy this application as
a part of zgodowie.org service similar to
`Brewlog app <https://brewlog.zgodowie.org>`_, but this may be postponed or may
even never happen. The code is what matters here.

Why that? I already have a pet project that I use on daily basis, the
`Brewlog project <https://github.com/zgoda/brewlog>`_. It's running file but I
started it in 2013 **(!)** and now it should be made a bit
more contemporary looking. I did not touch it for quite a long time, and issues
stockpiled. In 2019 I will be doing a general revamp of the project, partially
because it's running on outdated VPS that can't be upgraded to newer OS
version, but more important is that the tools made grat leap forward in last
years.

Miscellanea
-----------

.. toctree::
    :maxdepth: 2

    concepts
    tools
    tbc
    todo

Caveats
-------

.. toctree::
    :maxdepth: 2

    flask

Practicalia
-----------

.. toctree::
    :maxdepth: 2

    uwsgi

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
