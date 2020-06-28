# Configuration files

These are application configuration files for the most standard setup:

* app server: gunicorn
* web server: nginx
* supervisor: systemd

They should be treated as guidelines, the resource specification is not meant to be used for anything more than light traffic. This setup is intended to be used by regular user with (some) administrative privileges, eg. putting files in `/etc/systemd/system` or calling `systemctl` - of course with the help of `sudo`.

## nginx.conf

This file should be placed in directory `/etc/nginx/sites-available` and then symlinked to `/etc/nginx/sites-enabled`. This file does not include HTTPS configuration but `certbot` is very helpful and does most of nginx configuration changes automatically.

## systemd control files

* devlog.service: systemd unit file that launches and restarts Devlog web application

These files should be placed in `/etc/systemd/system`.

## devlog.env

This file provides environment variables for the application. It should be placed in user home directory.
