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

Wheel packaging
---------------

To push things a bit I decided to package the application as wheel (apart of
usual ``sdist``) and deploy it as artifact in Github release. This made
deployment a bit simpler: grab a package from known place and install it in
virtualenv. Next step could be private PyPi and distribution but this is still
cumbersome.

Development requirements specification
--------------------------------------

For a long time I insisted on keeping PIP requirements files only slightly
organized in project root. Now I decided to put them aside, since they don't
have any use besides development and CI. This makes project root much cleaner.

Bulma and other CSS frameworks
------------------------------

`Bootstrap <https://getbootstrap.com/>`_ is usually 1st choice when it comes
to CSS framework selection. It's proven, it has all the docs, it's widely
used. It has its drawbacks but not many and most people can live with that.
There are contenders and Bulma is one of them.

Bulma is pure CSS iow it does not neither provide or require any Javascript to
operate. There are parts that may require some Javascript code but one can
live without them I guess. My main concern is that Bulma has 2 modes of
operation and one of them is PITA for Flask template authors.

Normally all elements are totally unstyled. Paragraphs are displayed exactly
the same as headings, citations or even code. One has to add CSS context
classes to make them look like paragraphs, headings, citations or code. This
mode is the default mode and putting that extra classes on **every HTML
element** just feels really wrong. I guess web designers are happy with this
but for guys like me that just wants to output some HTML and make it look a
bit better than ugly it seems too much.

But Bulma has another mode, which is triggered by wrapping HTML elements in
class ``content`` and in this mode elements are styled normally.
