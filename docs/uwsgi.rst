uWSGI deployment
================

This is the simplest way to deploy WSGI-based application like this one, eg.
written with Flask. Directory ``conf`` in repo root contains configuration
files for uWSGI+Nginx based deployment. I tried to make it a bit less intrusive
but **this is still** something that requires full attention so prepare your
box and exercise with me. I recently did 1st deployment on freshly procisioned
box.

Preparations
------------

Create unprivileged user account. This will be the user that will be running
application code.

Create virtualenv and install application package (eg. wheel), remember to
specify ``prod`` extra option. Create directory to store instance configuration
and place local overrides there, in config files they're referred as
``config_local.py`` and ``secrets.py``. Create symlink to ``static``
subdirectory in package installation dir so it's accessible to Nginx under some
convenient path. uWSGI log directory is configured to be there so create it as
well.

Nginx
-----

On Ubuntu and other Debian based hosts place the file in
``/etc/nginx/sites-available`` under desired name, modify it to suit your
system and symlink it in ``/etc/nginx/sites-enabled``. I found leaving SSL
configuration for Certbot works fine on both Ubuntu and Debian. Start with
no-SSL configuration, run certbot, reload Nginx.

uWSGI
-----

uWSGI process is started as ordinary user so there's no special requirements
regarding file permission. Place it anywhere the user will have access to.

Upstart & systemd
-----------------

Sample configuration contains upstart startup script for Ubuntu 14.04 and
systemd unit file for newer releases.
