import re

from flask import request, url_for

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
        user_id = f'https://{host}/user/{username}'
        user = User.get_or_none(User.actor_id == user_id)
        if user is not None:
            profile_url = url_for('ap.userprofile', name=user.name, _external=True)
            doc = {
                'subject': res,
                'aliases': [
                    user.actor_id,
                    profile_url
                ],
                'links': [
                    {
                        'rel': 'self',
                        'type': 'application/activity+json',
                        'href': user.actor_id,
                    },
                    {
                        'rel': 'http://webfinger.net/rel/profile-page',
                        'type': 'text/html',
                        'href': profile_url
                    }
                ]
            }
            return doc
    return {'error': 'no such resource'}, 404
