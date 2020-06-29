import fcntl
import os
import stat
import sys

from dotenv import find_dotenv, load_dotenv

from .app import make_app
from .utils.blog import post_from_markdown

load_dotenv(find_dotenv())

app = make_app(os.environ.get('ENV'))
os.makedirs(app.instance_path, exist_ok=True)


def import_posts():
    lf = os.path.join(app.instance_path, 'postimport.lock')
    lf_flags = os.O_WRONLY | os.O_CREAT
    lf_mode = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
    lf_fd = os.open(lf, lf_flags, lf_mode)
    try:
        fcntl.lockf(lf_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        sys.exit('Only one instance of post import can be running')
    incoming_dir = app.config['POST_INCOMING_DIR']
    if not os.path.isabs(incoming_dir):
        incoming_dir = os.path.join(app.instance_path, incoming_dir)
        os.makedirs(incoming_dir, exist_ok=True)
    for file_name in os.listdir(incoming_dir):
        if not file_name.endswith('.md'):
            continue
        file_path = os.path.join(incoming_dir, file_name)
        with open(file_path) as fp:
            text = fp.read()
        post_from_markdown(text)
        os.remove(file_path)
    os.close(lf_fd)
    os.remove(lf)
