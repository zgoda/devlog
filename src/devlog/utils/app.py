import os

from flask import Flask


class Devlog(Flask):

    def __init__(self):
        kw = {}
        instance_path = os.environ.get('DEVLOG_INSTANCE_PATH')
        if instance_path:
            kw['instance_path'] = os.path.abspath(instance_path)
        super().__init__(__name__.split('.')[0], **kw)

    @property
    def jinja_options(self):
        options = dict(super().jinja_options)
        options.update({
            'trim_blocks': True,
            'lstrip_blocks': True,
        })
        return options
