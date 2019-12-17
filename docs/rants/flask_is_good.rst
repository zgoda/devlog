Flask is A Good Thing
=====================

Let's get things straight - `Flask <https://flask.palletsprojects.com/>`_ is
not *good micro framework*. Its code base is small but you won't feel that
*micro*  normally. Not at all, average application memory footprint will be on
par with similar Django application. It may be somewhat faster, but by a tiny
margin. This is not the reason why Flask Is A Good Thing (and Django is not,
at leasts compared to Flask).

Real strength of Flask is Python. When working on Django based application one
writes *in Django*. While technically this is still Python code, the framework
requires that developer *thinks in framework*. It provides everything plus
some customization options, but the cost is freedom if mind. Long time ago I
saw what was once Django framework code that has been stripped of all things
that are wrong, not usable or had better alternatives. What was left was
URL routing and request/response objects. Not much, huh? I am sure Django made
great leaps in that time but its *greatness* prevailed.

Flask roots lie in April Fools joke that one Austrian guy made in 2010. Later
when doing post-mortem he stated what he hates about it and so became early
Flask. Since then it was always about URL routing and request/response
wrappers. Oh, there's Jinja2 also but it's co-authored by that guy. And it's
built upon Werkzeug, which is a gem in itself - and is co-authored by the very
same Austrian guy. So it was like "I have a toolbox and one tool, this should
be enough to build something people will use to build their things". And it
is. BTW, later they added Click command line library, which unsuprisingly was
authored by this Austrain guy.

The most appealing in Flask is that it's composed, and you see that
composition. It does not hide Werkzeug, although not always exposes it. It
does all the tedious Jinja2 environment setup you would have to do by
yourself. I tried that once and I can tell you, it's really tedious. It was
about a year before Armin did his April Fools joke when I built my first own
web framework based on... Werkzeug and Jinja2. While it did not have automatic
route registration, it was all Flask otherwise - thin wrappers over Werkzeug's
request and response objects and a bunch of utility functions that make life
of ordinary developer easier.

But the most overlooked thing in Flask is that it's all Python, pure and to the
bone. Their documentation makes it clear - write code, write tests, package
your code and deploy. There's no shortcuts, from the very introductory
material they are straight - *go full Monty or go elsewhere*. While Flask does
not enforce that, the authors encourage users to *do the right thing*. I
recently tried to *package* Django web application into wheel just to see how
it can be done - and it's real PITA.

I'm grateful we have Flask. Event if it's not *micro*, and it's not as fast as
Sanic.
