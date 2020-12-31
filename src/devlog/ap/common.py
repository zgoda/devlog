import json
import re
from html import escape

from flask import make_response, request, url_for

from .._version import get_version
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
        username = escape(matchdict['username'])
        host = escape(matchdict['host'])
        user_id = f'https://{host}/user/{username}'
        user = User.get_or_none((User.actor_id == user_id) & (User.is_active))
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
            resp = make_response(json.dumps(doc))
            resp.headers['Content-Type'] = 'application/jrd+json'
            return resp
    return {'error': 'no such resource'}, 404


@bp.route('/.well-known/nodeinfo')
def nodeinfo():
    doc = {
        'version': '2.0',
        'software': {
            'name': 'devlog',
            'version': get_version(),
        },
        'protocols': [
            'activitypub',
        ],
        'services': {
            'inbound': [],
            'outbound': []
        },
        'openRegistrations': False,
        'usage': {
            'users': {
                'total': 1,
                'activeHalfyear': 1,
                'activeMonth': 1,
            },
            'localPosts': 0,
            'localComments': 0,
        },
        'metadata': {}
    }
    resp = make_response(json.dumps(doc))
    resp.headers['Content-Type'] = 'application/json; profile=http://nodeinfo.diaspora.software/ns/schema/2.0#'  # noqa: E501
    return resp
