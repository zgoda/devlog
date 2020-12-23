import re

from flask import request

from ..models import User
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
        user_id = f'https://{host}/{username}'
        user = User.get_or_none(User.actor_id == user_id)
        if user is not None:
            doc = {
                'subject': res,
                'links': [
                    {
                        'rel': 'self',
                        'type': 'application/activity+json',
                        'href': user.actor_id,
                    }
                ]
            }
            return doc
    return {'error', 'no such resource'}, 404
