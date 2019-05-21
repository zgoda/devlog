To be considered
================

Things that may be worth considering to be implemeneted/integrated as part of
this project. Or just interesting.

Resource Access Control
-----------------------

* `Vakt <https://github.com/kolotaev/vakt>`_ implements Attribute Based Access
  Control (ABAC).
* `Casbin <https://pypi.org/project/casbin/>`_ implements Role Based Access
  Control (RBAC)

Or prepare somethig that would be better suited for projects of this size
because both RBAC and ABAC are big things that don't scale down well - there is
large beginning processing overhead. Perhaps something losely resembling ABAC.

Unfortunately the access control implementations at object level are rather
scarce in Python. Specifically for Flask there is
`Flask-Principal <https://pypi.org/project/Flask-Principal/>`_ and more general
approach with `Permission <https://pypi.org/project/permission/>`_ but both
require writing tons of code. Permission seems to be more approachable but
lacks any tests which is quite unusual these days. Most of other
libraries/extensions are request handler oriented and do not fit my vision.

Separation of concern
---------------------

* `Stories <https://pypi.org/project/stories/>`_ and
  `Dependencies <https://pypi.org/project/dependencies/>`_ are interesting
  libraries to implement business DSL and DI respectively

WTForms + Jinja2 + CSS glue
---------------------------

For both rapid protoryping and full fledged web app development CSS frameworks
are code packages that relieve software developer from much of unwelcome visual
side development. While Bootstrap is supported pretty good, there are other CSS
frameworks which don't get much attention and provide some value Bootstrap is
missing.

This may come later into fruition as general purpose WTForms rendering
extension with pluggable visualisation engines for different frameworks,
although from a quick glance over form structuring in different frameworks it
does not look promising.
