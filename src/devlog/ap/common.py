import re

from flask import request

from . import activitypub_bp as bp

WEBFINGER = re.compile(
    r"""(?:acct:)?
    (?P<username>[\w.!#$%&\'*+-/=?^_`{|}~]+)@
    (?P<host>[\w.:-]+)""",
    re.VERBOSE | re.MULTILINE
)


@bp.route('/.well-known/webfinger')
def webfinger():
    res = request.args.get('resource')
    if not res:
        return {'error': 'malformed request'}, 400
    matchdict = WEBFINGER.match(res)
    if matchdict:
        username = matchdict['username']
        host = matchdict['host']
