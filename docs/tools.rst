Tools tested
============

Automatic online code review
----------------------------

Tested tools: `Codacy <https://www.codacy.com>`_,
`Code Beat <https://codebeat.co/>`_, `Code Climate <https://codeclimate.com/>`_

Only free offers was tested so I will not look at service performance, only
project configuration, features and access to vital quality indicators.

Both Codacy and Code Climate are configured with poorly documentent YAML files,
Code Beat only on project settings page. YAML configuration may be validated
offline by provided tools but apart of this support is far from being extensive
and there's much unclear statements in documentation for both services. I found
the key is appropriate configuration of exclusions and this is done in very
similar manner in both Codacy and Code Climate config files. Lack of possiblity
to configure analysis with config file kept under version control ruled out
Code Beat.

Feature wise, both services offer similar insight on Python project quality.
The selection of analytical packages is rather adequate, although not
specially flexible, the choice of external quality checkers is very limited. I
found Code Climate to produce more false negatives re. code duplication and
suggesting refactoring completely unrelated code because it barely *looks
similar* but Codacy is not much better.

When it comes to access to quality indicators and *insights*, Codacy seems to
provide easier access to key quality factors. The information is well
structured with important things put in front. On the other hand, Code Climate
presents almost identical set of information completely flat. There are no
visual indicators on trends, no alerts, just tabs filled with information. The
scope of provided information is very similar but you need to know what you're
looking for on Code Climate. On the other hand, Codacy immediately shows
what's important.

Black
-----

`Black <https://github.com/ambv/black>`_ is controversial "uncompromising
Python code formatter". And despite all these controversies it's quite popular
and has been adopted by many projects, eg.
`Werkzeug <http://werkzeug.pocoo.org/>`_ or `Attrs <https://www.attrs.org>`_.

The controversy with Black comes from the fact that it enforces code
formatting and is extremely intrusive. There's almost no configuration options
available except for only handful not related to Black's mode of work, and the
goal to produce smallest possible diff and most compact yet still readable
code is not something that will be plausible for everybody. To me, the result
code is *too compact* and loses too much readability in two cases: rewriting
`dict` literals to be in one line and specially rewriting class definitions so
they do not have vertical whitespace between class header and 1st method
definition. But my overall impression is that in *community* projects this kind
of code style unification may be invaluable, and this tool will make any admin
of public Python project with large committer base happy. But none of my
projects is like that. In fact, flake8 with couple plugins and isort will do
the same not getting in one's way in so intrusive way.

I will continue using it in this project, I don't like it but I am not
desperate.
