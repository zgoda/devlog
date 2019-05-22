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
working. Although it's just a playground, the
`application is deployed <https://devlog.zgodowie.org>`_ and can be seen live.
Changes are deployed with every tag.

Why that? I already have a pet project that I use on daily basis, the
`Brewlog project <https://github.com/zgoda/brewlog>`_. It's running fine but I
started it in 2012 **(!)**, did not throw much work on it recently and now it
just looks outdated. I did not touch it for quite a long time, and issues
stockpiled. In 2019 I will be doing a general revamp of the project, partially
because it's running on outdated VPS that can't be upgraded to newer OS
version, but more important is that the tools made grat leap forward in last
years, and development of Python web application does not look like before.

The tooling is pretty standard, and in fact that did not change much, it's
still Flask with SQLAlchemy but in the course Bootstrap got updated to version
4, OAuth support library got deprecated and superseded, packaging tools greatly
improved and VPS instances became really cheap.

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
    :maxdepth: 1

    uwsgi

Rants
-----

.. toctree::
    :maxdepth: 1

    rants/cssframeworks

Project documentation
---------------------

.. toctree::
    :maxdepth: 1

    coc
    contributing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
