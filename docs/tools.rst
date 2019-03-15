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
It's selection of analytical packages is rather adequate, although not
specially flexible, the choice of external quality checkers is very limited. I
found Code Climate to produce more false negatives re. code duplication and
suggesting refactoring completely unrelated code because it barely *looks
similar*.

When it comes to access to quality indicators and *insights*, Codacy seems to
provide easier access to key quality factors. The information is well
structured with important things put in front. On the other hand, Code Climate
presents almost identical set of information completely flat. There are no
visual indicators on trends.
