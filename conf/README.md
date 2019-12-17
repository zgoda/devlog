# Configuration files

These are application configuration files for the most standard setup:

* app server: uWSGI
* web server: nginx
* supervisor: Systemd

They should be treated as guidelines, the resource specification is very pessimistic and is not meant to be used for anything more than lightest traffic. This setup is intended to be used by regular user with (some) administrative privileges, eg. putting files in `/etc/systemd/system` or calling `systemctl` - of course with the help of `sudo`.

## uWSGI.ini

This is uWSGI control file. It should be modified and placed somewhere in user home directory.

## nginx.conf

This file should be placed in `/etc/nginx/sites-available` then symlinked to `/etc/nginx/sites-enabled`. This file does not include HTTPS configuration but `certbot` is very helpful and does most of nginx configuration changes automatically.

## systemd control files

* devlog.target: main systemd target file for all things Devlog (application, task workers, worker pool)
* devlog.service: systemd unit file that launches and restarts Devlog web application
* devlog-task@.service: task workers unit template
* devlog-tasks.target: systemd target that manages all running task workers at once

These files should be placed in `/etc/systemd/system`.
