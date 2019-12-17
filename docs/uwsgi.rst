uWSGI + Nginx deployment
========================

This is the simplest way to deploy WSGI-based application like this one, eg.
written with Flask. Directory ``conf`` in repo root contains configuration
files for uWSGI + Nginx based deployment. I tried to make it a bit less
intrusive but **this is still** something that requires full attention so
prepare your box and exercise.

This repository
`contains example configuration <https://github.com/zgoda/devlog/tree/master/conf>`_
for uWSGI, Nginx and appropriate ``systemd`` control files. There are
alternatives, but ``systemd`` is provided by most contemporary Linux systems.
Of course they require some hand editing but otherwise they are complete.

Moving parts
------------

uWSGI runs application code. Nginx proxies the stream. This is 2 independently
moving elements that produce independent logs. uWSGI in itself does not have
many bugs but it runs application code and may encounter various conditions.
Nginx once properly started does not require any attention. The problem is that
these 2 environments produce logs that must be examined both to trace any
problem.
