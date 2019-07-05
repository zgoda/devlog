Flask gotchas
=============

`Flask <http://flask.pocoo.org/>`_ is fine web framework, kind of enabler -
it's easy and simple at the beginning, and very appealing with its *no
unnecessary cruft* stance. It emphasizes *speed of development over speed of
execution* paradigm that was popularized by
`Django <https://www.djangoproject.com/>`_ framework long before Flask was
born from one Austrian guy April Fools joke.

Unfortunately this simplicity comes at some price that may not be apparent at
the beginning. It may not become apparent at all because Flask is easy and
simple as long as you do *standard things*. What is non-standard according to
Flask?

Template file name extensions
-----------------------------

This is documentend but easily overlooked. Flask sets autoescaping of template
context values only for files with couple standard extensions. If you use any
modern text editor that has Jinja support, it may suggest that you save your
templates eg. with ``.j2`` extension, like Ansible templates. And since the
extension is not on the list of file extensions that trigger autoescaping,
your app will render templates with raw values. Gotcha!

Remedy
^^^^^^

Either monkeypatch ``Flask`` object with your own implementation of
autoescaping selection logic or subclass it and override
``select_jinja_autoescape`` method. The former may be tempting by simplicity
but the later may be handy in resolving other issues which we will look at
later.

Jinja configuration
-------------------

Ever wondered why HTML output of rendering your templates is so rich in
whitespace? That's because default Jinja way of rendering that leaves all
whitespace intact, even around template directives. Jinja provides couple
configuration options that control whitespace rendering but they are hidden
deep in Flask initialization and there's no way to set it in any way.

Remedy
^^^^^^
This time monkeypatching won't help because Jinja environment is created as
soon as application is configured, and this may be too late for many so the
most reliable way to overcome this limitation is to subclass ``Flask`` and
set the options as you see fit. Originally this is plain instance variable
but you may make it to ``property`` and extend original ``jinja_options``.

Werkzeug goodies
----------------

During development application is usually running with reloader to quickly
reflect changes in code. Werkzeug allows specifying reloading engine by
providing backend name to server function but Flask does not expose this.
Using ``stat`` reloader may be specially painful to laptop users so it would
be great if we could switch to ``inotify``-based. Fortunately Werkzeug is nice
and uses the best available so it is enough to install
`watchdog <https://pypi.org/project/watchdog/>`_ package.

The same applies to colored terminal output, just install
`termcolor <https://pypi.org/project/termcolor/>`_ package.

Add these two to dev requirements.
