uWSGI deployment
================

This is the simplest way to deploy WSGI-based application like this one, eg.
written with Flask. Directory ``conf`` in repo root contains configuration
files for uWSGI based deployment.

Preparations
------------

Create virtualenv and install application package (eg. wheel), remember to
specify ``prod`` extra option. Create directory to store instance configuration
and place local overrides there, in config files they're referred as
``config_local.py`` and ``secrets.py``. Create symlink to ``static``
subdirectory in package installation dir so it's accessible under some
convenient path.

Nginx
-----

File ``nginx.conf`` contains Nginx server configuration with enabled SSL
support from `letsencrypt <https://letsencrypt.org/>`_. On Ubuntu and other
Debian based hosts place this file in ``/etc/nginx/sites-available`` under
desired name, modify it to suit your system and symlink it in
``/etc/nginx/sites-enabled``.

uWSGI
-----

uWSGI process is started as ordinary user so there's no special requirements
regarding file permission. Place it anywhere the user will have access to.

Upstart
-------

Sample configuration contains upstart startup script for Ubuntu 14.04. I plan
to migrate to Ubuntu 18.04 at some time in 2019 so most probably it will be
superseded by proper systemd unit file.
