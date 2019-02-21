from flask import session

from ..ext import oauth


def get_access_token():
    return session.get('access_token')


github = oauth.register('github', fetch_token=get_access_token)
