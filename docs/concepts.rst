Concepts tested
===============

This project is intended mostly to test implementations of various programming
concepts and application engineering tools.

Repo structure wrt packaging
----------------------------

There is ongoing discussion in Python world on how source code should be
structured to provide best experience and results regarding testability. The
most common (and even suggested in introductory materials) is "package in repo
root", but there is also strong movement towards "package in src subdirectory".
One of concepts tested was packaging web application with code located in src
subdirectory. I was usually following the crowd and I wanted to check suggested
benefits.

Observations
^^^^^^^^^^^^

* packaging configuration is much simplified, ``MANIFEST.in`` is no longer
  cluttered by includes and excludes; ``setup.py`` required only cosmetic
  changes;
* tests are always run against installed package, making the behaviour of code
  more realistic;
* much cleaner local copy root (but this is subjective);
* easier configuration of external code analysis tools like Codacy or
  CodeClimate, there is only one directory to be included in analysis;

Was this worth the hassle?
^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes, definitely. Highly recommended.
