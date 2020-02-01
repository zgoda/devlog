Notable moments and significant changes
=======================================

In January 2020 I decided to make the projest "smaller", by any means. There
would be a large application rewrite accompanied by full-scale data migration
to new structure.

Damage plan includes:

* switch to ``werkzeug`` security functions and retiring ``authlib``
* writing post export tool
* switch to SQLite as database backend
* switch to Pony as ORM layer
